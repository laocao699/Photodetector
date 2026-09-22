"""Reusable wide-bandgap semiconductor physics helpers.

The device models intentionally build on DEVSIM's stable isothermal
Scharfetter-Gummel implementation. Material and contact equations are kept
generic; beta-Ga2O3 is the first calibrated material.
"""

import math

from materials.ga2o3 import BETA_GA2O3, BOLTZMANN_EV
from materials.contacts import schottky_barrier_ev

from devsim import contact_equation, get_node_model_values, set_node_values, set_parameter
from devsim.python_packages.model_create import (
    CreateContactNodeModel,
    CreateContactNodeModelDerivative,
    CreateEdgeModel,
    CreateEdgeModelDerivatives,
    CreateNodeModel,
    CreateNodeModelDerivative,
    CreateSolution,
    InEdgeModelList,
    InNodeModelList,
)
from devsim.python_packages.simple_physics import (
    CreateBernoulli,
    CreateECE,
    CreateHCE,
    CreatePE,
    GetContactBiasName,
)


EPSILON_0_F_CM = 8.8541878128e-14
ELECTRON_CHARGE_C = 1.602176634e-19
BOLTZMANN_J_K = 1.380649e-23


def schottky_equilibrium_densities(temperature_k, work_function_ev,
                                  material=BETA_GA2O3, barrier_ev=None):
    """Equilibrium n/p densities at an ideal n-type Schottky contact."""
    thermal_voltage = BOLTZMANN_EV * temperature_k
    if barrier_ev is None:
        barrier_ev = schottky_barrier_ev(work_function_ev, material.affinity_ev)
    electrons = material.nc_cm3 * math.exp(-barrier_ev / thermal_voltage)
    holes = material.nv_cm3 * math.exp(
        -(material.bandgap_ev - barrier_ev) / thermal_voltage
    )
    return electrons, holes


def richardson_constant_a_cm2_k2(effective_mass):
    """Effective Richardson constant A* [A cm^-2 K^-2]."""
    return 120.172 * effective_mass


def schottky_surface_velocities(temperature_k, material=BETA_GA2O3):
    """Thermionic-emission surface recombination velocities [cm/s].

    The convention mirrors the project's HEMT Schottky model:
        Jn = q*V_surfe*(Electrons-Electrons_eq)*ContactSurfaceArea/NodeVolume
    where v_surf,n = A*_n*T^2/Nc and v_surf,p = A*_p*T^2/Nv.  The resulting
    electron saturation flux is exactly q*A*T^2*exp(-Phi_B/Vt).
    """
    electron_velocity = (
        richardson_constant_a_cm2_k2(material.electron_effective_mass)
        * temperature_k ** 2 / material.nc_cm3
    )
    hole_velocity = (
        richardson_constant_a_cm2_k2(material.hole_effective_mass)
        * temperature_k ** 2 / material.nv_cm3
    )
    return electron_velocity, hole_velocity


def build_trap_list(temperature_k=300.0, material=BETA_GA2O3, traps=None):
    """Convert a trap table into the dict list used by create_drift_diffusion."""
    from materials.ga2o3 import trap_srh_parameters

    if traps is None:
        from materials.ga2o3 import GA2O3_TRAPS
        traps = GA2O3_TRAPS
    out = []
    for t in traps:
        sigma_p = t["sigma_n_cm2"] / t["sigma_n_over_p"]
        n1, p1, taun, taup = trap_srh_parameters(
            trap_depth_ev=t["Ec_minus_Et_ev"], Nt_cm3=t["Nt_cm3"],
            sigma_n_cm2=t["sigma_n_cm2"], sigma_p_cm2=sigma_p,
            temperature_k=temperature_k, material=material,
        )
        out.append({"n1_cm3": n1, "p1_cm3": p1, "taun_s": taun, "taup_s": taup})
    return out


