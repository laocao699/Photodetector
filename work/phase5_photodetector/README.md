# Phase 5 — Si PIN 光电二极管 TCAD 仿真（开源 DEVSIM）

用开源 DEVSIM 实现光电传感器仿真，并复现 Roger et al. 2018 的 Si PIN 光电二极管
golden 数据。核心是自建 **Beer-Lambert 光学生成模块**并注入漂移-扩散连续性方程。

## 目录

```
optics/    吸收常数与光生率（Beer-Lambert，含背反射）
physics/   光生连续方程封装 + 接触电流
device/    2D 轴对称 PIN 网格/掺杂/柱坐标 与统一建解流程
drivers/   1D 解析验证 / 2D 暗 I-V·C-V / 2D 光谱响应
analysis/  出图脚本与结果图
METHOD_TEMPLATE.md   可复现光电器件 TCAD 仿真方法学模板
REPORT_p5.md         结果报告
```

## 环境

devsim 2.10.0、gmsh 4.15、numpy、scipy、matplotlib（Python ≥3.9）。

## 快速开始

```bash
python3 drivers/pd_pn_1d.py                 # 1D 解析验证（秒级）
python3 drivers/pd_pin_2d_dark.py 20 1e-4   # 暗 I-V / C-V
python3 drivers/pd_pin_2d_photo.py 30 1e-3 5  # 光谱响应/EQE
python3 analysis/plot_results.py            # 生成 analysis/fig_*.png
```

驱动参数：
- `pd_pin_2d_dark.py  <t_epi_um> <taun_s>`
- `pd_pin_2d_photo.py <t_epi_um> <taun_s> <V_bias>`

## 关键结果

- 1D 解析验证误差 **0.28%**
- 暗电流 @1 V：**3.58 pA**（文献 3.5–10 pA）
- 30 µm：R@800 nm **0.610 A/W**（文献 0.63），QE@750 nm **95%**

详见 `REPORT_p5.md`；迁移到其他器件见 `METHOD_TEMPLATE.md`。
