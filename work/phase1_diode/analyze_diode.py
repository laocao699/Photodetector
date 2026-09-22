import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from devsim import (
    solve,
    set_parameter,
    get_node_model_values,
    get_edge_model_values,
    edge_average_model,
    write_devices,
)
from devsim.python_packages.simple_physics import GetContactBiasName, PrintCurrents
import diode_common

device = "MyDevice"
region = "MyRegion"

diode_common.CreateMesh(device=device, region=region)
diode_common.SetParameters(device=device, region=region)
set_parameter(device=device, region=region, name="taun", value=1e-8)
set_parameter(device=device, region=region, name="taup", value=1e-8)
diode_common.SetNetDoping(device=device, region=region)

# step 1: potential-only solve
diode_common.InitialSolution(device, region)
solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

# step 2: add drift-diffusion, equilibrium solve
diode_common.DriftDiffusionInitialSolution(device, region)
solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

# node models: position, doping, carriers, potential
x = np.array(get_node_model_values(device=device, region=region, name="x"))
NetDoping = np.array(get_node_model_values(device=device, region=region, name="NetDoping"))
Donors = np.array(get_node_model_values(device=device, region=region, name="Donors"))
Acceptors = np.array(get_node_model_values(device=device, region=region, name="Acceptors"))

# edge models: electric field and currents (edge midpoint positions)
edge_average_model(device=device, region=region, node_model="x", edge_model="xmid")
edge_x = np.array(get_edge_model_values(device=device, region=region, name="xmid"))
EField = np.array(get_edge_model_values(device=device, region=region, name="ElectricField"))
Jn = np.array(get_edge_model_values(device=device, region=region, name="ElectronCurrent"))
Jp = np.array(get_edge_model_values(device=device, region=region, name="HoleCurrent"))

# --- 平衡态 (V=0) 数值验证：把 REPORT 的验证表落成可复跑的 PASS/FAIL 判据 ---
# 此时尚未进入偏压扫描，Potential/Electrons/Holes/EField 均为热平衡值。
_q = 1.602176634e-19      # C
_kb = 1.380649e-23        # J/K
_T = 300.0                # K (diode_common.SetParameters -> SetSiliconParameters(300))
_Vt = _kb * _T / _q       # 热电压 ~0.02585 V
_ni = 1.0e10              # 硅本征载流子浓度 (devsim 默认)
_NA = float(np.max(Acceptors))
_ND = float(np.max(Donors))
_Vbi_theory = _Vt * np.log(_NA * _ND / _ni**2)

Potential_eq = np.array(get_node_model_values(device=device, region=region, name="Potential"))
Electrons_eq = np.array(get_node_model_values(device=device, region=region, name="Electrons"))
Holes_eq = np.array(get_node_model_values(device=device, region=region, name="Holes"))
_Vbi = float(Potential_eq.max() - Potential_eq.min())
_np_prod = float(np.median(Electrons_eq * Holes_eq))
_Emax = float(np.max(np.abs(EField)))

_checks = []


def _check(name, got, expect, rtol, unit=""):
    ok = abs(got - expect) <= rtol * abs(expect)
    _checks.append(ok)
    flag = "PASS" if ok else "FAIL"
    print(f"[{flag}] {name}: {got:.5g}{unit}  (期望 {expect:.5g}{unit}, 容差 {rtol:.0%})")


print("=== Phase1 二极管 平衡态(V=0) 数值验证 ===")
print(f"[INFO] NA={_NA:.3g}  ND={_ND:.3g}  ni={_ni:.3g}  Vt={_Vt:.5g} V")
_check("内建电势 Vbi", _Vbi, _Vbi_theory, 0.02, " V")
_check("质量作用定律 n*p(中值)/ni^2", _np_prod, _ni**2, 0.05)
_check("结区最大电场 Emax", _Emax, 3.83e5, 0.25, " V/cm")

v_list, itot_list = [], []
v = 0.0
while v < 0.51:
    set_parameter(device=device, name=GetContactBiasName("top"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    PrintCurrents(device, "top")
    # re-read at each bias
    EField = np.array(get_edge_model_values(device=device, region=region, name="ElectricField"))
    Jn = np.array(get_edge_model_values(device=device, region=region, name="ElectronCurrent"))
    Jp = np.array(get_edge_model_values(device=device, region=region, name="HoleCurrent"))
    # total current is conserved along x (1D); use max abs as value
    itot = np.max(np.abs(Jn + Jp))
    v_list.append(v)
    itot_list.append(itot)
    v += 0.1

Electrons = np.array(get_node_model_values(device=device, region=region, name="Electrons"))
Holes = np.array(get_node_model_values(device=device, region=region, name="Holes"))
Potential = np.array(get_node_model_values(device=device, region=region, name="Potential"))

write_devices(file="diode_1d.dat", type="tecplot")

fig, ax = plt.subplots(2, 2, figsize=(12, 9))

# (a) IV curve (log scale)
ax[0, 0].semilogy(v_list, itot_list, "o-")
ax[0, 0].set_xlabel("Bias V (V)")
ax[0, 0].set_ylabel("|J| (A/cm^2)")
ax[0, 0].set_title("(a) Diode I-V (log)")

# (b) doping profile and carrier densities at V=0.5
ax[0, 1].semilogy(x, Donors, label="Donors")
ax[0, 1].semilogy(x, Acceptors, label="Acceptors")
ax[0, 1].semilogy(x, np.maximum(Electrons, 1), "--", label="Electrons")
ax[0, 1].semilogy(x, np.maximum(Holes, 1), "--", label="Holes")
ax[0, 1].set_xlabel("x (cm)")
ax[0, 1].set_ylabel("density (1/cm^3)")
ax[0, 1].set_title("(b) Doping & carriers at V=0.5")
ax[0, 1].legend()

# (c) potential and electric field
ax[1, 0].plot(x, Potential, label="Potential")
ax[1, 0].set_xlabel("x (cm)")
ax[1, 0].set_ylabel("Potential (V)")
ax[1, 0].set_title("(c) Potential at V=0.5")
ax[1, 0].twinx().plot(edge_x, EField, "r", label="E-field")
ax[1, 0].set_ylabel("E (V/cm)")

# (d) electron/hole currents (edge)
ax[1, 1].semilogy(edge_x, np.abs(Jn), label="J_n")
ax[1, 1].semilogy(edge_x, np.abs(Jp), label="J_p")
ax[1, 1].semilogy(edge_x, np.abs(Jn + Jp), "k", label="J_total")
ax[1, 1].set_xlabel("x (cm)")
ax[1, 1].set_ylabel("|J| (A/cm^2)")
ax[1, 1].set_title("(d) Current components at V=0.5")
ax[1, 1].legend()

plt.tight_layout()
plt.savefig("diode_1d_analysis.png", dpi=120)
print("saved diode_1d_analysis.png")

# --- IV 特性校验：0.5V 处 J 应与肖克莱指数特性一致(REPORT: 1.82e-2 A/cm^2) ---
_j05 = float(itot_list[-1])
_check("IV @V=0.5 电流密度 J", _j05, 1.82e-2, 0.10, " A/cm^2")

_nfail = _checks.count(False)
print("=" * 50)
if _nfail:
    print(f"=== Phase1 验证失败: {_nfail}/{len(_checks)} 项未通过 ===")
    sys.exit(1)
print(f"=== Phase1 验证通过: {len(_checks)}/{len(_checks)} 项全部 PASS ===")