def set_semiconductor_parameters(device, region, material=BETA_GA2O3,
                                 temperature_k=300.0, taun_s=1e-8,
                                 taup_s=1e-8):
    """Install electrical parameters expected by DEVSIM simple DD models."""
    from materials.ga2o3 import intrinsic_carrier_concentration

    ni = intrinsic_carrier_concentration(temperature_k, material)
    values = {
        "Permittivity": material.relative_permittivity * EPSILON_0_F_CM,
        "ElectronCharge": ELECTRON_CHARGE_C,
        "n_i": ni,
        "T": temperature_k,
        "kT": BOLTZMANN_J_K * temperature_k,
        "V_t": BOLTZMANN_J_K * temperature_k / ELECTRON_CHARGE_C,
        "mu_n": material.electron_mobility_cm2_v_s,
        "mu_p": material.hole_mobility_cm2_v_s,
        "n1": ni,
        "p1": ni,
        "taun": taun_s,
        "taup": taup_s,
        "Eg": material.bandgap_ev,
        "Affinity": material.affinity_ev,
        "Nc": material.nc_cm3,
        "Nv": material.nv_cm3,
        "vsat": material.saturation_velocity_cm_s,
        "AugerCn": 0.0,
        "AugerCp": 0.0,
    }
    for name, value in values.items():
        set_parameter(device=device, region=region, name=name, value=value)


def create_potential_only(device, region, use_bgn=False):
    """Create equilibrium Poisson equation for an arbitrary semiconductor."""
    if not InNodeModelList(device, region, "Potential"):
        CreateSolution(device, region, "Potential")
    if use_bgn:
        # doping-dependent intrinsic concentration via band-gap narrowing
        CreateNodeModel(device, region, "BGN_deltaEg",
                        "bgn_coeff*log(max(1.0,abs(NetDoping)/bgn_nref))")
        CreateNodeModel(device, region, "n_i_eff",
                        "n_i*exp(BGN_deltaEg/(2*V_t))")
    models = (
        ("IntrinsicElectrons", "n_i*exp(Potential/V_t)"),
        ("IntrinsicHoles", "n_i^2/IntrinsicElectrons"),
        ("IntrinsicCharge", "kahan3(IntrinsicHoles,-IntrinsicElectrons,NetDoping)"),
        ("PotentialIntrinsicCharge", "-ElectronCharge*IntrinsicCharge"),
    )
    for name, expression in models:
        CreateNodeModel(device, region, name, expression)
        CreateNodeModelDerivative(device, region, name, expression, "Potential")
    for name, expression in (
        ("ElectricField", "(Potential@n0-Potential@n1)*EdgeInverseLength"),
        ("PotentialEdgeFlux", "Permittivity*ElectricField"),
    ):
        CreateEdgeModel(device, region, name, expression)
        CreateEdgeModelDerivatives(device, region, name, expression, "Potential")
    from devsim import equation

    equation(
        device=device,
        region=region,
        name="PotentialEquation",
        variable_name="Potential",
        node_model="PotentialIntrinsicCharge",
        edge_model="PotentialEdgeFlux",
        variable_update="log_damp",
    )


def _create_potential_contact(device, region, contact, electron_density_cm3):
    if not InEdgeModelList(device, region, "contactcharge_edge"):
        CreateEdgeModel(device, region, "contactcharge_edge", "Permittivity*ElectricField")
        CreateEdgeModelDerivatives(
            device, region, "contactcharge_edge", "Permittivity*ElectricField", "Potential"
        )
    name = f"{contact}_potential_bc"
    set_parameter(
        device=device,
        name=f"{contact}_electron_density",
        value=electron_density_cm3,
    )
    expression = (
        f"Potential-{GetContactBiasName(contact)}-"
        f"V_t*log({contact}_electron_density/n_i)"
    )
    CreateContactNodeModel(device, contact, name, expression)
    CreateContactNodeModel(device, contact, f"{name}:Potential", "1")
    contact_equation(
        device=device,
        contact=contact,
        name="PotentialEquation",
        node_model=name,
        edge_charge_model="contactcharge_edge",
    )


def create_ohmic_potential_contact(device, region, contact, donor_density_cm3):
    _create_potential_contact(device, region, contact, donor_density_cm3)


def create_schottky_potential_contact(device, region, contact, work_function_ev,
                                      material=BETA_GA2O3,
                                      temperature_k=300.0,
                                      barrier_ev=None):
    electrons, _ = schottky_equilibrium_densities(
        temperature_k, work_function_ev, material, barrier_ev=barrier_ev
    )
    set_parameter(device=device, name=f"{contact}_work_function", value=work_function_ev)
    if barrier_ev is not None:
        set_parameter(device=device, name=f"{contact}_barrier_ev", value=barrier_ev)
    _create_potential_contact(device, region, contact, electrons)


def ensure_optical_generation(device, region):
    if not InNodeModelList(device, region, "OpticalGeneration"):
        CreateNodeModel(device, region, "OpticalGeneration", "0")


