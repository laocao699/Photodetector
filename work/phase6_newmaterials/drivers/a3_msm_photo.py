#!/usr/bin/env python3
"""S5: interdigitated beta-Ga2O3 MSM solar-blind photodetector proxy.

This is a two-Schottky-contact progression of the planar device, using the
same material library and optical front-end. It is included as a checked
engineering extension of Boulahia's IZTO/Ga2O3 Schottky photodiode.
"""

import argparse
import pathlib
import sys

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from devsim import (  # noqa: E402
    get_contact_current,
    get_contact_list,
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
    CALIBRATED_SCHOTTKY_BARRIER_EV,
    DONOR_CONCENTRATION_CM3,
    FILM_THICKNESS_CM,
    IZTO_OPTICAL_TRANSMISSION_255NM,
    IZTO_WORK_FUNCTION_EV,
    create_msm_mesh,
    set_uniform_doping,
)
from materials.ga2o3 import optical_generation_rate  # noqa: E402
from physics import wbg_physics as wbg  # noqa: E402


POWER_W_CM2 = 0.1 * IZTO_OPTICAL_TRANSMISSION_255NM
WAVELENGTH_NM = 255.0


def total_current(device, contact):
    return (
        get_contact_current(device=device, contact=contact, equation=ece_name)
        + get_contact_current(device=device, contact=contact, equation=hce_name)
    )


def solve_dc(relative_error=1e-9, maximum_iterations=100):
    solve(type="dc", absolute_error=1e3, relative_error=relative_error,
          maximum_iterations=maximum_iterations)


def set_generation(device, region, wavelength_nm, power_w_cm2, scale=1.0):
    y = np.asarray(
        __import__("devsim").get_node_model_values(
            device=device, region=region, name="y"
        )
    )
    depth = FILM_THICKNESS_CM - y
    generation = optical_generation_rate(
        depth, wavelength_nm, power_w_cm2 * scale, reflectance=0.0
    )
    wbg.set_optical_generation(device, region, generation)
    return generation


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doping", type=float, default=DONOR_CONCENTRATION_CM3)
    parser.add_argument("--wavelength", type=float, default=WAVELENGTH_NM)
    parser.add_argument("--power", type=float, default=POWER_W_CM2)
    parser.add_argument("--gap", type=float, default=2.0e-4)
    parser.add_argument("--fingers", type=int, default=4)
    parser.add_argument("--tag", default="a3_msm")
    return parser.parse_args()


def main():
    args = parse_args()
    device, region = "Ga2O3MSM", "Ga2O3"
    for parameter in ("extended_solver", "extended_model", "extended_equation"):
        set_parameter(name=parameter, value=True)

    geometry = create_msm_mesh(
        device, region, gap_cm=args.gap, finger_count=args.fingers
    )
    set_uniform_doping(device, region, args.doping)
    wbg.set_semiconductor_parameters(device, region, taun_s=1e-8, taup_s=1e-8)
    wbg.create_potential_only(device, region)
    for contact in get_contact_list(device=device):
        set_parameter(device=device, name=GetContactBiasName(contact), value=0.0)
    for contact in ("anode_left", "anode_right"):
        wbg.create_schottky_potential_contact(
            device, region, contact, IZTO_WORK_FUNCTION_EV,
            barrier_ev=CALIBRATED_SCHOTTKY_BARRIER_EV,
        )
    for contact in ("cathode_left", "cathode_right"):
        wbg.create_ohmic_potential_contact(
            device, region, contact, DONOR_CONCENTRATION_CM3
        )
    solve(type="dc", absolute_error=1.0, relative_error=1e-12,
          maximum_iterations=100)

    wbg.initialize_carriers(device, region)
    wbg.create_drift_diffusion(device, region)
    for contact in ("anode_left", "anode_right"):
        wbg.create_schottky_carrier_contact(
            device, contact, IZTO_WORK_FUNCTION_EV,
            barrier_ev=CALIBRATED_SCHOTTKY_BARRIER_EV,
        )
    for contact in ("cathode_left", "cathode_right"):
        wbg.create_ohmic_carrier_contact(
            device, contact, DONOR_CONCENTRATION_CM3
        )
    solve_dc(relative_error=1e-11)
    wbg.set_dark_generation(device, region)

    dark = []
    for voltage in np.arange(0.0, -2.001, -0.1):
        set_parameter(
            device=device, name=GetContactBiasName("anode_left"), value=float(voltage)
        )
        set_parameter(
            device=device, name=GetContactBiasName("anode_right"), value=float(voltage)
        )
        solve_dc()
        current = total_current(device, "anode_left") + total_current(
            device, "anode_right"
        )
        dark.append((voltage, current, current))
    dark = np.asarray(dark)

    for scale in (1e-4, 1e-3, 1e-2, 0.1, 0.5, 1.0):
        set_generation(device, region, args.wavelength, args.power, scale)
        solve_dc(relative_error=1e-8)
    illuminated_current = total_current(device, "anode_left") + total_current(
        device, "anode_right"
    )
    dark_current = dark[-1, 1]
    pdcr = abs(illuminated_current / dark_current)
    responsivity = abs(illuminated_current - dark_current) / (
        args.power * geometry["x_end"]
    )

    print("geometry:", geometry)
    print("dark I(-2V)=%.6e A" % dark_current)
    print("illuminated I(-2V,255nm)=%.6e A" % illuminated_current)
    print("PDCR=%.6e" % pdcr)
    print("area-normalized responsivity=%.6f A/W" % responsivity)

    np.savetxt(f"{args.tag}_dark.dat", dark,
               header="V_anode_V I_total_Apercm I_total_Apercm")
    write_devices(file=f"{args.tag}_photo", type="vtk")


if __name__ == "__main__":
    main()
