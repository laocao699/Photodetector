# Reusable device-assembly and solve helpers for the 2D cylindrical Si PIN.
#
# Keeping the build sequence here lets every Phase-5 driver share one
# reproducible recipe (mesh -> cylindrical -> doping -> equilibrium ->
# drift-diffusion), exactly the structure promoted to METHOD_TEMPLATE.md.

import math

from devsim import (
    circuit_alter,
    circuit_element,
    get_circuit_node_value,
    get_contact_list,
    set_node_values,
    set_parameter,
    solve,
)
from devsim.python_packages.model_create import CreateSolution
from devsim.python_packages.simple_physics import GetContactBiasName

from device import pin2d
from physics import optical_physics as op


def enable_extended_precision():
    """Extended precision greatly improves the lightly doped PIN conditioning."""
    set_parameter(name="extended_solver", value=True)
    set_parameter(name="extended_model", value=True)
    set_parameter(name="extended_equation", value=True)


def build_and_solve(device, region, t_epi, taun=1.0e-3, taup=None,
                    dy_epi=0.25e-4, nx=16, circuit_contacts=("cathode",)):
    """Build the 2D PIN and converge the dark drift-diffusion equilibrium.

    Parameters
    ----------
    t_epi : float
        Intrinsic EPI thickness [cm] (absorber).
    taun, taup : float
        SRH carrier lifetimes [s]; taup defaults to taun.
    nx : int
        Number of radial cells; the cylindrical node volume converges as
        1/nx, so >=16 keeps the generation integral accurate to ~2 %.
    circuit_contacts : iterable
        Contacts driven by a circuit element (needed for SSAC capacitance).
    """
    if taup is None:
        taup = taun

    pin2d.create_mesh(device, region, t_epi=t_epi, dy_epi=dy_epi, nx=nx)
    pin2d.setup_cylindrical(device, region)
    pin2d.set_doping(device, region, t_epi=t_epi)

    op.SetSiliconParameters(device, region, 300.0)
    set_parameter(device=device, region=region, name="taun", value=taun)
    set_parameter(device=device, region=region, name="taup", value=taup)

    if circuit_contacts:
        circuit_element(name="V1", n1=GetContactBiasName("cathode"), n2=0,
                        value=0.0, acreal=1.0, acimag=0.0)

    op.CreateSiliconPotentialOnly(device, region)
    for c in get_contact_list(device=device):
        is_circuit = c in circuit_contacts
        if not is_circuit:
            set_parameter(device=device, name=GetContactBiasName(c), value=0.0)
        op.CreateSiliconPotentialOnlyContact(device, region, c, is_circuit)
    solve(type="dc", absolute_error=1.0, relative_error=1e-12,
          maximum_iterations=80)

    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")
    set_node_values(device=device, region=region, name="Electrons",
                    init_from="IntrinsicElectrons")
    set_node_values(device=device, region=region, name="Holes",
                    init_from="IntrinsicHoles")
    op.CreateSiliconDriftDiffusionOptical(device, region)
    for c in get_contact_list(device=device):
        op.CreateSiliconDriftDiffusionAtContact(device, region, c,
                                                c in circuit_contacts)

    solve(type="dc", absolute_error=1e4, relative_error=1e-12,
          maximum_iterations=80)
    op.SetDarkGeneration(device, region)


def set_bias(v):
    """Set the cathode circuit source (reverse bias for v > 0)."""
    circuit_alter(name="V1", value=float(v))


def ramp_bias(v_target, dv=0.5):
    """Ramp the reverse bias in steps from 0 to v_target (Newton robustness)."""
    v = 0.0
    while v < v_target - 1e-9:
        v = min(v + dv, v_target)
        set_bias(v)
        solve_dc(relative_error=1e-10, maximum_iterations=60)
    return v


def solve_dc(relative_error=1e-12, maximum_iterations=80):
    solve(type="dc", absolute_error=1e4, relative_error=relative_error,
          maximum_iterations=maximum_iterations)


def apply_optical_ramp(device, region, wavelength_nm, Phi0, reflectance,
                       ramp=(1e-3, 1e-2, 0.1, 0.5, 1.0), **kwargs):
    """Apply a Beer-Lambert source with power ramping for Newton robustness."""
    for scale in ramp:
        op.ApplyBeerLambert(device, region, wavelength_nm, Phi0 * scale,
                            reflectance=reflectance, **kwargs)
        solve_dc(relative_error=1e-8, maximum_iterations=40)


def capacitance(frequency=1.0):
    """Junction capacitance from the small-signal AC imaginary current."""
    solve(type="ac", frequency=frequency)
    return -get_circuit_node_value(node="V1.I",
                                   solution="ssac_imag") / (2 * math.pi * frequency)
