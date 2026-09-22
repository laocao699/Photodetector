# Optical absorption data for crystalline silicon at 300 K.
#
# Data source (table values, interpolated in log-alpha):
#   M. A. Green and M. J. Keevers, "Optical properties of intrinsic silicon at
#   300 K", Progress in Photovoltaics 3, 189-192 (1995);
#   M. A. Green, "Self-consistent optical parameters of intrinsic silicon at
#   300 K including temperature coefficients", Sol. Energy Mater. Sol. Cells
#   92, 1305-1310 (2008).
#
# The wavelengths below 400 nm and above 1100 nm are less relevant for the
# Si PIN benchmark and are included only for completeness.  alpha is the
# absorption coefficient in cm^-1, n the real refractive index.

import numpy as np

# Physical constants (CGS, matching DEVSIM's cm/g/s unit system)
PLANCK = 6.62607015e-34      # J*s
LIGHT_SPEED = 2.99792458e10  # cm/s
ELECTRON_CHARGE = 1.602176634e-19  # C

# (wavelength_nm, alpha_cm^-1, n)
_SI_TABLE = np.array([
    # nm        alpha (1/cm)     n
    [250.0, 1.84e6, 1.60],
    [300.0, 1.10e6, 1.50],
    [350.0, 2.20e5, 1.60],
    [400.0, 9.52e4, 1.88],
    [450.0, 4.35e4, 2.28],
    [500.0, 1.11e4, 2.65],
    [550.0, 8.15e3, 3.00],
    [600.0, 4.09e3, 3.30],
    [650.0, 2.64e3, 3.54],
    [700.0, 2.01e3, 3.69],
    [750.0, 1.22e3, 3.70],
    [800.0, 8.63e2, 3.69],
    [850.0, 5.49e2, 3.67],
    [900.0, 3.24e2, 3.64],
    [950.0, 1.83e2, 3.61],
    [1000.0, 9.60e1, 3.57],
    [1050.0, 4.20e1, 3.54],
    [1100.0, 1.30e1, 3.51],
    [1150.0, 4.00e0, 3.49],
])

WAVELENGTHS_NM = _SI_TABLE[:, 0]


def alpha_si(wavelength_nm):
    """Absorption coefficient of intrinsic Si [cm^-1] at 300 K.

    Log-linear interpolation in alpha between tabulated points.
    """
    wl = np.atleast_1d(np.asarray(wavelength_nm, dtype=float))
    out = np.exp(np.interp(wl, _SI_TABLE[:, 0], np.log(_SI_TABLE[:, 1])))
    return out if out.size > 1 else float(out[0])


def n_si(wavelength_nm):
    """Real refractive index of intrinsic Si at 300 K (linear interpolation)."""
    wl = np.atleast_1d(np.asarray(wavelength_nm, dtype=float))
    out = np.interp(wl, _SI_TABLE[:, 0], _SI_TABLE[:, 2])
    return out if out.size > 1 else float(out[0])


def fresnel_reflectance_si(wavelength_nm, n_ambient=1.0):
    """Normal-incidence Fresnel reflectance of an air/Si interface.

    Uncoated mirror loss; an anti-reflective coating (BARC) reduces this
    towards zero.  For the benchmark the *residual* reflectance after the BARC
    is what matters and is supplied by the caller.
    """
    n = n_si(wavelength_nm)
    return ((n - n_ambient) / (n + n_ambient)) ** 2


def photon_energy_joules(wavelength_nm):
    """Photon energy h*nu [J] for a vacuum wavelength in nm."""
    wl_cm = np.asarray(wavelength_nm, dtype=float) * 1e-7  # nm -> cm
    return PLANCK * LIGHT_SPEED / wl_cm


def absorption_length_nm(wavelength_nm):
    """1/alpha expressed in nm (optical penetration depth)."""
    return 1e7 / alpha_si(wavelength_nm)  # cm -> nm


if __name__ == "__main__":
    for wl in (425.0, 750.0, 800.0, 900.0):
        print(
            "lambda=%6.1f nm  alpha=%9.3e 1/cm  L_abs=%8.2f um  R_fresnel=%.3f"
            % (wl, alpha_si(wl), absorption_length_nm(wl) / 1e3,
               fresnel_reflectance_si(wl))
        )
