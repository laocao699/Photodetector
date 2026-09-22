#!/usr/bin/env python3
"""S2/S3: planar IZTO/beta-Ga2O3/Al solar-blind photodetector.

The paper specifies 1 um-wide top contacts but not their spacing. The default
2 um gap is therefore an explicit sensitivity parameter, not hidden input.
Current per out-of-plane centimetre is normalised by the 1 um contact width.
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
    CALIBRATED_SCHOTTKY_BARRIER_EV,
    DONOR_CONCENTRATION_CM3,
    FILM_THICKNESS_CM,
    IZTO_OPTICAL_TRANSMISSION_255NM,
    IZTO_WORK_FUNCTION_EV,
    PLANAR_CONTACT_WIDTH_CM,
    create_planar_mesh,
    set_uniform_doping,
)
from materials.ga2o3 import BETA_GA2O3, optical_generation_rate  # noqa: E402
from physics import wbg_physics as wbg  # noqa: E402


POWER_W_CM2 = 0.1 * IZTO_OPTICAL_TRANSMISSION_255NM  # coupled into Ga2O3
WAVELENGTH_NM = 255.0


def total_current(device, contact):
    return (
        get_contact_current(device=device, contact=contact, equation=ece_name)
        + get_contact_current(device=device, contact=contact, equation=hce_name)
    )


def solve_dc(relative_error=1e-9, maximum_iterations=100):
    solve(type="dc", absolute_error=1e3, relative_error=relative_error,
          maximum_iterations=maximum_iterations)


def set_generation(device, region, wavelength_nm, power_w_cm2, scale=1.0,
                   gap_cm=2.0e-4, thickness_cm=FILM_THICKNESS_CM):
    x = np.asarray(get_node_model_values(device=device, region=region, name="x"))
    y = np.asarray(get_node_model_values(device=device, region=region, name="y"))
    gap_start = PLANAR_CONTACT_WIDTH_CM
    gap_end = PLANAR_CONTACT_WIDTH_CM + gap_cm
    illuminated = (x > gap_start) & (x < gap_end)
    depth = thickness_cm - y
    generation = optical_generation_rate(
        depth, wavelength_nm, power_w_cm2 * scale, reflectance=0.0
    )
    generation[~illuminated] = 0.0
    wbg.set_optical_generation(device, region, generation)
    return generation


def build_device(donor_concentration_cm3=DONOR_CONCENTRATION_CM3,
                 barrier_ev=CALIBRATED_SCHOTTKY_BARRIER_EV,
                 work_function_ev=IZTO_WORK_FUNCTION_EV,
                 gap_cm=2.0e-4, use_traps=False, use_arora=False,
                 thickness_cm=FILM_THICKNESS_CM, material=None,
                 name="a2"):
    device = "PlanarGa2O3_" + name
    region = "Ga2O3"
    for parameter in ("extended_solver", "extended_model", "extended_equation"):
        set_parameter(name=parameter, value=True)
    geometry = create_planar_mesh(device, region, gap_cm=gap_cm,
                                  thickness_cm=thickness_cm,
                                  name="mesh_" + name)
    set_uniform_doping(device, region, donor_concentration_cm3)
    wbg.set_semiconductor_parameters(device, region, material=material
                                     if material is not None else BETA_GA2O3,
                                     taun_s=1e-8, taup_s=1e-8)
    wbg.create_potential_only(device, region)
    for contact in get_contact_list(device=device):
        set_parameter(device=device, name=GetContactBiasName(contact), value=0.0)
    wbg.create_schottky_potential_contact(
        device, region, "anode", work_function_ev, barrier_ev=barrier_ev,
    )
    wbg.create_ohmic_potential_contact(
        device, region, "cathode", donor_concentration_cm3
    )
    solve(type="dc", absolute_error=1.0, relative_error=1e-12,
          maximum_iterations=100)
    wbg.initialize_carriers(device, region)
    traps = wbg.build_trap_list() if use_traps else None
    wbg.create_drift_diffusion(device, region, traps=traps, use_arora=use_arora)
    wbg.create_schottky_carrier_contact(
        device, "anode", work_function_ev, barrier_ev=barrier_ev,
    )
    wbg.create_ohmic_carrier_contact(
        device, "cathode", donor_concentration_cm3
    )
    solve_dc(relative_error=1e-11)
    wbg.set_dark_generation(device, region)
    return device, region, geometry


def dark_sweep(device, region, voltage_max=-2.0):
    rows = []
    for voltage in np.arange(0.0, voltage_max - 1e-9, -0.1):
        set_parameter(device=device, name=GetContactBiasName("anode"),
                      value=float(voltage))
        solve_dc()
        current = total_current(device, "anode")
        rows.append((voltage, current, current / PLANAR_CONTACT_WIDTH_CM))
    return np.asarray(rows)


def illuminate_at_operating_point(device, region, wavelength_nm,
                                  power_w_cm2, gap_cm=2.0e-4,
                                  thickness_cm=FILM_THICKNESS_CM):
    for scale in (1e-4, 1e-3, 1e-2, 0.1, 0.5, 1.0):
        set_generation(
            device, region, wavelength_nm, power_w_cm2, scale, gap_cm=gap_cm,
            thickness_cm=thickness_cm,
        )
        solve_dc(relative_error=1e-8)
    return total_current(device, "anode") / PLANAR_CONTACT_WIDTH_CM


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doping", type=float, default=DONOR_CONCENTRATION_CM3)
    parser.add_argument("--wavelength", type=float, default=WAVELENGTH_NM)
    parser.add_argument("--power", type=float, default=POWER_W_CM2)
    parser.add_argument("--gap", type=float, default=2.0e-4)
    parser.add_argument("--traps", action="store_true",
                        help="include Labed 2022 deep-level traps")
    parser.add_argument("--arora", action="store_true",
                        help="use Arora doping-dependent mobility")
    parser.add_argument("--tag", default="a2_planar")
    return parser.parse_args()


def main():
    args = parse_args()
    device, region, geometry = build_device(
        donor_concentration_cm3=args.doping,
        gap_cm=args.gap,
        use_traps=args.traps,
        use_arora=args.arora,
    )
    dark = dark_sweep(device, region)
    illuminated_density = illuminate_at_operating_point(
        device, region, args.wavelength, args.power, gap_cm=args.gap
    )
    dark_density = dark[-1, 2]
    photocurrent_density = illuminated_density - dark_density
    responsivity = abs(photocurrent_density) / args.power
    pdcr = abs(illuminated_density / dark_density)

    print("geometry:", geometry)
    print("doping=%.3e cm^-3  wavelength=%.1f nm  traps=%s" %
          (args.doping, args.wavelength, args.traps))
    print("dark J(-2V)=%.6e A/cm^2" % dark_density)
    print("illuminated J(-2V,255nm)=%.6e A/cm^2" % illuminated_density)
    print("photocurrent density=%.6e A/cm^2" % photocurrent_density)
    print("PDCR=%.6e (paper ~1e2 at -2V)" % pdcr)
    print("responsivity=%.6f A/W (paper 0.23 A/W)" % responsivity)

    np.savetxt(
        f"{args.tag}_dark.dat", dark,
        header="V_anode_V I_anode_Apercm J_anode_Acm2",
    )
    np.savetxt(
        f"{args.tag}_operating_point.dat",
        np.array([[dark_density, illuminated_density, photocurrent_density,
                   pdcr, responsivity]]),
        header="J_dark_Acm2 J_illum_Acm2 J_photo_Acm2 PDCR R_AW",
    )
    write_devices(file=f"{args.tag}_photo", type="vtk")


if __name__ == "__main__":
    main()
