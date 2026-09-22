#!/usr/bin/env python3
"""S1: 1D beta-Ga2O3 Schottky dark I-V numerical gate.

This vertical proxy isolates the material and contact physics before the
paper's 2D lateral IZTO/Ga2O3/Al photodetector is introduced.
"""

import pathlib
import sys

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from devsim import (  # noqa: E402
    get_contact_current,
    get_contact_list,
    get_node_model_values,
    set_parameter,
    solve,
    write_devices,
)
from devsim.python_packages.simple_physics import (  # noqa: E402
    GetContactBiasName,
    ece_name,
    hce_name,
)

from device.ga2o3_schottky import (  # noqa: E402
    DONOR_CONCENTRATION_CM3,
    FILM_THICKNESS_CM,
    IZTO_WORK_FUNCTION_EV,
    create_vertical_mesh,
    set_uniform_doping,
)
from materials.contacts import thermionic_saturation_current_density  # noqa: E402
from materials.ga2o3 import BETA_GA2O3  # noqa: E402
from physics import wbg_physics as wbg  # noqa: E402


def total_current(device, contact):
    return (
        get_contact_current(device=device, contact=contact, equation=ece_name)
        + get_contact_current(device=device, contact=contact, equation=hce_name)
    )


def main():
    finite_surface_recombination = (
        len(sys.argv) < 2 or sys.argv[1].lower() in ("1", "true", "te", "on")
    )
    device, region = "Ga2O3Device", "Ga2O3"
    for parameter in ("extended_solver", "extended_model", "extended_equation"):
        set_parameter(name=parameter, value=True)

    create_vertical_mesh(device, region)
    set_uniform_doping(device, region)
    wbg.set_semiconductor_parameters(device, region, taun_s=1e-8, taup_s=1e-8)
    wbg.create_potential_only(device, region)
    set_parameter(device=device, name=GetContactBiasName("anode"), value=0.0)
    set_parameter(device=device, name=GetContactBiasName("cathode"), value=0.0)
    wbg.create_schottky_potential_contact(
        device, region, "anode", IZTO_WORK_FUNCTION_EV
    )
    wbg.create_ohmic_potential_contact(
        device, region, "cathode", DONOR_CONCENTRATION_CM3
    )
    solve(type="dc", absolute_error=1.0, relative_error=1e-12,
          maximum_iterations=80)

    wbg.initialize_carriers(device, region)
    wbg.create_drift_diffusion(device, region)
    wbg.create_schottky_carrier_contact(
        device, "anode", IZTO_WORK_FUNCTION_EV,
        finite_surface_recombination=finite_surface_recombination,
    )
    wbg.create_ohmic_carrier_contact(
        device, "cathode", DONOR_CONCENTRATION_CM3
    )
    solve(type="dc", absolute_error=1e2, relative_error=1e-12,
          maximum_iterations=100)
    wbg.set_dark_generation(device, region)

    equilibrium_anode = total_current(device, "anode")
    equilibrium_cathode = total_current(device, "cathode")
    print("equilibrium KCL: anode=%.6e cathode=%.6e sum=%.3e" %
          (equilibrium_anode, equilibrium_cathode,
           equilibrium_anode + equilibrium_cathode))

    rows = []
    print("finite_surface_recombination:", finite_surface_recombination)
    # Negative anode voltage is reverse bias; positive is forward bias.
    for voltage in np.arange(0.0, -2.001, -0.1):
        set_parameter(device=device, name=GetContactBiasName("anode"),
                      value=float(voltage))
        solve(type="dc", absolute_error=1e2, relative_error=1e-10,
              maximum_iterations=80)
        ia = total_current(device, "anode")
        ic = total_current(device, "cathode")
        rows.append((voltage, ia, ic, ia + ic))
        print("reverse V=%5.2f  Ja=% .6e  Jc=% .6e  KCL=% .2e" %
              (voltage, ia, ic, ia + ic))

    # Return to zero using the converged reverse path, then sweep forward.
    for voltage in np.arange(-1.9, 0.801, 0.1):
        set_parameter(device=device, name=GetContactBiasName("anode"),
                      value=float(voltage))
        solve(type="dc", absolute_error=1e2, relative_error=1e-10,
              maximum_iterations=80)
        if voltage >= -1e-9:
            ia = total_current(device, "anode")
            ic = total_current(device, "cathode")
            rows.append((voltage, ia, ic, ia + ic))
            print("forward V=%5.2f  Ja=% .6e  Jc=% .6e  KCL=% .2e" %
                  (voltage, ia, ic, ia + ic))

    rows = np.asarray(rows)
    np.savetxt(
        "a1_schottky_dark.dat",
        rows,
        header="V_anode_V J_anode_Acm2 J_cathode_Acm2 KCL_Acm2",
    )
    x = np.asarray(get_node_model_values(device=device, region=region, name="x"))
    potential = np.asarray(
        get_node_model_values(device=device, region=region, name="Potential")
    )
    np.savetxt(
        "a1_schottky_profile.dat",
        np.column_stack([x, potential]),
        header="x_cm Potential_V",
    )
    write_devices(file="a1_schottky_dark", type="vtk")

    jte = thermionic_saturation_current_density(
        300.0,
        IZTO_WORK_FUNCTION_EV,
        BETA_GA2O3.affinity_ev,
        BETA_GA2O3.electron_effective_mass,
    )
    reverse = rows[np.argmin(rows[:, 0]), 1]
    print("summary: t=%.0f nm ND=%.2e cm^-3 J_TE=%.3e J_reverse(-2V)=%.3e" %
          (FILM_THICKNESS_CM * 1e7, DONOR_CONCENTRATION_CM3, jte, reverse))


if __name__ == "__main__":
    main()
