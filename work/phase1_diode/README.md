# Phase 1 — 硅 PN 二极管基础样例（DEVSIM 官方样例复现 + 数值验证）

在 `work/phase1_diode/` 下隔离运行 DEVSIM 官方 `examples/diode/` 全部样例，并用
`analyze_diode.py` 做逐行拆解与物理数值验证。本阶段是后续 Phase 3–6 的方法学起点。

## 环境与运行

devsim 2.10.0 / Python 3.13。所有脚本无命令行参数，直接运行：

```bash
cd work/phase1_diode
python3 diode_1d.py          # 1D 内建网格：势场解 -> 漂移扩散 -> DC 扫描
python3 diode_2d.py          # 2D 内建网格（含 air 区）
python3 gmsh_diode2d.py      # gmsh 2D 网格导入
python3 gmsh_diode3d.py      # gmsh 3D 网格导入
python3 ssac_diode.py        # 小信号 AC + circuit_element，提取结电容 C(V)
python3 tran_diode.py        # transient_bdf1 瞬态 + 扩展精度
python3 analyze_diode.py     # 复现 + 断言式数值验证（生成 diode_1d_analysis.png）
```

一键复现（日志写入 `work/logs/`）：

```bash
bash work/tools/run_phase.sh 1
```

## 验证判据（analyze_diode.py 内置断言门禁）

`analyze_diode.py` 在平衡态 (V=0) 与 IV 特性上内置 4 项 PASS/FAIL 断言，任一失败则以
非零码退出，可直接作为回归门禁。当前实测（devsim 2.10.0）：

| 物理量 | 仿真值 | 理论/期望 | 结论 |
|---|---|---|---|
| 内建电势 Vbi | 0.9537 V | Vt·ln(NA·ND/ni²)=0.9524 V | PASS (±2%) |
| 质量作用定律 n·p (中值) | 1.00e20 | ni²=1e20 | PASS (±5%) |
| 结区最大电场 Emax | 3.832e5 V/cm | 3.83e5 V/cm | PASS (±25%) |
| IV @V=0.5 电流密度 J | 1.816e-2 A/cm² | 1.82e-2 A/cm² | PASS (±10%) |

器件参数：NA=ND=1e18 cm⁻³（`step` 突变结，结位于 x=0.5 µm），ni=1e10 cm⁻³，T=300 K。

小信号电容（`ssac_diode.py`）：C(0 V)=2.087e-7 F → C(0.5 V)=3.127e-7 F，与
`REPORT_phase1_3.md` 记载一致。所有样例均收敛（DC RelError→1e-14 量级）。

## 产物

| 文件 | 内容 |
|---|---|
| `diode_1d_analysis.png` | IV / 掺杂载流子 / 电位电场 / 电流分量 四联图 |
| `diode_1d.dat`、`gmsh_diode*_dd.dat` | tecplot 数据 |
| `work/logs/phase1_*.log` | 各脚本运行日志（由 run_phase.sh 生成） |

## 审查结论（本次复核）

- 全部 7 个脚本在 devsim 2.10.0 / Python 3.13 下 **exit=0 通过**，数值与
  `REPORT_phase1_3.md` 精确一致。
- 优化项：`analyze_diode.py` 原仅出图，现增补平衡态 + IV 断言式校验，把报告中的验证表
  落成**可复跑的 PASS/FAIL 门禁**（纯后处理，未改动任何物理/数值行为）。
- 脚本为官方样例的现代化 py3 版本，结构清晰，无遗留缺陷。

详细总结见 `../REPORT_phase1_3.md` 第 1 节。
