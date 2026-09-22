#!/usr/bin/env python3
"""Print the calibrated beta-Ga2O3 material/optical sanity checks."""

import pathlib
import sys

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from device.ga2o3_schottky import depletion_width_cm  # noqa: E402
from materials.contacts import thermionic_saturation_current_density  # noqa: E402
from materials.ga2o3 import (  # noqa: E402
    BETA_GA2O3,
    alpha_ga2o3,
    intrinsic_carrier_concentration,
    optical_generation_rate,
)


def main():
    print(BETA_GA2O3)
    print("ni(300 K) = %.6e cm^-3" % intrinsic_carrier_concentration(300.0))
    print("Wdep(-2 V) = %.3f um" % (depletion_width_cm(2.0) * 1e4))
    print("J_TE(300 K, Wf=4.58 eV) = %.6e A/cm^2" %
          thermionic_saturation_current_density(300.0, 4.58, 4.0, 0.28))
    for wavelength in (250.0, 255.0, 261.0, 280.0, 355.0):
        generation = optical_generation_rate(
            np.array([0.0]), wavelength, 0.1
        )[0]
        print("lambda=%5.1f nm alpha=%9.3e cm^-1 G(0)=%9.3e cm^-3s^-1" %
              (wavelength, alpha_ga2o3(wavelength), generation))


if __name__ == "__main__":
    main()
