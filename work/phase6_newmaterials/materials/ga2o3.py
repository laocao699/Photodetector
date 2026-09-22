"""Calibrated beta-Ga2O3 material and DUV optical parameters.

Electrical parameters reproduce Table 1 of Boulahia et al., Optical and
Quantum Electronics 56, 549 (2024), doi:10.1007/s11082-023-06231-4.

The DUV absorption table is a compact phenomenological fit to the paper's
reported 255 nm response peak, cutoff below 261 nm, and peak generation rate
of about 1e22 cm^-3 s^-1 at 100 mW/cm^2. It is intentionally kept separate
from the electrical parameters so measured n/k tables can replace it later.
"""

import math

import numpy as np

from .registry import SemiconductorMaterial


BOLTZMANN_EV = 8.617333262145e-5  # eV/K
PLANCK_J_S = 6.62607015e-34
LIGHT_SPEED_CM_S = 2.99792458e10

BETA_GA2O3 = SemiconductorMaterial(
    name="beta-Ga2O3",
    bandgap_ev=4.8,
    affinity_ev=4.0,
    relative_permittivity=12.6,
    nc_cm3=3.7e18,
    nv_cm3=5.0e18,
    electron_mobility_cm2_v_s=172.0,
    hole_mobility_cm2_v_s=10.0,
    electron_effective_mass=0.28,
    hole_effective_mass=0.35,
    saturation_velocity_cm_s=1.0e7,
    donor_concentration_cm3=3.0e16,
)

# (wavelength_nm, alpha_cm^-1). The steep edge represents the intrinsic
# solar-blind cutoff reported around 261 nm.
_DUV_ABSORPTION = np.array([
    [155.0, 8.0e5],
    [200.0, 5.0e5],
    [220.0, 3.0e5],
    [240.0, 1.8e5],
    [250.0, 1.3e5],
    [255.0, 1.0e5],
    [260.0, 6.0e4],
    [261.0, 3.0e4],
    [265.0, 1.0e4],
    [270.0, 3.0e3],
    [275.0, 1.0e3],
    [280.0, 3.0e2],
    [300.0, 1.0e1],
    [355.0, 1.0e-1],
    [455.0, 1.0e-3],
])


def intrinsic_carrier_concentration(temperature_k, material=BETA_GA2O3):
    """Boltzmann intrinsic carrier concentration [cm^-3]."""
    return math.sqrt(material.nc_cm3 * material.nv_cm3) * math.exp(
        -material.bandgap_ev / (2.0 * BOLTZMANN_EV * temperature_k)
    )


def alpha_ga2o3(wavelength_nm):
    """DUV absorption coefficient [cm^-1], log-linearly interpolated."""
    wavelength = np.atleast_1d(np.asarray(wavelength_nm, dtype=float))
    lo, hi = _DUV_ABSORPTION[0, 0], _DUV_ABSORPTION[-1, 0]
    if np.any((wavelength < lo) | (wavelength > hi)):
        raise ValueError(f"wavelength must be within {lo:g}-{hi:g} nm")
    result = np.exp(
        np.interp(wavelength, _DUV_ABSORPTION[:, 0], np.log(_DUV_ABSORPTION[:, 1]))
    )
    return result if result.size > 1 else float(result[0])


def photon_energy_joules(wavelength_nm):
    wavelength_cm = np.asarray(wavelength_nm, dtype=float) * 1e-7
    return PLANCK_J_S * LIGHT_SPEED_CM_S / wavelength_cm


def optical_generation_rate(depth_cm, wavelength_nm, power_density_w_cm2,
                            reflectance=0.0, alpha_cm=None):
    """Single-pass Beer-Lambert generation rate [cm^-3 s^-1]."""
    depth = np.asarray(depth_cm, dtype=float)
    alpha = alpha_ga2o3(wavelength_nm) if alpha_cm is None else float(alpha_cm)
    photon_flux = (1.0 - reflectance) * power_density_w_cm2 / photon_energy_joules(
        wavelength_nm
    )
    return alpha * photon_flux * np.exp(-alpha * depth)


# ---------------------------------------------------------------------------
# Deep-level traps (Labed et al., Nanomaterials 2022, 12, 1061, Table 2,
# Si-doped beta-Ga2O3 thin layer).  sigma_p = sigma_n / (sigma_n/sigma_p).
# ---------------------------------------------------------------------------
FREE_ELECTRON_MASS_KG = 9.1093837015e-31
BOLTZMANN_J_K = 1.380649e-23