def set_optical_generation(device, region, values):
    ensure_optical_generation(device, region)
    set_node_values(device=device, region=region, name="OpticalGeneration", values=values)


def set_dark_generation(device, region):
    count = len(get_node_model_values(device=device, region=region, name="NodeVolume"))
    set_optical_generation(device, region, [0.0] * count)


def create_recombination_with_optical(device, region, traps=None):
    """SRH + Auger + deep-level-trap recombination and optical generation.

    traps is a list of dicts with keys:
        Et_ev (Ec-Et), Nt_cm3, sigma_n_cm2, sigma_p_cm2, v_thn_cm_s, v_thp_cm_s
    When empty/None the model is identical to the un-trapped baseline.
    """
    ensure_optical_generation(device, region)
    srh = "(Electrons*Holes-n_i^2)/(taup*(Electrons+n1)+taun*(Holes+p1))"
    auger = (
        "AugerCn*(Electrons^2*Holes-Electrons*n_i^2)+"
        "AugerCp*(Electrons*Holes^2-Holes*n_i^2)"
    )

    terms = ["USRH", "UAuger"]
    if traps:
        for i, trap in enumerate(traps):
            tag = "T%d" % i
            set_parameter(device=device, region=region,
                          name=f"taun_{tag}", value=trap["taun_s"])
            set_parameter(device=device, region=region,
                          name=f"taup_{tag}", value=trap["taup_s"])
            set_parameter(device=device, region=region,
                          name=f"n1_{tag}", value=trap["n1_cm3"])
            set_parameter(device=device, region=region,
                          name=f"p1_{tag}", value=trap["p1_cm3"])
            expr = ("(Electrons*Holes-n_i^2)/(taup_{0}*(Electrons+n1_{0})"
                    "+taun_{0}*(Holes+p1_{0}))").format(tag)
            CreateNodeModel(device, region, f"UTrap{tag}", expr)
            for variable in ("Electrons", "Holes"):
                CreateNodeModelDerivative(device, region, f"UTrap{tag}", expr,
                                          variable)
            terms.append(f"UTrap{tag}")

    total = "+".join(terms)
    electron_source = "-ElectronCharge*NetRecombination+ElectronCharge*OpticalGeneration"
    hole_source = "ElectronCharge*NetRecombination-ElectronCharge*OpticalGeneration"
    CreateNodeModel(device, region, "USRH", srh)
    CreateNodeModel(device, region, "UAuger", auger)
    CreateNodeModel(device, region, "NetRecombination", total)
    CreateNodeModel(device, region, "ElectronGeneration", electron_source)
    CreateNodeModel(device, region, "HoleGeneration", hole_source)
    for variable in ("Electrons", "Holes"):
        CreateNodeModelDerivative(device, region, "USRH", srh, variable)
        CreateNodeModelDerivative(device, region, "UAuger", auger, variable)
        CreateNodeModelDerivative(device, region, "NetRecombination", total, variable)
        CreateNodeModelDerivative(
            device, region, "ElectronGeneration", "-ElectronCharge*NetRecombination", variable
        )
        CreateNodeModelDerivative(
            device, region, "HoleGeneration", "ElectronCharge*NetRecombination", variable
        )


def create_arora_mobility(device, region, n_ref_cm3=1.0e17, alpha=0.85):
    """Doping-dependent Arora mobility edge models.

    Produces mu_n_arora / mu_p_arora = mu_(n|p) / (1 + (N/Nref)^alpha), using
    edge-averaged |NetDoping|.  To use, pass mu_n="mu_n_arora" into
    create_drift_diffusion.
    """
    from devsim import edge_average_model, edge_from_node_model
    edge_from_node_model(device=device, region=region, node_model="NetDoping")
    edge_average_model(device=device, region=region,
                       edge_model="edgeNetDoping", node_model="NetDoping")
    nd = "abs(edgeNetDoping)"
    mu_n_expr = "mu_n/(1.0+(%s/%.6e)^%.6f)" % (nd, n_ref_cm3, alpha)
    mu_p_expr = "mu_p/(1.0+(%s/%.6e)^%.6f)" % (nd, n_ref_cm3, alpha)
    CreateEdgeModel(device, region, "mu_n_arora", mu_n_expr)
    CreateEdgeModel(device, region, "mu_p_arora", mu_p_expr)
    for var in ("Potential", "Electrons", "Holes"):
        pass  # doping-only model; no solution-variable derivatives needed


