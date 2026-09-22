#!/usr/bin/env python3
"""P5.2  --  2D axisymmetric Si PIN photodiode: dark I-V and C-V.

Benchmark structure after Roger et al., MDPI Proceedings 2018, 2, 909
(365 um circular PIN, 20/30 um intrinsic EPI on a p+ substrate).

Extracts:
  * reverse dark current vs bias   (Roger 2018: 3.5-10 pA @ 1 V)
  * junction capacitance by SSAC   (bounded by eps*A/t_epi)

The cathode is a circuit-coupled contact driven by V1, which allows the
small-signal AC solve used to extract C(V).  The finite carrier lifetime
(taun/taup) sets the generation-limited reverse leakage.

Usage:  python3 drivers/pd_pin_2d_dark.py [t_epi_um] [taun_s]
"""

import os
import sys

import numpy as np

_PHASE5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PHASE5)

from device import pin2d  # noqa: E402
from device import pin2d_device as dev  # noqa: E402
from physics import optical_physics as op  # noqa: E402


def main():
    t_epi = float(sys.argv[1]) * 1e-4 if len(sys.argv) > 1 else 20e-4
    taun = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0e-3
    device, region = "MyDevice", "MyRegion"

    dev.enable_extended_precision()
    dev.build_and_solve(device, region, t_epi, taun=taun)

    print("area = %.6e cm^2 (circle r=%.1f um), t_epi = %.1f um, taun = %.1e s"
          % (pin2d.AREA_CM2, pin2d.RADIUS * 1e4, t_epi * 1e4, taun))

    vgrid = np.concatenate([np.arange(0.0, 1.001, 0.25),
                            np.arange(1.5, 5.01, 0.5)])
    rows = []
    for v in vgrid:
        dev.set_bias(v)
        dev.solve_dc()
        I = op.TotalContactCurrent(device, "cathode")
        C = dev.capacitance()
        rows.append((v, I, I / pin2d.AREA_CM2, C))
        print("V=%5.2f  I_dark=%12.4e A  J=%11.4e A/cm2  C=%8.4f pF"
              % (v, I, I / pin2d.AREA_CM2, C * 1e12))

    eps_si = 11.7 * 8.8541878128e-14
    C_plate = eps_si * pin2d.AREA_CM2 / t_epi
    print("")
    print("================ P5.2 dark summary ================")
    for v, I, J, C in rows:
        if abs(v - 1.0) < 1e-6:
            print("I_dark @ 1 V : %8.3f pA   (Roger 2018: 3.5-10 pA)"
                  % (abs(I) * 1e12))
    print("C_plate = eps*A/t_epi (depletion bound) : %8.3f pF" % (C_plate * 1e12))
    print("C @ 1 V                                  : %8.3f pF"
          % (rows[[r[0] for r in rows].index(1.0)][3] * 1e12))
    print("===================================================")

    tag = int(round(t_epi * 1e4))
    np.savetxt("pd_pin_2d_dark_%dum.dat" % tag, rows,
               header="V_cathode_V I_dark_A J_dark_Acm2 C_F")
    print("wrote pd_pin_2d_dark_%dum.dat" % tag)


if __name__ == "__main__":
    main()
