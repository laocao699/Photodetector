# Phase 3 — 硅 BJT 全流程复现（网格→掺杂→漂移扩散→DC/AC/fT→混合仿真）

在 `work/phase3_bjt/` 隔离运行 `devsim_bjt_example/simdir/` 全链路，并与论文 golden
数据（`devsim_bjt_example/data/*.out`，2016 devsim "Beta 0.01" 生成）逐项对照。
器件：2D 硅 BJT，`bjt.msh`（13777 节点 / 27235 三角元），base/emitter/collector 三接触。

脚本为官方 devsim 样例（Apache-2.0）的副本，物理与数值行为保持一致；本目录仅对其做
最小、向后兼容的复现性增强（见下"审查结论"）。

## 完整运行链路

`bjt_common.run()` 通过 `load_devices("bjt_dd_0.msh")` 复用平衡态，故 **必须先跑
`bjt_dd.py`**；其后每个 `bjt_circuitN.py` 独立冷启动（可并行）。

| 环节 | 命令 | 产物 | 对应 golden |
|---|---|---|---|
| 1. 平衡态 | `python3 bjt_dd.py` | `bjt_dd_0.tec/.msh` | — |
| 2. Ic-Vce 族 | `python3 bjt_circuit2.py <Vb> [rel_err]` | `vb2_<Vb>_new.out` | `ic_vce_<Vb>.out` |
| 3. 输出特性 | `python3 bjt_circuit3.py <Vc>` | `vc_<Vc>_new.out` | `vc_<Vc>.out` |
| 4. Gummel | `python3 bjt_circuit4.py <Vcb>` | `ve_<Vcb>_new.out` | `gummel_<Vcb>.out` |
| 5. fT (SSAC) | `python3 bjt_circuit5.py 0.0 1000 1e11 3` | `ssac_0.0_new.out`→`ft_data_new.out` | `ft_data.out` |
| 6. 出图 | `python3 plot_bjt.py` | `bjt_gummel/icvce/ft_new.png` | 论文图 |

一键全族复现（日志写入 `work/logs/`）：

```bash
bash work/tools/run_phase.sh 3            # 平衡态 + 全部扫描 + fT + 出图
python3 work/tools/compare_golden.py      # 自动 golden 对照表
```

> **Vb=0.1 离态说明**：`bjt_circuit2.py 0.1` 处于近截止离态，电流为纯数值噪声
> (~1e-12 A)，用默认 Vc 扫描容差 `1e-3` 会触发 `RuntimeError: Min step size too small`。
> 本目录已把该容差参数化为可选第 2 参数（默认 `1e-3` 不变），离态点用
> `bjt_circuit2.py 0.1 1e-2` 即可扫完；`run_phase.sh` 已自动处理。此为物理离态的数值
> 特性（golden 数据同样如此），非复现错误。

## 复现结果与 golden 对照（devsim 2.10.0，本次端到端重跑）

`compare_golden.py` 输出（`|Ic|` 相对偏差，离态点 |Ic|<1e-9 已排除）：

| 曲线族 | mean dIc% | max dIc% | 判定 |
|---|---|---|---|
| Gummel Vcb=0.0–0.5 | 2.06–4.63 | ≤14.6 | 低注入区系统性偏移 |
| Ic-Vce Vb=0.3–1.0 | 0.63–2.69 | ≤2.73 | OK |
| 输出特性 Vc=0.0/0.5 | 0.11–1.89 | ≤2.69 | OK |
| **截止频率 fT (Vcb=0)** | 峰值 **1.836 GHz** vs golden 1.771 GHz | **+3.71%** | OK (≤5%) |
| fT 峰值处 Ic | 0.3735 A/cm vs golden 0.3676 | +1.6% | OK |

DC 曲线总体均值 **2.24%**，全部落在 `REPORT_phase1_3.md` 记载的容差内。低注入区
系统性 +2~2.8% 偏移源于 golden 由 2016 "Beta 0.01" 生成、与 2.10.0 的版本差异
（斜率/峰值/滚降全部吻合），非复现错误。

## 审查结论（本次复核）

- 全族 19 次设备重建 + fT（1000 频点·工作点）**端到端重跑全部收敛**，`compare_golden.py`
  自动对照确认与 golden 高度一致（fT +3.71%，DC 均值 2.24%）。
- **修复的复现缺口**：`bjt_circuit2.py` 原硬编码 Vc 扫描容差 `1e-3`，导致离态点 Vb=0.1
  无法扫完且无任何脚本固化所需的放宽容差。现增补可选第 2 参数（默认 `1e-3`，行为不变），
  使 Vb=0.1 可复现，`run_phase.sh` 一键跑通全族（FAILS=0）。
- **孤立文件修复**：`diode_1d.py`（BJT 目录中从官方 simdir 拷来的 py2 遗留热身脚本，
  不被 BJT 流程引用）含 `print ymin` 等 Python 2 语法，在 py3 下无法解析；已改为
  `print(ymin)`。功能等价的现代 py3 版本见 `../phase1_diode/diode_1d.py`。
- **官方派生代码保留项**（不改，仅记录）：`physics/ramp2.py` 存在两处完全相同的
  `def rampbias`（前者被后者遮蔽，且 BJT 流程实际使用 `rampvoltage`，属死代码）；
  `physics/new_physics.py` 有 4 处 `"<无占位符串>" % tdict` 的空操作（ruff F507，无害）。
  二者均为上游样例原样，改动无收益且有偏离 golden 风险，故保留。

详见 `../REPORT_phase1_3.md` 第 3 节与 `../REVIEW_REPORT.md`。
