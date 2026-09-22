# DEVSIM optical/optoelectronic physics layer.
#
# Extends the isothermal silicon drift-diffusion model of
# devsim.python_packages.simple_physics with a photo-generation source term.
#
# The continuity equations in DEVSIM are assembled as
#     d(time_node_model)/dt + div(edge_model) + node_model = 0
# For the standard SRH model simple_physics uses
#     Gn = -q*USRH ,  Gp = +q*USRH           (USRH = net recombination > 0)
# Photo-generation adds carriers with the opposite sign of recombination, so
#     Gn = -q*USRH + q*Gopt
#     Gp = +q*USRH - q*Gopt
# where Gopt [cm^-3 s^-1] is the (fixed) optical generation rate node model.
#
# This module is self-contained and importable from a driver run inside this
# directory (drivers add the phase5 root to sys.path).

import numpy as np

from devsim import (
    get_contact_current,
    get_node_model_values,
    set_node_values,
)
from devsim.python_packages.model_create import (
    CreateNodeModel,
    CreateNodeModelDerivative,
    InNodeModelList,
)
from devsim.python_packages.simple_physics import (
    CreateBernoulli,
    CreateECE,
    CreateHCE,
    CreatePE,
    CreateSiliconDriftDiffusionAtContact,  # re-exported
    CreateSiliconPotentialOnly,
    CreateSiliconPotentialOnlyContact,
    GetContactBiasName,
    SetSiliconParameters,
    ece_name,
    hce_name,
)

import optics  # noqa: F401  (ensures the package is importable)
from optics.generation import beer_lambert_G

__all__ = [
    "SetSiliconParameters",
    "CreateSiliconPotentialOnly",
    "CreateSiliconPotentialOnlyContact",
    "CreateSiliconDriftDiffusionAtContact",
    "GetContactBiasName",
    "CreateBernoulli",
    "CreateECE",
    "CreateHCE",
    "CreatePE",
    "EnsureOpticalGenerationModel",
    "SetOpticalGeneration",
    "SetDarkGeneration",
    "ApplyBeerLambert",
    "CreateSRHWithOptical",
    "CreateSiliconDriftDiffusionOptical",
    "TotalContactCurrent",
    "RegionMeanGeneration",
    "ece_name",
    "hce_name",
]


def EnsureOpticalGenerationModel(device, region):
    """Create the fixed photo-generation node model (default 0 => dark)."""
    if not InNodeModelList(device, region, "OpticalGeneration"):
        CreateNodeModel(device, region, "OpticalGeneration", "0.0")


def SetOpticalGeneration(device, region, values):
    """Set photo-generation [cm^-3 s^-1] per node from an array-like."""
    EnsureOpticalGenerationModel(device, region)
    set_node_values(device=device, region=region, name="OpticalGeneration",
                    values=np.asarray(values, dtype=float))


def SetDarkGeneration(device, region):
    """Zero the photo-generation model (dark conditions)."""
    nodes = len(get_node_model_values(device=device, region=region,
                                      name="NodeVolume"))
    SetOpticalGeneration(device, region, np.zeros(nodes))


def ApplyBeerLambert(device, region, wavelength_nm, Phi0, alpha_cm=None,
                     reflectance=0.0, depth_cm=None, coord_name="x",
                     surface_position=0.0, direction=1.0, mask=None,
                     eta_int=1.0, back_reflectance=0.0, thickness_cm=None):
    """Compute and install a Beer-Lambert generation profile on the mesh.

    Depth is taken from the mesh coordinate ``coord_name`` via
    depth = direction * (coord - surface_position) unless ``depth_cm`` is
    supplied explicitly.  ``mask`` is an optional boolean array selecting the
    nodes where generation is applied (e.g. only the depleted absorber).

    ``back_reflectance`` / ``thickness_cm`` enable a second (reflected) pass.

    Returns the applied G array [cm^-3 s^-1].
    """
    if depth_cm is None:
        coord = np.asarray(
            get_node_model_values(device=device, region=region, name=coord_name),
            dtype=float,
        )
        depth_cm = direction * (coord - surface_position)

    G = beer_lambert_G(depth_cm, wavelength_nm, Phi0, alpha_cm=alpha_cm,
                       reflectance=reflectance, eta_int=eta_int,
                       back_reflectance=back_reflectance,
                       thickness_cm=thickness_cm)
    if mask is not None:
        G = np.where(np.asarray(mask, dtype=bool), G, 0.0)
    SetOpticalGeneration(device, region, G)
    return G


def CreateSRHWithOptical(device, region):
    """SRH recombination plus a photo-generation source in both continuity eqs."""
    EnsureOpticalGenerationModel(device, region)

    USRH = "(Electrons*Holes - n_i^2)/(taup*(Electrons + n1) + taun*(Holes + p1))"
    Gn = "-ElectronCharge*USRH + ElectronCharge*OpticalGeneration"
    Gp = "+ElectronCharge*USRH - ElectronCharge*OpticalGeneration"

    CreateNodeModel(device, region, "USRH", USRH)
    CreateNodeModel(device, region, "ElectronGeneration", Gn)
    CreateNodeModel(device, region, "HoleGeneration", Gp)

    for v in ("Electrons", "Holes"):
        CreateNodeModelDerivative(device, region, "USRH", USRH, v)
        # the optical term does not depend on the solution variables, so its
        # Jacobian contribution is exactly zero
        CreateNodeModelDerivative(device, region, "ElectronGeneration",
                                  "-ElectronCharge*USRH", v)
        CreateNodeModelDerivative(device, region, "HoleGeneration",
                                  "+ElectronCharge*USRH", v)


def CreateSiliconDriftDiffusionOptical(device, region, mu_n="mu_n", mu_p="mu_p"):
    """Full potential + electron/hole continuity system with optical generation.

    Call this *instead of* simple_physics.CreateSiliconDriftDiffusion so that
    the continuity equations include the OpticalGeneration node model.
    """
    CreatePE(device, region)
    CreateBernoulli(device, region)
    CreateSRHWithOptical(device, region)
    CreateECE(device, region, mu_n)
    CreateHCE(device, region, mu_p)


def TotalContactCurrent(device, contact):
    """Total terminal current = electron + hole contact current [A/cm]."""
    return (
        get_contact_current(device=device, contact=contact, equation=ece_name)
        + get_contact_current(device=device, contact=contact, equation=hce_name)
    )


def RegionMeanGeneration(device, region):
    """Volume-weighted mean photo-generation rate [cm^-3 s^-1]."""
    G = np.asarray(get_node_model_values(device=device, region=region,
                                         name="OpticalGeneration"), dtype=float)
    V = np.asarray(get_node_model_values(device=device, region=region,
                                         name="NodeVolume"), dtype=float)
    return float(np.sum(G * V) / np.sum(V))
