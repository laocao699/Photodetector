# 1D PN diode electro-thermal simulation: transfer the HEMT electro-thermal
# method (temperature variable + temperature-dependent models + Wachutka heat
# generation + heat-conduction equation + thermal boundary) to a silicon diode.
from ZLsimple_physics import *
from devsim import *
import sys, os
import numpy as np

device = "MyDevice"
region = "MyRegion"

# ---- 1D mesh (same as examples/diode/diode_common.CreateMesh) ----
create_1d_mesh(mesh="dio")
add_1d_mesh_line(mesh="dio", pos=0, ps=1e-7, tag="top")
add_1d_mesh_line(mesh="dio", pos=0.5e-5, ps=1e-9, tag="mid")
add_1d_mesh_line(mesh="dio", pos=1e-5, ps=1e-7, tag="bot")
add_1d_contact(mesh="dio", name="top", tag="top", material="metal")
add_1d_contact(mesh="dio", name="bot", tag="bot", material="metal")
add_1d_region(mesh="dio", material="Si", region=region, tag1="top", tag2="bot")
finalize_mesh(mesh="dio")
create_device(mesh="dio", device=device)

# ---- parameters ----
SetSiliconParameters(device, region)
set_parameter(device=device, region=region, name="T", value=300.0)            # reference temp for mobility
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

# ---- doping ----
CreateNodeModel(device, region, "Acceptors", "1.0e18*step(0.5e-5-x)")
CreateNodeModel(device, region, "Donors", "1.0e18*step(x-0.5e-5)")
CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")

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
CreateMobilityModels(device, region, "mu_n", "mu_p")   # creates mu_nT, mu_pT (T-dependent)
CreateSiliconDriftDiffusion(device, region, mu_n="mu_nT", mu_p="mu_pT")
for c in get_contact_list(device=device):
    CreateSiliconDriftDiffusionAtContact(device, region, c)
solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

# ---- isothermal ramp 0 -> 0.7 V (fine steps) ----
def total_current():
    return (get_contact_current(device=device, contact="top", equation=ece_name)
            + get_contact_current(device=device, contact="top", equation=hce_name))

v = 0.0
while v < 0.701:
    set_parameter(device=device, name=GetContactBiasName("top"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    print("isothermal V=%.2f J=%.6e" % (v, total_current()))
    v += 0.1

# ---- electro-thermal coupling ----
CreateSiThermalConductivity(device, region)
CreateThermoelectricPowers(device, region)

# rigorous positive-definite Joule heat (|Jn|^2/(q mu_n n) + |Jp|^2/(q mu_p p)),
# same form as the HEMT GaN version but with the temperature-dependent silicon
# mobility mu_nT / mu_pT.  (The author's CreateJouleHeatSilicon uses the J.E
# form, which is negative in diffusion-dominated regions.)
edge_average_model(device=device, region=region, edge_model="edgeElectrons", node_model="Electrons")
edge_average_model(device=device, region=region, edge_model="edgeHoles", node_model="Holes")
_JouleHeat = "ElectronCurrent*ElectronCurrent/(mu_nT*ElectronCharge*edgeElectrons) + HoleCurrent*HoleCurrent/(mu_pT*ElectronCharge*edgeHoles)"
CreateEdgeModel(device, region, "JouleHeat", _JouleHeat)
for _v in ("Potential", "Electrons", "Holes", "Temperature"):
    CreateEdgeModelDerivatives(device, region, "JouleHeat", _JouleHeat, _v)

CreateRecombinationHeatSilicon(device, region)
CreatePJTheatSilicon(device, region)

# combined Wachutka heat source (Joule + recombination + Peltier-Thomson)
# Jacobian built from Joule + recombination (both have derivatives); PT frozen.
Heatsource = "JouleHeat + Recomheat + PJTheat"
CreateEdgeModel(device, region, "Heatsource", Heatsource)
for vv in ("Potential", "Electrons", "Holes", "Temperature"):
    CreateEdgeModel(device, region, "Heatsource:%s@n0" % vv, "JouleHeat:%s@n0 + Recomheat:%s@n0" % (vv, vv))
    CreateEdgeModel(device, region, "Heatsource:%s@n1" % vv, "JouleHeat:%s@n1 + Recomheat:%s@n1" % (vv, vv))

CreateTemperaturefield(device, region)
# thermal boundary: both contacts fixed at 300 K
for c in get_contact_list(device=device):
    set_parameter(device=device, name=GetContactTemperatureName(c), value=300.0)
    CreateTemperatureboundary(device, region, c)

print("=== solving coupled electro-thermal system ===")
solve(type="dc", absolute_error=1e10, relative_error=1e-8, maximum_iterations=500)

# ---- report ----
x = np.array(get_node_model_values(device=device, region=region, name="x"))
T = np.array(get_node_model_values(device=device, region=region, name="Temperature"))
print("Temperature: min=%.4f K  max=%.4f K  rise=%.4f K" % (T.min(), T.max(), T.max()-300.0))
print("Isothermal-vs-coupled Id: (see above ramp)")

for h in ("JouleHeat", "Recomheat", "PJTheat", "PJT_pos", "PJT_neg"):
    vv = np.array(get_edge_model_values(device=device, region=region, name=h))
    print("%-10s peak_abs=%.3e  peak=%.3e  mean=%.3e" % (h, np.abs(vv).max(), vv.max(), vv.mean()))

# temperature vs x
for xi, ti in zip(x, T):
    print("T(%.3e)=%.5f" % (xi, ti))
write_devices(file="diode_1d_electrothermal", type="tecplot")
print("diode electro-thermal done")
