# Phase 5 报告：基于开源 DEVSIM 的 Si PIN 光电二极管仿真与可复现流程

> 目标：用开源 TCAD（DEVSIM 2.10）实现一个光电传感器仿真，复现文献 golden 数据，
> 并沉淀一套可复现的光电器件仿真方法与流程。
> 基准：Roger et al., *Systematic Electro-Optical Study of Photodiodes in
> Intrinsic Material…*, MDPI Proceedings 2018, 2, 909（doi:10.3390/proceedings2130909）。
> 结论：**关键指标复现成功**——30 µm 器件响应度 0.610 A/W @800 nm（文献 0.63，差 3.2%），
> 漏电 3.58 pA @1 V（文献 3.5–10 pA），QE@750 nm=95%（文献 ~100%）；方法学模板见
> `METHOD_TEMPLATE.md`。

---

## 1. 背景与工具选型

DEVSIM 是开源（Apache-2.0）有限体积 TCAD，支持 Python 脚本、用户自定义 PDE/节点模型、
gmsh 导入、DC/AC/瞬态。**其本身没有光学模型**，因此本工作的核心是自建光学生成模块并
注入漂移-扩散连续性方程。

选型对比（简述）：OghmaNano 内置光学但偏 GUI；Charon 无光学且接入成本高；FEniCSx 需从零
写 DD。DEVSIM 与本仓库 Phase 1–4（二极管/BJT/电热）同源，可复用其收敛与验证范式，故选之。

---

## 2. 物理模型与实现

### 2.1 光学模块
- `optics/absorption.py`：Si@300K 的 $\alpha(\lambda)$、$n(\lambda)$ 查表（Green 1995/2008）
  与 Fresnel 反射。
- `optics/generation.py`：Beer-Lambert 光生率，支持前反射 $R$、背反射 $R_b$（二次程）、
  内量子产率；并提供理想光电流/EQE 解析式用于验证。

### 2.2 注入连续性方程
在 `simple_physics` 的 SRH 基础上扩展（`physics/optical_physics.py`）：
```
ElectronGeneration = -q*USRH + q*OpticalGeneration
HoleGeneration     = +q*USRH - q*OpticalGeneration
```
`OpticalGeneration` 为固定节点模型（与解变量无关，Jacobian 贡献为 0）。
符号与单位先由 1D 解析解锁定（见 §3.1）。

### 2.3 器件与数值
- 2D **轴对称（柱坐标，x=半径，y=深度）** 365 µm 圆形 PIN：浅 n⁺ 阱 / p⁻ iEPI
  （400 Ω·cm，$N_A\approx3.3\times10^{13}$ cm⁻³，20/30 µm）/ p⁺ 衬底（$10^{19}$）。
- 轻掺杂 → 启用 `extended_solver/model/equation`。
- 光照与偏压均**斜坡加载**；电容用**电路耦合接触 + SSAC** 提取。

---

## 3. 结果

### 3.1 P5.1 — 1D 解析验证（光学符号/单位锁定）
全耗尽 1D PIN（i 区 5 µm，λ=800 nm，Φ₀=1 mW/cm²，反偏 −5 V）：

| 量 | 值 (A/cm²) |
|---|---|
| 仿真空穴/电子光电流 $I_{illum}-I_{dark}$ | 2.1600×10⁻⁴ |
| 网格积分目标 $q\sum G\,V$ | 2.1662×10⁻⁴ |
| 闭式 Beer-Lambert | 2.1659×10⁻⁴ |
| 相对误差（仿真 vs 积分） | **−0.283 %** |

→ 光生率符号、单位与“全收集”假设正确，光学模块可用。
（暗电流 −3.31×10⁻¹³ A/cm²，i 区电子浓度 2.6×10⁴ ≪ 10¹⁴，确认全耗尽。）

### 3.2 P5.2 — 暗特性（2D 轴对称）

在 τ=10⁻⁴ s 下（见 §3.4 标定）：

| 器件 | $I_{dark}$@1 V | C@1 V | C@5 V | $C_{plate}=\varepsilon A/t_{epi}$ |
|---|---|---|---|---|
| 20 µm iEPI | **3.584 pA** | 1.395 pF | 0.722 pF | 0.542 pF |
| 30 µm iEPI | **3.590 pA** | 1.395 pF | 0.722 pF | 0.361 pF |

- 漏电与文献 3.5–10 pA 一致；
- C 随反压单调下降并趋近 $\varepsilon A/t_{epi}$ 极限；
- 20/30 µm 在 ≤5 V 的 C 相同，因为此时 $W_{dep}<t_{epi}$（未全耗尽），属正确物理。
- 暗 I-V 单调、阴极/阳极电流 KCL 严格闭合（残差 0）。

### 3.3 P5.3 — 光谱响应度与 EQE（复现文献）

