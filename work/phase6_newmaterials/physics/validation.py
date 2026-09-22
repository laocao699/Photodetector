# Validation gates and figure-of-merit helpers for Phase 6 devices.
#
# Pure, testable functions for KCL, energy conservation, responsivity, EQE and
# detectivity, plus small solvers-side helpers.

import math

PLANCK_J_S = 6.62607015e-34
LIGHT_SPEED_CM_S = 2.99792458e10
ELECTRON_CHARGE_C = 1.602176634e-19
BOLTZMANN_J_K = 1.380649e-23


def check_kcl(i_a, i_b, tol=1e-20):
    """Two-terminal current balance: |I_a + I_b| <= tol."""
    return abs(i_a + i_b) <= tol


def max_collectible_photocurrent(power_w_cm2, wavelength_nm, area_cm2,
                                 reflectance=0.0):
    """Upper bound I_ph = q*(1-R)*Phi0*A/(h nu) (gain-free)."""
    hnu = PLANCK_J_S * LIGHT_SPEED_CM_S / (wavelength_nm * 1e-7)
    return ELECTRON_CHARGE_C * (1.0 - reflectance) * power_w_cm2 * area_cm2 / hnu


def energy_conservation_ok(photocurrent_a, power_w_cm2, wavelength_nm,
                           area_cm2, reflectance=0.0, gain=1.0):
    """photocurrent <= gain * max_collectible (gain>1 allowed for impact)."""
    return photocurrent_a <= gain * max_collectible_photocurrent(
        power_w_cm2, wavelength_nm, area_cm2, reflectance
    )


def responsivity_a_w(photocurrent_a, incident_power_w):
    return photocurrent_a / incident_power_w


def eqe_from_responsivity(responsivity_a_w, wavelength_nm):
    return responsivity_a_w * 1239.841984 / wavelength_nm


def detectivity_jones(responsivity_a_w, wavelength_nm, ra_ohm_cm2,
                      temperature_k=300.0):
    """D* = (q lambda/hc) eta sqrt(RA / 4 kT)  [cm Hz^1/2 W^-1, Jones]."""
    eta = eqe_from_responsivity(responsivity_a_w, wavelength_nm)
    hnu = PLANCK_J_S * LIGHT_SPEED_CM_S / (wavelength_nm * 1e-7)
    return (ELECTRON_CHARGE_C / hnu) * eta * math.sqrt(
        ra_ohm_cm2 / (4.0 * BOLTZMANN_J_K * temperature_k)
    )
