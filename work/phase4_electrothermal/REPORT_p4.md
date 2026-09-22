# 电热耦合方法可迁移性验证报告

> 目标：把 HEMT 中验证过的电热耦合方法（温度变量 + 温度相关模型 + Wachutka 三项热产生 + 热传导方程 + 热边界）移植到 devsim_testing 下已跑通的硅器件上，验证其在**不同器件**上能否收敛。
> 结论：**方法成功移植，在 1D 硅二极管和 2D 硅 BJT 上均收敛**。发现并修正了原 silicon Joule 热公式的符号问题。

---

## 1. 方法移植方式

复用 `HEMT-simulation/work/` 的 `ZLsimple_physics.py` + `ZLsimple_dd.py`（作者已写好的 silicon 电热函数，即 SOI-MOS 论文函数），在 `devsim_testing/work/phase4_electrothermal/` 中写两个新电热驱动：

- `diode_1d_electrothermal.py`：1D PN 二极管（465 节点，top/bot 接触）
- `bjt_electrothermal.py`：2D 硅 BJT（bjt.msh 13777 节点，base/emitter/collector 三接触）

每个驱动流程与 HEMT `electrothermal.py` 同构：
网格/掺杂 → `SetSiliconParameters`（补设 `T=300`、`initialTemperature=300`）→ `Temperature` 变量 + `edgeTemp` → 温度相关热电压 `V_t_T`/`edgeV_t_T` → 温度相关 `CreateSiliconPotentialOnly` → `CreateMobilityModels`(μ(T)) + `CreateSiliconDriftDiffusion`(mu_nT/mu_pT) → 等温斜坡 → `CreateSiThermalConductivity` + `CreateThermoelectricPowers` + 三项热产生 + 组合热源 → `CreateTemperaturefield` + 三接触 300K 热边界 → 耦合求解。

## 2. 关键发现：原 silicon Joule 热公式有符号问题

作者 `ZLsimple_physics.py` 的 `CreateJouleHeatSilicon` 用 `JouleHeat = ElectricField * (ElectronCurrent + HoleCurrent)`（J·E 形式），在**扩散主导区**给出负值（载流子逆场扩散），导致净热源为负、温度场无法升温（diode 首次运行 mean=−3.35×10⁶ W/cm³，全为冷却）。

**修正**：改用严格正定的形式（与 HEMT GaN 版一致，仅把迁移率换成温度相关的 mu_nT/mu_pT）：

$$\text{JouleHeat} = \frac{J_n^2}{q\mu_n n} + \frac{J_p^2}{q\mu_p p}$$

修正后 Joule 热恒为正。此修正已写入驱动脚本，未改动拷贝的模块本体。

## 3. 结果

### 3.1 收敛性（核心验证目标）

| 器件 | 维度 | 方程数 | 耦合求解 | 结果 |
|---|---|---|---|---|
| PN 二极管 | 1D | 4 方程 × 465 节点 | 2 次 Newton 至 RelError 5.7×10⁻¹⁴ | ✅ 收敛 |
| BJT | 2D | 4 方程 × 13777 节点 | extended 精度，耦合收敛至 1e-8（约 83s） | ✅ 收敛 |

热传导方程（`HeatconductionEquation`）在两次迭代中均正常收敛（diode RelError 2.6×10⁻¹⁵），确认温度场被真正联立求解。

### 3.2 热产生分解（与论文量级关系一致）

| 器件 | Joule 峰值/均值 (W/cm³) | 复合热 峰值 (W/cm³) | PT 热 峰值/均值 (W/cm³) |
|---|---|---|---|
| 二极管 (V=0.7) | 2.67×10⁷ / 1.95×10⁵ | 7.4×10³ | 2.9×10⁸ / −8.2×10⁵ |
| BJT (Vbe=0.8) | 2.50×10⁷ / 6.96×10⁵ | 5.1×10⁴ | 2.4×10⁷ / −2.77×10⁵ |

结论与论文一致：**Joule 主导（恒正）→ 复合热小（≈Joule 均值的 0.2%）→ PT 热峰值与 Joule 同量级但正负交替、净抵消**（BJT 的 PJT 均值 −2.77×10⁵，正负部分大体相消）。

