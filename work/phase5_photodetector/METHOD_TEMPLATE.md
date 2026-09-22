# 光电器件 TCAD 仿真方法学模板（开源 DEVSIM）

> 本模板由 `work/phase5_photodetector/` 的 Si PIN 光电二极管实现提炼而来，可迁移到其他
> 光电探测/传感器器件（PIN/APD/MSM/异质结等）。核心难点是 **DEVSIM 无内置光学模型**，
> 需自建光学生成模块并注入连续性方程。

---

## 0. 方法总览（一句话）

> 用 Beer-Lambert（或多层 TMM）把入射光换算成按深度分布的光生率 $G_{opt}(x,\lambda)$，
> 作为一个**固定节点模型**注入电子/空穴连续方程的源项，再用漂移-扩散求解光照下的
> 终端电流，从而得到响应度、量子效率、暗电流、电容与带宽。

---

## 1. 物理与单位约定（务必先锁定）

| 量 | 符号 | DEVSIM 单位 |
|---|---|---|
| 长度 | x | cm |
| 掺杂 | N | cm⁻³ |
| 光生率 | $G_{opt}$ | cm⁻³ s⁻¹ |
| 入射光功率密度 | $\Phi_0$ | W cm⁻² |
| 吸收系数 | $\alpha$ | cm⁻¹ |
| 光子能量 | $h\nu=hc/\lambda$ | J |
| 载流子寿命 | $\tau_n,\tau_p$ | s |

**Beer-Lambert 光生率**（单色、垂直入射、深度 $d$）：

$$G_{opt}(d,\lambda)=\alpha(\lambda)\,\frac{(1-R(\lambda))\,\Phi_0}{h\nu}\,e^{-\alpha(\lambda)d}$$

含衬底背反射（二次程，$t=$ 吸收区厚度）时：

$$G_{opt}=\alpha\frac{(1-R)\Phi_0}{h\nu}\Big[e^{-\alpha d}+R_b\,e^{-\alpha(2t-d)}\Big]$$

**注入连续性方程（符号，已用 1D 解析验证）**：

```
ElectronGeneration = -q*USRH + q*OpticalGeneration
HoleGeneration     = +q*USRH - q*OpticalGeneration
```

其中 `OpticalGeneration` 是固定（与解变量无关）的节点模型，其 Jacobian 贡献为 0。

---

## 2. 可复现流程（固定步骤）

### 步骤 1 — 光学常数与吸收模型
- 建立 $\alpha(\lambda)$、$n(\lambda)$、$R(\lambda)$ 查表（本仓库 `optics/absorption.py`，Si@300K）。
- 多层/抗反膜用传输矩阵（TMM）算残余反射与吸收剖面（可选增强）。
- **自检**：$\int G\,dd \le (1-R)\Phi_0/h\nu$（能量守恒）。

### 步骤 2 — 几何与网格
- 2D 轴对称器件用 **柱坐标**：`raxis_variable="x"`, `raxis_zero=0`，并调用
  `cylindrical_node_volume / edge_couple / surface_area`，设置全局 `*_model` 参数。
- **径向必须足够密**：`CylindricalNodeVolume` 对径向单元是 O(1/nx) 收敛，
  `nx=2→16` 时体积误差 16.7%→2.1%（否则会虚增总光生载流子 → EQE>100%）。
- 用内建 2D mesher 时，**每个接触两侧都要有 region**（可加薄 dummy 区），否则接触数为 0。
- 表面/结区细化（ps=1e-6 cm）；吸收深度方向按 $\alpha$ 决定分辨率。

### 步骤 3 — 掺杂剖面
- 用 `node_model` 的 `erfc/step` 构造高斯/余误差分布（见 `device/netdoping.py` 风格）。
- 电阻率→掺杂：$N=\dfrac{1}{q\,\mu\,\rho}$（例：400 Ω·cm p-Si → $N_A\approx3.3\times10^{13}$）。

### 步骤 4 — 平衡态求解（标准收敛策略）
```
势场解 (CreateSiliconPotentialOnly) → DC
载流子初始化 (init_from=IntrinsicElectrons/Holes)
漂移扩散 (含光生模型，Gopt=0) → DC
```

