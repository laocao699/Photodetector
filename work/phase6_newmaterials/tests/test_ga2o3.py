import math
import pathlib
import sys
import unittest

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from materials.ga2o3 import (  # noqa: E402
    BETA_GA2O3,
    alpha_ga2o3,
    intrinsic_carrier_concentration,
    optical_generation_rate,
)
from materials.contacts import (  # noqa: E402
    richardson_constant,
    schottky_barrier_ev,
    thermionic_saturation_current_density,
)
from physics.wbg_physics import schottky_equilibrium_densities  # noqa: E402
from physics.wbg_physics import schottky_surface_velocities  # noqa: E402
from device.ga2o3_schottky import doping_sweep_values  # noqa: E402
from materials.ga2o3 import trap_srh_parameters, GA2O3_TRAPS  # noqa: E402
from materials.ga2o3 import arora_mobility  # noqa: E402
from materials.ga2o3 import bandgap_narrowing_ev, effective_bandgap_ev  # noqa: E402
from materials.ga2o3 import selberherr_ionization_coefficient  # noqa: E402


class Ga2O3MaterialTests(unittest.TestCase):
    def test_boulahia_material_parameters(self):
        self.assertEqual(BETA_GA2O3.bandgap_ev, 4.8)
        self.assertEqual(BETA_GA2O3.affinity_ev, 4.0)
        self.assertEqual(BETA_GA2O3.relative_permittivity, 12.6)
        self.assertEqual(BETA_GA2O3.nc_cm3, 3.7e18)
        self.assertEqual(BETA_GA2O3.nv_cm3, 5.0e18)
        self.assertEqual(BETA_GA2O3.electron_mobility_cm2_v_s, 172.0)
        self.assertEqual(BETA_GA2O3.hole_mobility_cm2_v_s, 10.0)
        self.assertEqual(BETA_GA2O3.saturation_velocity_cm_s, 1.0e7)

    def test_intrinsic_carrier_concentration_is_finite_at_300_k(self):
        ni = intrinsic_carrier_concentration(300.0)
        expected = math.sqrt(3.7e18 * 5.0e18) * math.exp(
            -4.8 / (2 * 8.617333262145e-5 * 300.0)
        )
        self.assertGreater(ni, 0.0)
        self.assertAlmostEqual(ni / expected, 1.0, places=12)

    def test_duv_absorption_has_solar_blind_cutoff(self):
        alpha = alpha_ga2o3(np.array([255.0, 280.0, 355.0]))
        self.assertGreaterEqual(alpha[0], 7.0e4)
        self.assertLessEqual(alpha[1], 1.0e3)
        self.assertGreater(alpha[0] / alpha[2], 1.0e4)

    def test_255_nm_generation_matches_paper_order_of_magnitude(self):
        generation = optical_generation_rate(
            depth_cm=np.array([0.0]),
            wavelength_nm=255.0,
            power_density_w_cm2=0.1,
            reflectance=0.0,
        )[0]
        self.assertGreaterEqual(generation, 1.0e22)
        self.assertLess(generation, 3.0e22)

    def test_izto_ga2o3_schottky_barrier(self):
        self.assertAlmostEqual(schottky_barrier_ev(4.58, 4.0), 0.58)

    def test_richardson_constant_uses_effective_mass(self):
        self.assertAlmostEqual(richardson_constant(0.28), 33.64816, places=5)

    def test_izto_saturation_current_matches_dark_current_order(self):
        current = thermionic_saturation_current_density(
            temperature_k=300.0,
            work_function_ev=4.58,
            affinity_ev=4.0,
            effective_mass=0.28,
        )
        self.assertGreater(current, 4.0e-4)
        self.assertLess(current, 7.0e-4)

    def test_schottky_equilibrium_density_matches_barrier_formula(self):
        electrons, holes = schottky_equilibrium_densities(
            temperature_k=300.0,
            work_function_ev=4.58,
            material=BETA_GA2O3,
        )
        vt = 8.617333262145e-5 * 300.0
        self.assertAlmostEqual(
            electrons / (BETA_GA2O3.nc_cm3 * math.exp(-0.58 / vt)),
            1.0,
            places=12,
        )
        self.assertLess(holes, 1e-20)

    def test_schottky_surface_velocity_reproduces_richardson_flux(self):
        electron_velocity, _ = schottky_surface_velocities(300.0, BETA_GA2O3)
        electrons, _ = schottky_equilibrium_densities(
            300.0, 4.58, BETA_GA2O3
        )
        current_density = electron_velocity * electrons
        expected = thermionic_saturation_current_density(
            300.0, 4.58, 4.0, 0.28
        )
        self.assertAlmostEqual(current_density / expected, 1.0, places=12)

    def test_doping_sweep_matches_boulahia_range(self):
        values = doping_sweep_values()
        self.assertEqual(values[0], 3.0e16)
        self.assertEqual(values[-1], 1.0e18)
        self.assertEqual(len(values), 6)

    def test_trap_table_present(self):
        self.assertTrue(len(GA2O3_TRAPS) >= 3)

    def test_selberherr_negligible_at_low_field(self):
        low = selberherr_ionization_coefficient(1.0e5, 2.0e7, 2.0e7)
        high = selberherr_ionization_coefficient(1.0e7, 2.0e7, 2.0e7)
        self.assertLess(low, 1.0e-3)
        self.assertGreater(high, low)

    def test_bandgap_narrowing_grows_with_doping(self):
        d_lo = bandgap_narrowing_ev(1.0e16)
        d_hi = bandgap_narrowing_ev(1.0e19)
        self.assertGreaterEqual(d_lo, 0.0)
        self.assertGreater(d_hi, d_lo)
        self.assertLess(effective_bandgap_ev(1.0e19), BETA_GA2O3.bandgap_ev)

    def test_arora_mobility_monotonic_with_doping(self):
        mu_lo = arora_mobility(1.0e16, 172.0)
        mu_hi = arora_mobility(1.0e18, 172.0)
        self.assertLessEqual(mu_lo, 172.0)
        self.assertGreater(mu_lo, mu_hi)
        self.assertGreater(mu_hi, 0.0)

    def test_trap_srh_lifetime_positive_and_finite(self):
        n1, p1, taun, taup = trap_srh_parameters(
            trap_depth_ev=0.74, Nt_cm3=2.0e16, sigma_n_cm2=2.0e-14,
            sigma_p_cm2=2.0e-16, temperature_k=300.0,
        )
        self.assertGreater(n1, 0.0)
        self.assertGreater(p1, 0.0)
        self.assertGreater(taun, 0.0)
        self.assertGreater(taup, 0.0)
        self.assertTrue(math.isfinite(taun) and math.isfinite(taup))


if __name__ == "__main__":
    unittest.main()