### 3.3 温度场

| 器件 | 温升 | 热点位置 |
|---|---|---|
| 二极管 | ≈1.6 µK（8 位精度显示 0） | 结区 |
| BJT | **14 mK**（max 300.014 K） | 发射极-基区结（x≈18.8µm，y≈1.58µm），电流密度最高处 |

温度场物理正确：从热点向 300K 热边界平滑衰减，热点位于电流密度最大的结区（BJT 的 emitter-base 结）。

### 3.4 等温 vs 电热 IV

BJT 在 Vbe=0.8 处：等温 Ic=0.32118 A/cm，电热 Ic=0.32126 A/cm（差 0.024%，在收敛容差内）。温升 14 mK 对应的迁移率退化仅 −2.2×0.014/300≈0.01%，小于求解容差，属数值噪声——物理上符合预期。

## 4. 物理解读：为何温升远小于 HEMT/SOI-MOS

温升 $\Delta T \approx P_{\text{surface}}\cdot L/\kappa$。**体硅热导率高**（κ_Si=1.48 W/cm·K），且这两例器件为纳米/微米尺度：

- 二极管：厚 100 nm，双端 300K 热沉，热阻≈0 → 温升 µK 级；
- BJT：~20 µm，在 Ic=0.32 A/cm（Vbe=0.8）下温升仅 14 mK。

对比：SOI-MOS 论文 140K 温升来自**埋氧层**（κ_SiO2=0.014，比 Si 低 100×）的热障；HEMT 2.3K 来自 2DEG 局部高功率密度。这说明**方法收敛性与温升大小无关**——温升由器件热阻决定，是物理量级问题而非耦合方法的失效。

## 5. 结论

1. **方法可迁移**：同一套电热耦合代码（复用 `ZLsimple` silicon 电热函数）在 1D PN 二极管和 2D BJT 上均**收敛**，与 HEMT（GaN 异质结）形成"不同材料、不同结构、不同维度"的交叉验证。
2. **移植要点全部适用**：温度变量、温度相关 V_t/迁移率/热导、Wachutka 三项热产生、热传导方程、热边界——各环节在硅器件上无需改动即可复用。
3. **修正了一个模型缺陷**：原 silicon Joule 热用 J·E 形式在扩散区出负值，应改用严格正定的 $J^2/(q\mu n)$ 形式（与 GaN 版统一）。

## 交付物（`devsim_testing/work/phase4_electrothermal/`）

| 文件 | 内容 |
|---|---|
| `diode_1d_electrothermal.py` / `diode.log` | 1D 二极管电热驱动 + 运行日志 |
| `bjt_electrothermal.py` / `bjt.log` | 2D BJT 电热驱动 + 运行日志 |
| `plot_temperature.py` / `bjt_temperature.png` | 温度场提取与 2D 温度分布图 |
| `ZLsimple_physics.py` / `ZLsimple_dd.py` / `bjt.msh` / `netdoping.py` / `read_gmsh.py` | 复用的模块与器件资源 |
| `REPORT_p4.md` | 本报告 |

---

## 6. 本次复核（devsim 2.10.0 端到端重跑）

- 1D 二极管与 2D BJT 电热驱动均 `exit=0` 收敛，关键量与本报告逐位一致：
  二极管 RelError 5.75e-14、Joule peak 2.67e7 / mean 1.95e5（恒正）；
  BJT 耦合 RelError 9.6e-10、温升 **14.3 mK**、等温 vs 电热 Ic 差 **0.024%**、
  Joule peak 2.50e7 / mean 6.96e5、PT peak 2.4e7 / mean −2.77e5。
- `CreateJouleHeatSilicon`（旧 `J·E` 形式）经核实为**死代码**（两驱动均内联正定形式，
  从不调用它），已在 `ZLsimple_physics.py` 加警示注释消除误用隐患；驱动内正定 Joule 热不变。
- 一键复现：`bash work/tools/run_phase.sh 4`；全项目审查见 `../REVIEW_REPORT.md`。
