# DEVSIM TCAD 研究工作台（work/）— 总索引与状态

本目录是在开源 TCAD 仿真器 **DEVSIM 2.10.0** 之上、按阶段递进开展的器件仿真研究：
从官方样例复现，到方法迁移，再到自建物理（光学 / 宽禁带）与新材料器件开发。
所有阶段均**构建在 `python_packages/` 官方物理封装之上**，不修改上游 C++ 引擎。

> 环境：devsim 2.10.0 / Python 3.13 / numpy·scipy·matplotlib；gmsh 网格。
> 本次全面审查/验证/优化的完整记录见 [`REVIEW_REPORT.md`](REVIEW_REPORT.md)。

## 阶段索引与状态矩阵

| Phase | 目录 | 器件 / 物理 | golden 基准 | 复现状态 | 文档 |
|---|---|---|---|---|---|
| 1 | [`phase1_diode/`](phase1_diode) | Si PN 二极管 1D/2D/3D，DC/AC/瞬态 | 理论公式 | 已验证 4/4 PASS | [README](phase1_diode/README.md) |
| 2 | *(见 REPORT)* | 框架原理（FVM/模型三层/SYMDIFF/Newton） | 文档 Ch5/8/9/10 | 理论梳理 | [REPORT §2](REPORT_phase1_3.md) |
| 3 | [`phase3_bjt/`](phase3_bjt) | 2D Si BJT，DC/Gummel/Ic-Vce/fT，混合仿真 | devsim_bjt_example/data | 已验证 fT +3.71%、DC 均 2.24% | [README](phase3_bjt/README.md) |
| 4 | [`phase4_electrothermal/`](phase4_electrothermal) | 1D 二极管 + 2D BJT 电热耦合 | 跨材料交叉验证 | 已验证（温升 14.3mK、Joule 恒正） | [REPORT_p4](phase4_electrothermal/REPORT_p4.md) |
| 5 | [`phase5_photodetector/`](phase5_photodetector) | 2D 轴对称 Si PIN 光电二极管 | Roger et al. 2018 | 已验证（R@800nm 0.610、1D 0.28%） | [README](phase5_photodetector/README.md) · [REPORT_p5](phase5_photodetector/REPORT_p5.md) |
| 6 | [`phase6_newmaterials/`](phase6_newmaterials) | β-Ga₂O₃ 宽禁带日盲探测器（肖特基/平面/MSM） | Boulahia 2024 / Labed 2022 | 已验证（单测 20 项、日盲截止 ~255nm） | [README](phase6_newmaterials/README.md) · [REPORT_p6](phase6_newmaterials/REPORT_p6.md) |

四维评级（可靠 / 稳定 / 高效 / 说明清晰）见 [`REVIEW_REPORT.md`](REVIEW_REPORT.md) 汇总表。

## 标准仿真流程链（贯穿所有 Phase）

```
网格(gmsh/内建) → 掺杂(erfc 节点模型) → 势场初解(纯泊松) → 载流子初始化
   → 漂移扩散装配(态密度/迁移率/SRH/Bernoulli-SG) → 平衡态 DC
   → 偏置斜坡/扫描(自适应步长) → [电路耦合 AC/fT | 光生注入 | 热方程耦合]
   → 后处理出图 → 三层验证(解析极限 / 物理守恒 KCL·能量 / 文献 golden)
```

## 复现工具（work/tools/）

| 工具 | 作用 |
|---|---|
| [`tools/run_phase.sh`](tools/run_phase.sh) | 各 Phase 端到端一键复现，日志写入 `work/logs/` |
| [`tools/compare_golden.py`](tools/compare_golden.py) | Phase 3 BJT 复现结果与论文 golden 自动对照（DC 插值比对 + fT β=1 提取） |

快速开始：

```bash
bash work/tools/run_phase.sh 1        # 秒级，验证工具链
bash work/tools/run_phase.sh 3        # BJT 全族（含 fT），约 20-30 分钟
python3 work/tools/compare_golden.py  # golden 对照表
bash work/tools/run_phase.sh 5        # Si PIN 光电
bash work/tools/run_phase.sh 6        # beta-Ga2O3（含 20 项单测）
```

## 目录约定

- `logs/`：`run_phase.sh` 生成的带时间戳运行日志。
- `_baseline_snapshot/`：优化前既有产物（`.out/.dat/.log/.vtm`）快照，供回归 diff。
- 各 Phase 目录：`device/ physics/ materials/ optics/ drivers/ analysis/ tests/` 分层
  （Phase 5/6），或扁平脚本序列（Phase 1/3/4，源自官方样例）。
