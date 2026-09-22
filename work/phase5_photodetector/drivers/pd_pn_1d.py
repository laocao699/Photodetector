#!/usr/bin/env python3
"""P5.1  --  1D Si PIN photodiode: optical-generation sign/unit validation.

Goal
----
Before touching the 2D benchmark, validate the new optical generation module
against a closed-form target on the simplest possible device:

    * 1D p+ / i / n+ silicon PIN, i-region fully depleted at V = -5 V.
    * Beer-Lambert generation restricted to the i-region (mask), so that
      every generated electron-hole pair is collected (no diffusion from the
      quasi-neutral regions, no recombination in the field-free zones).
    * For a fully depleted absorber the *collected* photocurrent density must
      equal the *generated* carrier integral:
            J_ph,ideal = q * integral G(x) dx
      computed here with the actual mesh quadrature (NodeVolume).

The driver reports dark current, illuminated current, simulated photocurrent,
the integral target and the relative error.  Passing means the DEVSIM source
sign, units and the Beer-Lambert model are all correct.

Run:  python3 drivers/pd_pn_1d.py
"""

import os
import sys

import numpy as np

_PHASE5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PHASE5)

from devsim import (  # noqa: E402
    add_1d_contact,
    add_1d_mesh_line,
    add_1d_region,
    create_1d_mesh,
    create_device,
    finalize_mesh,
    get_contact_list,
    get_node_model_values,
    set_parameter,
    solve,
)
from devsim.python_packages.simple_physics import GetContactBiasName  # noqa: E402

from physics import optical_physics as op  # noqa: E402
from optics.absorption import ELECTRON_CHARGE, alpha_si  # noqa: E402

# ----------------------------------------------------------------------------
# Device definition (cm)
# ----------------------------------------------------------------------------
L_P = 0.5e-4    # p+ anode thickness
L_I = 5.0e-4    # intrinsic (lightly n) absorber
L_N = 0.5e-4    # n+ cathode thickness
X_PI = L_P
X_IN = L_P + L_I
X_END = L_P + L_I + L_N

NA_P = 1.0e19
ND_I = 1.0e14
ND_N = 1.0e19

WAVELENGTH_NM = 800.0
PHI0 = 1.0e-3          # 1 mW/cm^2
REFLECTANCE = 0.0      # ideal AR in this validation
V_REVERSE = -5.0


def build_mesh(device, region):
    create_1d_mesh(mesh="pin1d")
    add_1d_mesh_line(mesh="pin1d", pos=0.0, ps=1e-7, tag="top")
    for pos, ps in [
        (X_PI * 0.5, 1e-6),
        (X_PI, 1e-7),
        (X_PI + 0.25 * L_I, 1e-5),
        (X_PI + 0.50 * L_I, 1e-5),
        (X_PI + 0.75 * L_I, 1e-5),
        (X_IN, 1e-7),
        (X_IN + L_N * 0.5, 1e-6),
    ]:
        add_1d_mesh_line(mesh="pin1d", pos=pos, ps=ps)
    add_1d_mesh_line(mesh="pin1d", pos=X_END, ps=1e-7, tag="bot")
    add_1d_contact(mesh="pin1d", name="top", tag="top", material="metal")
    add_1d_contact(mesh="pin1d", name="bot", tag="bot", material="metal")
    add_1d_region(mesh="pin1d", material="Si", region=region,
                  tag1="top", tag2="bot")
    finalize_mesh(mesh="pin1d")
    create_device(mesh="pin1d", device=device)