| 指标 | 本工作 | Roger 2018 |
|---|---|---|
| 30 µm：R@800 nm | **0.610 A/W** | 0.63 A/W |
| 30 µm：EQE@750 nm | **95.0 %** | ~100 % |
| 30 µm：EQE@900 nm | **82.9 %** | 接近 100 %（定性） |
| 20 µm：R@800 nm | 0.586 A/W | — |
| 20 µm：EQE@750 nm | 92.9 % | ~100 % |
| 裸硅（无 BARC）30 µm：R@800 nm | 0.422 A/W | —（BARC 显著增益） |

- 峰值波长 ~800–825 nm、长波截止趋势、BARC 增益、厚度增溢均与文献一致；
- 绝对误差：R@800 nm 低约 3.2%（源于集电极效率 <100% 与背反射假设）。

### 3.4 P5.4 — 参数标定与扫描
- **寿命标定漏电**：$I_{gen}$ 与 $1/\tau$ 成正比。$\tau=10^{-3}$ s → 0.38 pA；
  $\tau=10^{-4}$ s → 3.58 pA，与文献 3.5 pA 匹配。
- **厚度**：20→30 µm 使 NIR 响应上升（吸收更充分）。
- **BARC**：前反射 0.03 vs 裸硅 Fresnel（~0.30）→ 响应度提升 ~45%。
- 图：`analysis/fig_spectral.png`、`analysis/fig_dark.png`。

---

## 4. 讨论与局限

1. **蓝光响应偏低**：本工作 400–425 nm EQE≈20–30%，文献 425 nm 约 72–82%。
   原因是欧姆接触钉扎表面载流子，形成较厚的“死层”，而模型未含表面钝化/表面复合工程。
   对 NIR 主指标无影响。
2. **背反射假设**：采用理想背反射（$R_b=1$）解释文献近 100% 的 750 nm QE；
   真实 wafer 背面反射率应作为参数标定。
3. **柱坐标体积离散**：`CylindricalNodeVolume` 径向 O(1/nx) 收敛，nx=16 时误差 ~2%，
   否则会虚增总光生使 EQE>100%（已在 `METHOD_TEMPLATE.md` 记录并处理）。
4. **无 Auger/带隙窄化/隧穿**：当前仅 SRH，重掺杂区电流未含这些机制。

---

## 5. 交付物与复现

```
work/phase5_photodetector/
├── optics/{absorption,generation}.py
├── physics/optical_physics.py
├── device/{pin2d,pin2d_device}.py
├── drivers/{pd_pn_1d,pd_pin_2d_dark,pd_pin_2d_photo}.py
├── analysis/plot_results.py  + fig_spectral.png / fig_dark.png
├── METHOD_TEMPLATE.md        # 可复现光电器件 TCAD 流程
└── REPORT_p5.md              # 本报告
```

复现命令（在 `work/phase5_photodetector/` 下）：
```
python3 drivers/pd_pn_1d.py                 # P5.1 解析验证
python3 drivers/pd_pin_2d_dark.py 20 1e-4   # P5.2 暗 I-V / C-V
python3 drivers/pd_pin_2d_dark.py 30 1e-4
python3 drivers/pd_pin_2d_photo.py 20 1e-3 5   # P5.3 光谱（BARC/裸硅）
python3 drivers/pd_pin_2d_photo.py 30 1e-3 5
python3 analysis/plot_results.py            # P5.4 出图
```

---

## 6. 结论

- 在**无内置光学**的开源 DEVSIM 上，成功搭建了“光学吸收 → 载流子产生 → 漂移扩散 →
  器件指标”的完整光电仿真链路，并以 1D 解析解（0.28%）与 2D 文献 golden 数据
  （R@800 nm 误差 3.2%、漏电一致）双重验证。
- 沉淀出可迁移的 **`METHOD_TEMPLATE.md`**：换器件只需替换几何/掺杂/材料光学常数，
  求解与验证框架（斜坡加载、扩展精度、SSAC 电容、能量/KCL 校验）保持不变。

---

## 7. 本次复核（devsim 2.10.0 端到端重跑）

全部驱动 `exit=0`，关键指标与本报告逐位一致：1D 解析误差 **−0.283%**；暗电流 @1V
3.584 pA(20µm)/3.590 pA(30µm)；R@800nm 0.586(20µm)/0.610(30µm) A/W；EQE@750nm
92.9%/95.0%；C_plate 0.542/0.361 pF、C@1V 1.395 pF；能量守恒 EQE≤100% 与 KCL 均满足。
代码审查未发现缺陷（分层清晰，单位/插值边界 clamp/扩展精度/双斜坡/SSAC 电容均正确）。
一键复现：`bash work/tools/run_phase.sh 5`；全项目审查见 `../REVIEW_REPORT.md`。
