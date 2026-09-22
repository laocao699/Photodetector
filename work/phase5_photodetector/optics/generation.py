# Optical carrier-generation models (Beer-Lambert baseline).
#
# The photo-generation rate at depth d below the illuminated surface is
#     G(d, lambda) = alpha(lambda) * (1 - R) * Phi0 / (h*nu) * exp(-alpha*d)
# with
#     alpha  absorption coefficient [cm^-1]
#     R      residual reflectance after the (optional) ARC / BARC
#     Phi0   incident optical power density [W/cm^2]
#     h*nu   photon energy [J]
# giving G in cm^-3 s^-1.

import numpy as np

from .absorption import (
    PLANCK,
    LIGHT_SPEED,
    alpha_si,
    photon_energy_joules,
)


def beer_lambert_G(depth_cm, wavelength_nm, Phi0, alpha_cm=None, reflectance=0.0,
                   eta_int=1.0, back_reflectance=0.0, thickness_cm=None):
    """Photo-generation rate G [cm^-3 s^-1] versus depth.

    Parameters
    ----------
    depth_cm : array_like
        Depth below the illuminated surface [cm]; 0 at the surface.
    wavelength_nm : float
        Vacuum wavelength [nm].
    Phi0 : float
        Incident optical power density [W/cm^2].
    alpha_cm : float, optional
        Absorption coefficient [cm^-1]; default: tabulated Si value.
    reflectance : float
        Residual front (single-interface) power reflectance; the coupled
        fraction is (1 - reflectance).
    eta_int : float
        Internal quantum yield (absorbed photon -> collected pair), usually 1.
    back_reflectance : float
        Power reflectance of the rear interface.  A reflective substrate
        (metallised back) creates a second forward pass, adding
        R_b*exp(-alpha*(2*thickness - depth)).
    thickness_cm : float, optional
        Absorber thickness used for the reflected path (defaults to 0, i.e.
        a single pass).
    """
    depth_cm = np.asarray(depth_cm, dtype=float)
    a = alpha_si(wavelength_nm) if alpha_cm is None else float(alpha_cm)
    hnu = photon_energy_joules(wavelength_nm)
    forward = np.exp(-a * depth_cm)
    if back_reflectance > 0.0 and thickness_cm:
        backward = back_reflectance * np.exp(-a * (2.0 * thickness_cm - depth_cm))
        total = forward + backward
    else:
        total = forward
    return eta_int * a * (1.0 - reflectance) * Phi0 / hnu * total


def absorbed_flux_fraction(wavelength_nm, thickness_cm, alpha_cm=None,
                           reflectance=0.0):
    """Fraction of incident photons absorbed in a slab of given thickness."""
    a = alpha_si(wavelength_nm) if alpha_cm is None else float(alpha_cm)
    return (1.0 - reflectance) * (1.0 - np.exp(-a * np.asarray(thickness_cm)))


def photocurrent_density_ideal(wavelength_nm, Phi0, thickness_cm, alpha_cm=None,
                               reflectance=0.0, eta_int=1.0):
    """Ideal (100% collection) photocurrent density [A/cm^2].

    J_ph = q * (1-R) * Phi0/(h*nu) * (1 - exp(-alpha*W)) * eta_int
    This is the analytic target used to validate the drift-diffusion solution
    for a fully depleted absorber.
    """
    from .absorption import ELECTRON_CHARGE

    a = alpha_si(wavelength_nm) if alpha_cm is None else float(alpha_cm)
    hnu = photon_energy_joules(wavelength_nm)
    frac = (1.0 - reflectance) * (1.0 - np.exp(-a * np.asarray(thickness_cm)))
    return ELECTRON_CHARGE * eta_int * Phi0 / hnu * frac


def internal_quantum_efficiency(wavelength_nm, thickness_cm, alpha_cm=None,
                                reflectance=0.0):
    """IQE of an ideal slab: fraction of *absorbed* photons collected = 1 here,
    external QE = (1-R)(1-exp(-alpha W)).  Returned for convenience."""
    return (1.0 - reflectance) * (1.0 - np.exp(-(alpha_si(wavelength_nm)
                                                if alpha_cm is None else alpha_cm)
                                               * np.asarray(thickness_cm)))


def responsivity_from_qe(qe, wavelength_nm):
    """Responsivity [A/W] from (external) quantum efficiency."""
    return qe * np.asarray(wavelength_nm, dtype=float) / 1239.841984


def qe_from_responsivity(responsivity, wavelength_nm):
    """External quantum efficiency from responsivity [A/W]."""
    return np.asarray(responsivity, dtype=float) * 1239.841984 / np.asarray(
        wavelength_nm, dtype=float
    )


if __name__ == "__main__":
    for wl in (750.0, 800.0, 900.0):
        qe30 = internal_quantum_efficiency(wl, 30e-4)
        print("W=30um lambda=%.0f nm  EQE=%.3f  R=%.3f A/W"
              % (wl, qe30, responsivity_from_qe(qe30, wl)))