GA2O3_TRAPS = [
    {"Ec_minus_Et_ev": 0.60, "Nt_cm3": 3.6e13, "sigma_n_cm2": 2.0e-14,
     "sigma_n_over_p": 100.0},
    {"Ec_minus_Et_ev": 0.75, "Nt_cm3": 4.6e13, "sigma_n_cm2": 2.0e-14,
     "sigma_n_over_p": 100.0},
    {"Ec_minus_Et_ev": 0.72, "Nt_cm3": 4.6e13, "sigma_n_cm2": 2.0e-14,
     "sigma_n_over_p": 100.0},
    {"Ec_minus_Et_ev": 1.05, "Nt_cm3": 1.1e14, "sigma_n_cm2": 2.0e-14,
     "sigma_n_over_p": 10.0},
]


def with_overrides(base=BETA_GA2O3, **overrides):
    """Return a copy of a material with selected fields overridden."""
    import dataclasses
    return dataclasses.replace(base, **overrides)


def thermal_velocity_cm_s(effective_mass, temperature_k):
    """Mean thermal velocity v_th = sqrt(3 k_B T / m*) [cm/s]."""
    v = math.sqrt(3.0 * BOLTZMANN_J_K * temperature_k
                  / (effective_mass * FREE_ELECTRON_MASS_KG))
    return v * 100.0  # m/s -> cm/s


def arora_mobility(total_doping_cm3, mu_dop_cm2_v_s, mu_min_cm2_v_s=1.0,
                   n_ref_cm3=1.0e17, alpha=0.85, temperature_k=300.0):
    """Arora doping/temperature-dependent mobility [cm^2/Vs].

    mu = mu_min + mu_dop / (1 + (N/N_ref)^alpha) * (T/300)^beta
    Calibrated so that mu(3e16) ~ mu_dop for beta-Ga2O3.
    """
    temp_factor = (temperature_k / 300.0) ** (-2.0)
    return mu_min_cm2_v_s + mu_dop_cm2_v_s * temp_factor / (
        1.0 + (total_doping_cm3 / n_ref_cm3) ** alpha
    )


def bandgap_narrowing_ev(total_doping_cm3, bgn_coeff=1.3e-2, n_ref_cm3=1.0e18):
    """Band-gap narrowing Delta_Eg [eV] (Slotboom-style logarithmic form).

    DeltaEg = bgn_coeff * ln(N/Nref) for N>Nref, else 0.  A simple, conservative
    model appropriate for the moderate doping used here.
    """
    ratio = total_doping_cm3 / n_ref_cm3
    return 0.0 if ratio <= 1.0 else bgn_coeff * math.log(ratio)


def effective_bandgap_ev(total_doping_cm3, material=BETA_GA2O3):
    """Bandgap reduced by BGN."""
    return material.bandgap_ev - bandgap_narrowing_ev(total_doping_cm3)


def selberherr_ionization_coefficient(field_v_cm, a_coeff, b_coeff):
    """Selberherr impact-ionization coefficient alpha(E) = a*exp(-b/|E|) [1/cm]."""
    field = max(abs(field_v_cm), 1.0)
    return a_coeff * math.exp(-b_coeff / field)


def impact_generation_rate(electron_current_a_cm2, hole_current_a_cm2,
                           field_v_cm, an=2.0e7, bn=2.0e7, ap=5.0e6,
                           bp=2.0e7, electron_charge_c=1.602176634e-19):
    """Impact-ionization generation G = (alpha_n|Jn| + alpha_p|Jp|)/q [cm^-3 s^-1]."""
    alphan = selberherr_ionization_coefficient(field_v_cm, an, bn)
    alphap = selberherr_ionization_coefficient(field_v_cm, ap, bp)
    return (alphan * abs(electron_current_a_cm2)
            + alphap * abs(hole_current_a_cm2)) / electron_charge_c


def trap_srh_parameters(trap_depth_ev, Nt_cm3, sigma_n_cm2, sigma_p_cm2,
                        temperature_k=300.0, material=BETA_GA2O3):
    """SRH n1/p1 and lifetimes for a deep-level trap.

    trap_depth_ev is Ec - E_t.  n1 = n_i exp((E_t - E_i)/kT) with E_i at Eg/2.
    taun = 1/(sigma_n v_th,n Nt), taup = 1/(sigma_p v_th,p Nt).
    Returns (n1, p1, taun, taup).
    """
    n_i = intrinsic_carrier_concentration(temperature_k, material)
    # E_t measured from midgap: E_t - E_i = Eg/2 - trap_depth
    e_t_minus_e_i = material.bandgap_ev / 2.0 - trap_depth_ev
    vt = BOLTZMANN_EV * temperature_k
    n1 = n_i * math.exp(e_t_minus_e_i / vt)
    p1 = n_i * math.exp(-e_t_minus_e_i / vt)
    v_thn = thermal_velocity_cm_s(material.electron_effective_mass, temperature_k)
    v_thp = thermal_velocity_cm_s(material.hole_effective_mass, temperature_k)
    taun = 1.0 / (sigma_n_cm2 * v_thn * Nt_cm3)
    taup = 1.0 / (sigma_p_cm2 * v_thp * Nt_cm3)
    return n1, p1, taun, taup