### 步骤 5 — 光注入
- `SetOpticalGeneration(G)` 写入节点模型；`G=0` 即暗态。
- 对任意 α/TMM/多层，直接在 Python 逐节点算 G 后 `set_node_values` 最灵活。
- **光照必须斜坡加载**（`Φ0×[1e-3,1e-2,0.1,0.5,1]`），否则 Newton 发散。

### 步骤 6 — 偏压处理
- 反向偏压**逐步斜坡**（ΔV≈0.5 V），不可从 0 直接跳到高反压。
- 电容/带宽用**电路耦合接触 + SSAC**：`circuit_element(V1, ...)`,
  `contact_equation(circuit_node=...)`, `solve(ac)`,
  $C=-\mathrm{Im}(I_{V1.I})/(2\pi f)$。
- 注意：不要把 `cathode_bias` 设为 device 参数，否则会**遮蔽**电路节点更新。

### 步骤 7 — 光电器件指标
$$R(\lambda)=\frac{I_{ph}}{P_{opt}}=\frac{I_{illum}-I_{dark}}{\Phi_0 A},\qquad
\mathrm{EQE}=\frac{R\,hc}{q\lambda}=\frac{R\cdot1239.84}{\lambda[\mathrm{nm}]}$$
- 暗电流：$G=0$ 下反偏 I-V。
- 电容：SSAC（或 dQ/dV，但需正确的接触电荷模型）。
- 带宽：瞬态脉冲光照（时变源需支持时间参数）或 AC + 等效 RC。

### 步骤 8 — 验证（必做）
1. **解析对标**：1D 全耗尽 PIN 满足 $J_{ph}=q\int G\,dx$（本仓库 P5.1：误差 0.28%）。
2. **能量守恒**：$I_{ph}\le q(1-R)\Phi_0/h\nu\,A$（EQE≤100%）。
3. **KCL**：阴极与阳极电流等大反号。
4. **物理极限**：$C\to\varepsilon A/t_{epi}$（全耗尽）；暗电流由 $q n_i W A/\tau$ 定标。
5. **文献 golden 数据**比对。

---

## 3. 常见坑与对策

| 现象 | 原因 | 对策 |
|---|---|---|
| Newton 发散（施加光照/偏压后） | 源/偏压突变、载流子量级突变 | Φ0 与 V 均斜坡加载 |
| 轻掺杂器件不收敛 | 矩阵病态 | `extended_solver/model/equation=True` |
| EQE>100% | 柱坐标体积积分虚增光生 | 增大径向 `nx`（≥16）；或校验体积和 |
| 接触数为 0 | 内建 mesher 接触需两侧 region | 加薄 dummy region |
| 蓝光响应过低 | 欧姆接触钉扎表面载流子（死层） | 加表面复合/SRH 或浅结工程（进阶） |
| C 不随厚度变化 | 未全耗尽（W<t_epi） | 提高反压或减薄 epi 到全耗尽 |
| 电容为 0/常数 | 用了 `get_contact_charge` 而非 SSAC | 用电路 + AC 方法 |

---

## 4. 复用清单（本仓库）

| 模块 | 作用 |
|---|---|
| `optics/absorption.py` | Si α(λ), n(λ), Fresnel R |
| `optics/generation.py` | Beer-Lambert（含背反射）、理想光电流/EQE 公式 |
| `physics/optical_physics.py` | 光生连续方程封装、`ApplyBeerLambert`、接触电流 |
| `device/pin2d.py` | 2D 轴对称 PIN 网格/掺杂/柱坐标 |
| `device/pin2d_device.py` | 统一的“建-解-斜坡-电容”流程 |
| `drivers/pd_pn_1d.py` | 1D 解析验证 |
| `drivers/pd_pin_2d_dark.py` | 暗 I-V / C-V |
| `drivers/pd_pin_2d_photo.py` | 光谱响应度/EQE |
| `analysis/plot_results.py` | 出图 |

> 迁移到新器件时，只需替换 **步骤 2/3（几何与掺杂）** 与 **步骤 1 的材料光学常数**，
> 步骤 4–8 的求解与验证框架保持不变。
