# Phase 6A — β-Ga₂O₃ 日盲紫外光电探测器

## 目标
- 以 Boulahia et al. 2024（Optical and Quantum Electronics 56:549）为基准，先验证 β-Ga₂O₃ 材料与肖特基边界，再构建 2D 平面光电探测器，并向 MSM 递进。

## 交付内容
- `materials/`：β-Ga₂O₃ 参数与 DUV 吸收、肖特基接触纯函数。
- `physics/`：通用宽禁带漂移扩散、SRH+Auger+光生、肖特基/欧姆边界。
- `device/`：1D 肖特基、2D 平面、2D MSM 几何。
- `drivers/`：材料自检、1D 暗态、2D 光电、MSM 驱动。
- `tests/`：20 项单元测试全部通过（`python3 -m unittest discover -s tests -v`）。
- `analysis/plot_results.py`：`analysis/fig_phase6.png`。

## 快速复现
```bash
python3 -m unittest discover -s tests -v
python3 drivers/a0_material_check.py
python3 drivers/a1_schottky_dark.py
python3 drivers/a2_planar_photo.py
python3 drivers/a3_msm_photo.py
python3 analysis/plot_results.py
```

## 当前结论
- β-Ga₂O₃ 材料库与肖特基接触已验证。
- 255 nm 日盲响应明确，355 nm 几乎无响应。
- 暗电流、掺杂、波长趋势符合论文方向；绝对响应度低于 Silvaco 参考值，主要是论文中的陷阱/Arora/BGN/离化细节尚未完全移植。

## 本次复核（devsim 2.10.0 端到端重跑）
- 单元测试 `Ran 20 tests ... OK`；a0 材料自检 ni=2.067e-22 cm⁻³、Wdep(-2V)=0.346 µm、255nm G(0)=1.28e22、355nm α≈0.1（日盲截止正确）。
- a1 肖特基暗态：全偏压 **KCL=0.00e+00**、J_reverse(-2V)=-2.679e-3 A/cm²。
- a2 平面光电：暗 J(-2V)=-2.718e-3、R@255nm=0.1286 A/W（与 REPORT_p6 一致）。
- a3 MSM：dark I(-2V)=-6.35e-7 A、illum=-4.65e-6 A、PDCR=7.33、R=0.0574 A/W。
- 一键复现：`bash work/tools/run_phase.sh 6`（tests + a0–a4 + 出图）。

详细过程与限制见 `REPORT_p6.md`，可迁移流程见 `METHOD_TEMPLATE_v2.md`，全项目审查见 `../REVIEW_REPORT.md`。