def create_drift_diffusion(device, region, mu_n="mu_n", mu_p="mu_p", traps=None,
                           use_arora=False):
    if use_arora:
        create_arora_mobility(device, region)
        mu_n, mu_p = "mu_n_arora", "mu_p_arora"
    CreatePE(device, region)
    CreateBernoulli(device, region)
    create_recombination_with_optical(device, region, traps=traps)
    CreateECE(device, region, mu_n)
    CreateHCE(device, region, mu_p)


def initialize_carriers(device, region):
    for name, source in (
        ("Electrons", "IntrinsicElectrons"),
        ("Holes", "IntrinsicHoles"),
    ):
        CreateSolution(device, region, name)
        set_node_values(device=device, region=region, name=name, init_from=source)


def _create_carrier_contact(device, contact, electron_density_cm3,
                            hole_density_cm3):
    set_parameter(device=device, name=f"{contact}_electrons_eq", value=electron_density_cm3)
    set_parameter(device=device, name=f"{contact}_holes_eq", value=hole_density_cm3)
    electron_name = f"{contact}_electrons_bc"
    hole_name = f"{contact}_holes_bc"
    electron_expression = f"Electrons-{contact}_electrons_eq"
    hole_expression = f"Holes-{contact}_holes_eq"
    CreateContactNodeModel(device, contact, electron_name, electron_expression)
    CreateContactNodeModel(device, contact, f"{electron_name}:Electrons", "1")
    CreateContactNodeModel(device, contact, hole_name, hole_expression)
    CreateContactNodeModel(device, contact, f"{hole_name}:Holes", "1")
    contact_equation(
        device=device,
        contact=contact,
        name="ElectronContinuityEquation",
        node_model=electron_name,
        edge_current_model="ElectronCurrent",
    )
    contact_equation(
        device=device,
        contact=contact,
        name="HoleContinuityEquation",
        node_model=hole_name,
        edge_current_model="HoleCurrent",
    )


def create_ohmic_carrier_contact(device, contact, donor_density_cm3,
                                 material=BETA_GA2O3,
                                 temperature_k=300.0):
    from materials.ga2o3 import intrinsic_carrier_concentration

    ni = intrinsic_carrier_concentration(temperature_k, material)
    _create_carrier_contact(device, contact, donor_density_cm3,
                            ni * ni / donor_density_cm3)


def create_schottky_carrier_contact(device, contact, work_function_ev,
                                    material=BETA_GA2O3,
                                    temperature_k=300.0,
                                    finite_surface_recombination=True,
                                    barrier_ev=None):
    electrons, holes = schottky_equilibrium_densities(
        temperature_k, work_function_ev, material, barrier_ev=barrier_ev
    )
    if not finite_surface_recombination:
        _create_carrier_contact(device, contact, electrons, holes)
        return

    electron_velocity, hole_velocity = schottky_surface_velocities(
        temperature_k, material
    )
    set_parameter(device=device, name=f"{contact}_electron_velocity",
                  value=electron_velocity)
    set_parameter(device=device, name=f"{contact}_hole_velocity",
                  value=hole_velocity)
    set_parameter(device=device, name=f"{contact}_electrons_eq", value=electrons)
    set_parameter(device=device, name=f"{contact}_holes_eq", value=holes)

    electron_name = f"{contact}_electrons_te"
    hole_name = f"{contact}_holes_te"
    electron_expression = (
        f"ElectronCharge*{contact}_electron_velocity*"
        f"(Electrons-{contact}_electrons_eq)*ContactSurfaceArea/NodeVolume"
    )
    hole_expression = (
        f"-ElectronCharge*{contact}_hole_velocity*"
        f"(Holes-{contact}_holes_eq)*ContactSurfaceArea/NodeVolume"
    )
    CreateContactNodeModel(device, contact, electron_name, electron_expression)
    CreateContactNodeModelDerivative(
        device, contact, electron_name, electron_expression, "Electrons"
    )
    CreateContactNodeModel(device, contact, hole_name, hole_expression)
    CreateContactNodeModelDerivative(
        device, contact, hole_name, hole_expression, "Holes"
    )
    contact_equation(
        device=device,
        contact=contact,
        name="ElectronContinuityEquation",
        node_model=electron_name,
        edge_current_model="ElectronCurrent",
    )
    contact_equation(
        device=device,
        contact=contact,
        name="HoleContinuityEquation",
        node_model=hole_name,
        edge_current_model="HoleCurrent",
    )
