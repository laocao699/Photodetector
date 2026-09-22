from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SemiconductorMaterial:
    name: str
    bandgap_ev: float
    affinity_ev: float
    relative_permittivity: float
    nc_cm3: float
    nv_cm3: float
    electron_mobility_cm2_v_s: float
    hole_mobility_cm2_v_s: float
    electron_effective_mass: float
    hole_effective_mass: float
    saturation_velocity_cm_s: float
    donor_concentration_cm3: float

    def as_dict(self):
        return asdict(self)
