import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from device.ga2o3_schottky import (  # noqa: E402
    FILM_THICKNESS_CM,
    depletion_width_cm,
)


class SchottkyDeviceTests(unittest.TestCase):
    def test_reference_film_is_300_nm(self):
        self.assertEqual(FILM_THICKNESS_CM, 300e-7)

    def test_reverse_bias_depletes_reference_film(self):
        width = depletion_width_cm(reverse_bias_v=2.0)
        self.assertGreater(width, FILM_THICKNESS_CM)


if __name__ == "__main__":
    unittest.main()
