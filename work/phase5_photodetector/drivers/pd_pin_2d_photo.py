#!/usr/bin/env python3
"""P5.3  --  2D axisymmetric Si PIN photodiode: spectral responsivity / EQE.

Illuminates the PIN from the top (n+ well side) with a Beer-Lambert generation
profile and extracts, per wavelength:

    R(lambda)   = I_ph / P_opt              [A/W]
    EQE(lambda) = R * hc/(q*lambda)         [-]

Two surface conditions are reported:
    * ideal BARC  : small residual front reflectance (Roger 2018 optimised BARC)
    * bare Si     : Fresnel front reflectance (no coating)
A reflective substrate (metallised back) adds a second forward pass.

Benchmark (Roger et al. 2018):  0.63 A/W @ 800 nm (30 um iEPI);
                                EQE ~ 100 % @ 750 nm.

Usage:  python3 drivers/pd_pin_2d_photo.py [t_epi_um] [taun_s] [V_bias]
"""

import os
import sys

import numpy as np

_PHASE5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PHASE5)

from devsim import get_node_model_values  # noqa: E402

from device import pin2d  # noqa: E402
from device import pin2d_device as dev  # noqa: E402
from physics import optical_physics as op  # noqa: E402
from optics.absorption import fresnel_reflectance_si  # noqa: E402

PHI0 = 1.0e-6          # incident power density [W/cm^2] (low injection)
LAMBDAS = np.arange(400.0, 1001.0, 25.0)


def main():
    t_epi = float(sys.argv[1]) * 1e-4 if len(sys.argv) > 1 else 20e-4
    taun = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0e-3
    v_bias = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    device, region = "MyDevice", "MyRegion"

    dev.enable_extended_precision()
    dev.build_and_solve(device, region, t_epi, taun=taun)

    y = np.asarray(get_node_model_values(device=device, region=region,
                                         name="y"))
    si_mask = y >= 0.0
    t_end = t_epi + pin2d.T_SUB

    dev.ramp_bias(v_bias, dv=0.5)
    dev.solve_dc()
    i_dark = op.TotalContactCurrent(device, "cathode")
    print("t_epi=%.1f um  taun=%.1e s  V_bias=%+.1f V  I_dark=%.4e A"
          % (t_epi * 1e4, taun, v_bias, i_dark))

    def responsivity(reflectance):
        dev.apply_optical_ramp(
            device, region, lambda_nm, PHI0, reflectance,
            coord_name="y", surface_position=0.0, direction=1.0,
            mask=si_mask, back_reflectance=1.0, thickness_cm=t_end,
        )
        dev.solve_dc()
        i_tot = op.TotalContactCurrent(device, "cathode")
        i_ph = i_tot - i_dark
        return i_ph / (PHI0 * pin2d.AREA_CM2)

    rows = []
    print("%5s  %8s  %10s  %10s  %10s  %10s"
          % ("lam", "R_front", "EQE_barc", "R_barc", "EQE_bare", "R_bare"))
    for lambda_nm in LAMBDAS:
        r_barc = 0.03
        r_bare = float(fresnel_reflectance_si(lambda_nm))
        R_barc = responsivity(r_barc)
        R_bare = responsivity(r_bare)
        eqe_barc = R_barc * 1239.841984 / lambda_nm
        eqe_bare = R_bare * 1239.841984 / lambda_nm
        rows.append((lambda_nm, r_barc, eqe_barc, R_barc, r_bare, eqe_bare, R_bare))
        print("%5.0f  %8.3f  %10.4f  %10.4f  %10.4f  %10.4f"
              % (lambda_nm, r_barc, eqe_barc, R_barc, eqe_bare, R_bare))

    print("")
    print("================ P5.3 spectral summary ================")
    def at(lam):
        return rows[int(np.argmin([abs(r[0] - lam) for r in rows]))]

    print("EQE @ 750 nm (BARC) : %.1f %%   (Roger 2018: ~100 %%)"
          % (at(750.0)[2] * 100))
    print("R   @ 800 nm (BARC) : %.3f A/W (Roger 2018: 0.63 A/W, 30 um)"
          % at(800.0)[3])
    print("EQE @ 900 nm (BARC) : %.1f %%" % (at(900.0)[2] * 100))
    print("======================================================")

    tag = int(round(t_epi * 1e4))
    np.savetxt("pd_pin_2d_photo_%dum.dat" % tag, rows,
               header="lambda_nm R_front EQE_barc R_barc_AW R_bare EQE_bare R_bare_AW")
    print("wrote pd_pin_2d_photo_%dum.dat" % tag)


if __name__ == "__main__":
    main()
