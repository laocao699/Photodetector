"""Contact parameter helpers for wide-bandgap Schottky devices."""

import math

from .ga2o3 import BOLTZMANN_EV


RICHARDSON_FREE_ELECTRON = 120.172  # A cm^-2 K^-2


def schottky_barrier_ev(work_function_ev, affinity_ev):
    """Ideal n-type Schottky barrier Phi_B = Phi_M - chi [eV]."""
    return work_function_ev - affinity_ev


def richardson_constant(effective_mass):
    """Effective Richardson constant A* [A cm^-2 K^-2]."""
    return RICHARDSON_FREE_ELECTRON * effective_mass


def thermionic_saturation_current_density(temperature_k, work_function_ev,
                                          affinity_ev, effective_mass):
    """Ideal thermionic-emission saturation current density [A/cm^2]."""
    barrier = schottky_barrier_ev(work_function_ev, affinity_ev)
    return richardson_constant(effective_mass) * temperature_k ** 2 * math.exp(
        -barrier / (BOLTZMANN_EV * temperature_k)
    )
