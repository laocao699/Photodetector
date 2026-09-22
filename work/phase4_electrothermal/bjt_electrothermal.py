# 2D BJT electro-thermal simulation: transfer the HEMT electro-thermal method
# to a silicon bipolar transistor (2D gmsh mesh, base/emitter/collector contacts).
from ZLsimple_physics import *
from devsim import *
import sys, os
import numpy as np

set_parameter(name="extended_solver", value=True)
set_parameter(name="extended_model", value=True)
set_parameter(name="extended_equation", value=True)

device = "bjt"
region = "bjt"

import read_gmsh
read_gmsh.run("bjt.msh", device, region, "Silicon", ("base", "collector", "emitter"))

import netdoping
netdoping.run(device, region)

# ---- parameters ----
SetSiliconParameters(device, region)
set_parameter(device=device, region=region, name="T", value=300.0)
set_parameter(device=device, name="initialTemperature", value=300.0)

# ---- temperature solution variable + edge model ----
CreateSolution(device, region, "Temperature")
CreateTinitial(device, region)
set_node_values(device=device, region=region, name="Temperature", init_from="Init_temperature")
edge_from_node_model(device=device, region=region, node_model="Temperature")
edge_average_model(device=device, region=region, edge_model="edgeTemp", node_model="Temperature")
edge_average_model(device=device, region=region, edge_model="edgeTemp", node_model="Temperature", derivative="Temperature")

# ---- temperature-dependent thermal voltage ----
node_model(device=device, region=region, name="V_t_T", equation="boltzmannConstant*Temperature/ElectronCharge")
node_model(device=device, region=region, name="V_t_T:Temperature", equation="boltzmannConstant/ElectronCharge")
edge_average_model(device=device, region=region, edge_model="edgeV_t_T", node_model="V_t_T")
edge_average_model(device=device, region=region, edge_model="edgeV_t_T", node_model="V_t_T", derivative="Temperature")

# ---- potential-only (temperature-aware) ----
CreateSiliconPotentialOnly(device, region)
for c in get_contact_list(device=device):
    CreateSiliconPotentialOnlyContact(device, region, c)
    set_parameter(device=device, name=GetContactBiasName(c), value=0.0)
solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

# ---- drift-diffusion (temperature-aware, temperature-dependent mobility) ----
CreateSolution(device, region, "Electrons")
CreateSolution(device, region, "Holes")
set_node_values(device=device, region=region, name="Electrons", init_from="IntrinsicElectrons")
set_node_values(device=device, region=region, name="Holes", init_from="IntrinsicHoles")
CreateMobilityModels(device, region, "mu_n", "mu_p")
CreateSiliconDriftDiffusion(device, region, mu_n="mu_nT", mu_p="mu_pT")
for c in get_contact_list(device=device):
    CreateSiliconDriftDiffusionAtContact(device, region, c)
solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

# ---- isothermal ramp to operating point: Vbe 0->0.8, Vce=1.0 ----
set_parameter(device=device, name="emitter_bias", value=0.0)
set_parameter(device=device, name="collector_bias", value=1.0)

def collector_current():
    return (get_contact_current(device=device, contact="collector", equation=ece_name)
            + get_contact_current(device=device, contact="collector", equation=hce_name))

vbe = 0.0
while vbe < 0.801:
    set_parameter(device=device, name="base_bias", value=vbe)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=50)
    print("isothermal Vbe=%.2f Ic=%.6e" % (vbe, collector_current()))
    vbe += 0.05

# ---- electro-thermal coupling ----
CreateSiThermalConductivity(device, region)
CreateThermoelectricPowers(device, region)

# rigorous positive-definite Joule heat (like the HEMT GaN version)
edge_average_model(device=device, region=region, edge_model="edgeElectrons", node_model="Electrons")
edge_average_model(device=device, region=region, edge_model="edgeHoles", node_model="Holes")
_JouleHeat = "ElectronCurrent*ElectronCurrent/(mu_nT*ElectronCharge*edgeElectrons) + HoleCurrent*HoleCurrent/(mu_pT*ElectronCharge*edgeHoles)"
CreateEdgeModel(device, region, "JouleHeat", _JouleHeat)
for _v in ("Potential", "Electrons", "Holes", "Temperature"):
    CreateEdgeModelDerivatives(device, region, "JouleHeat", _JouleHeat, _v)

CreateRecombinationHeatSilicon(device, region)
CreatePJTheatSilicon(device, region)

# combined Wachutka heat source (Joule + recombination + PT), Jacobian from Joule+Recomb
Heatsource = "JouleHeat + Recomheat + PJTheat"
CreateEdgeModel(device, region, "Heatsource", Heatsource)
for vv in ("Potential", "Electrons", "Holes", "Temperature"):
    CreateEdgeModel(device, region, "Heatsource:%s@n0" % vv, "JouleHeat:%s@n0 + Recomheat:%s@n0" % (vv, vv))
    CreateEdgeModel(device, region, "Heatsource:%s@n1" % vv, "JouleHeat:%s@n1 + Recomheat:%s@n1" % (vv, vv))

CreateTemperaturefield(device, region)
# thermal boundary: all three contacts fixed at 300 K
for c in get_contact_list(device=device):
    set_parameter(device=device, name=GetContactTemperatureName(c), value=300.0)
    CreateTemperatureboundary(device, region, c)

print("=== solving coupled electro-thermal system ===")
solve(type="dc", absolute_error=1e10, relative_error=1e-8, maximum_iterations=500)

# ---- report ----
T = np.array(get_node_model_values(device=device, region=region, name="Temperature"))
print("Temperature: min=%.4f K  max=%.4f K  rise=%.5f K" % (T.min(), T.max(), T.max()-300.0))
print("Ic (coupled) = %.6e A/cm" % collector_current())

for h in ("JouleHeat", "Recomheat", "PJTheat", "PJT_pos", "PJT_neg"):
    vv = np.array(get_edge_model_values(device=device, region=region, name=h))
    print("%-10s peak_abs=%.3e  peak=%.3e  mean=%.3e" % (h, np.abs(vv).max(), vv.max(), vv.mean()))

write_devices(file="bjt_electrothermal", type="tecplot")
print("BJT electro-thermal done")
