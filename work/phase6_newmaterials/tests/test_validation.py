import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from physics.validation import (  # noqa: E402
    detectivity_jones,
    energy_conservation_ok,
    eqe_from_responsivity,
    max_collectible_photocurrent,
    responsivity_a_w,
)


class ValidationTests(unittest.TestCase):
    def test_kcl_energy_helpers(self):
        # max collectible at 0.1 W/cm2, 1e-8 cm^2, 255nm ~ 2e-10 A
        self.assertGreater(max_collectible_photocurrent(0.1, 255.0, 1e-8), 0.0)
        self.assertTrue(energy_conservation_ok(1e-11, 0.1, 255.0, 1e-8))
        self.assertFalse(energy_conservation_ok(1.0, 0.1, 255.0, 1e-8))

    def test_responsivity_eqe_roundtrip(self):
        r = responsivity_a_w(1e-3, 0.05)
        self.assertAlmostEqual(r, 0.02)
        self.assertAlmostEqual(eqe_from_responsivity(0.206, 255.0), 1.0, places=2)

    def test_detectivity_monotonic_in_ra_and_positive(self):
        d1 = detectivity_jones(0.23, 255.0, 1e3)
        d2 = detectivity_jones(0.23, 255.0, 1e6)
        self.assertGreater(d1, 0.0)
        self.assertGreater(d2, d1)


if __name__ == "__main__":
    unittest.main()