def main():
    device, region = "MyDevice", "MyRegion"

    build_mesh(device, region)
    op.SetSiliconParameters(device, region, 300.0)

    # doping: p+ / n- / n+
    from devsim.python_packages.model_create import CreateNodeModel

    CreateNodeModel(device, region, "Acceptors",
                    "%.6e*step(%.6e-x)" % (NA_P, X_PI))
    CreateNodeModel(device, region, "Donors",
                    "%.6e*step(x-%.6e) + %.6e*(step(x-%.6e)-step(x-%.6e))"
                    % (ND_N, X_IN, ND_I, X_PI, X_IN))
    CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")

    # ---- potential-only equilibrium ----
    op.CreateSiliconPotentialOnly(device, region)
    for c in get_contact_list(device=device):
        set_parameter(device=device, name=GetContactBiasName(c), value=0.0)
        op.CreateSiliconPotentialOnlyContact(device, region, c)
    solve(type="dc", absolute_error=1.0, relative_error=1e-12,
          maximum_iterations=50)

    # ---- drift-diffusion with optical generation ----
    from devsim.python_packages.model_create import CreateSolution

    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")
    from devsim import set_node_values

    set_node_values(device=device, region=region, name="Electrons",
                    init_from="IntrinsicElectrons")
    set_node_values(device=device, region=region, name="Holes",
                    init_from="IntrinsicHoles")
    op.CreateSiliconDriftDiffusionOptical(device, region)
    for c in get_contact_list(device=device):
        op.CreateSiliconDriftDiffusionAtContact(device, region, c)
    solve(type="dc", absolute_error=1e6, relative_error=1e-10,
          maximum_iterations=50)

    # ---- reverse ramp to -5 V (dark) ----
    op.SetDarkGeneration(device, region)
    v = 0.0
    while v > V_REVERSE - 1e-9:
        set_parameter(device=device, name=GetContactBiasName("top"), value=v)
        solve(type="dc", absolute_error=1e6, relative_error=1e-10,
              maximum_iterations=50)
        v -= 1.0
    i_dark = op.TotalContactCurrent(device, "top")
    print("dark current @ %.1f V : I_dark = %.6e A/cm^2" % (V_REVERSE, i_dark))

    # depletion check: electrons/holes vanish in the i-region
    x = np.asarray(get_node_model_values(device=device, region=region, name="x"))
    n = np.asarray(get_node_model_values(device=device, region=region,
                                         name="Electrons"))
    i_center = (x > X_PI + 0.25 * L_I) & (x < X_IN - 0.25 * L_I)
    print("i-region mean n = %.3e cm^-3 (depleted if << %.1e)" % (n[i_center].mean(), ND_I))

    # ---- illuminated: generation over the *whole* i-region ----
    gen_mask = (x >= X_PI) & (x <= X_IN)
    G = op.ApplyBeerLambert(device, region, WAVELENGTH_NM, PHI0,
                            reflectance=REFLECTANCE, coord_name="x",
                            surface_position=0.0, direction=1.0, mask=gen_mask)
    print("alpha(%.0f nm) = %.1f cm^-1   peak G = %.3e cm^-3 s^-1"
          % (WAVELENGTH_NM, alpha_si(WAVELENGTH_NM), G.max()))

    solve(type="dc", absolute_error=1e6, relative_error=1e-10,
          maximum_iterations=80)
    i_photo_total = op.TotalContactCurrent(device, "top")
    # both currents are reverse (negative); photocurrent magnitude is the increase
    j_ph_sim = i_dark - i_photo_total

    # ideal target: every generated carrier collected
    V = np.asarray(get_node_model_values(device=device, region=region,
                                         name="NodeVolume"))
    j_ph_ideal = ELECTRON_CHARGE * float(np.sum(G * V))

    # closed-form Beer-Lambert value for the same masked slab, accounting for
    # attenuation by the p+ overlayer at the i-region entrance
    from optics.generation import photocurrent_density_ideal

    phi_at_i = PHI0 * np.exp(-alpha_si(WAVELENGTH_NM) * X_PI)
    j_ph_closed = float(photocurrent_density_ideal(
        WAVELENGTH_NM, phi_at_i, (X_IN - X_PI), reflectance=REFLECTANCE))

    print("")
    print("================ P5.1 validation ================")
    print("J_ph simulated (I_illum - I_dark) : %.6e A/cm^2" % j_ph_sim)
    print("J_ph mesh-integral  q*sum(G*V)    : %.6e A/cm^2" % j_ph_ideal)
    print("J_ph closed-form Beer-Lambert     : %.6e A/cm^2" % j_ph_closed)
    print("rel. error sim vs integral        : %.3f %%" %
          (100.0 * (j_ph_sim - j_ph_ideal) / j_ph_ideal))
    print("rel. error closed vs integral     : %.3f %%" %
          (100.0 * (j_ph_closed - j_ph_ideal) / j_ph_ideal))
    print("responsivity R = J_ph/Phi0        : %.4f A/W" % (j_ph_sim / PHI0))
    print("================================================")

    np.savetxt(
        "pd_pn_1d_profile.dat",
        np.column_stack([x, n, G]),
        header="x_cm Electrons_cm-3 OpticalGeneration_cm-3s-1",
    )
    print("wrote pd_pn_1d_profile.dat")


if __name__ == "__main__":
    main()
