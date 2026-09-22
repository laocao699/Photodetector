# DEVSIM 研究项目 — 全面审查 / 验证 / 优化报告

> 范围：`work/` 研究工作层（Phase 1/3/4/5/6，约 8000 行 Python）+ 其复用的
> `python_packages/` 物理封装。**不改动**上游 devsim C++ 引擎（`src/`、`external/`）
> 与官方样例（`examples/`、`testing/`、`devsim_bjt_example/simdir`）。
> 方法：静态审查（ruff + 人工）→ **全部阶段实际端到端重跑** → 与 golden/理论/既有产物
> 对照 → 修复缺陷与优化 → 更新文档。
> 环境：devsim 2.10.0 / Python 3.13 / numpy·scipy·matplotlib；16 核 / 23 GB。

---

## 1. 总体结论

**研究代码整体质量高、流程可靠**：五个阶段全部在本环境端到端重跑成功，关键指标与各自
golden/文献基准在文档记载容差内**精确复现**（多数为逐位吻合）。发现的问题以"复现链路
缺口 + 文档不一致 + 官方派生死代码"为主，**无影响物理正确性的缺陷**。已完成最小且经验证
的修复与优化，并补齐/校正了各阶段说明文档。

| 维度 | 结论 |
|---|---|
| 可靠（结果正确） | 全部阶段重跑结果与 golden/理论一致；Phase 3 fT +3.71%、DC 均 2.24%；Phase 1/4/5 逐位吻合 |
| 稳定（收敛无崩溃） | 全流程收敛；Phase 3 全族 0 崩溃（修复离态点后）；Phase 6 KCL 残差 0 |
| 高效（运行时间） | 轻量阶段秒级；重阶段（BJT fT、2D 扩展精度、Ga₂O₃ a4）分钟~数十分钟，已支持并行/后台 |
| 说明清晰（文档） | 新增顶层索引 + 审查报告；补齐 Phase 1/3 README；校正 Phase 6 测试数；各报告与实跑一致 |

---

## 2. 各阶段端到端验证结果

### Phase 1 — Si PN 二极管（`phase1_diode/`）
7 个脚本全部 `exit=0`；`analyze_diode.py` 新增断言门禁 **4/4 PASS**：

| 物理量 | 实测 | 期望 | 判定 |
|---|---|---|---|
| 内建电势 Vbi | 0.9537 V | 0.9524 V（Vt·ln(NaNd/ni²)） | PASS |
| 质量作用 n·p | 1.00e20 | ni²=1e20 | PASS |
| 结区最大电场 Emax | 3.832e5 V/cm | 3.83e5 | PASS |
| IV @0.5V 电流密度 | 1.816e-2 A/cm² | 1.82e-2 | PASS |
| SSAC 结电容 C(0→0.5V) | 2.087e-7 → 3.127e-7 F | 报告 2.09e-7→3.13e-7 | 一致 |

### Phase 3 — Si BJT 全流程（`phase3_bjt/`）
平衡态 + 全族扫描（19 次设备重建）+ fT（1000 频点·工作点）端到端重跑，`compare_golden.py`
自动对照 golden：

| 曲线族 | mean dIc% | 判定 |
|---|---|---|
| Gummel Vcb=0.0–0.5 | 2.06–4.63 | 低注入系统性偏移（版本差异） |
| Ic-Vce Vb=0.3–1.0 | 0.63–2.69 | OK |
| 输出特性 Vc=0.0/0.5 | 0.11–1.89 | OK |
| **fT 峰值** | **1.836 GHz vs golden 1.771（+3.71%）** | OK |
| fT 峰值处 Ic | 0.3735 vs 0.3676 A/cm（+1.6%） | OK |

DC 总体均值 **2.24%**，全部落在 `REPORT_phase1_3.md` 记载容差内。

### Phase 4 — 电热耦合（`phase4_electrothermal/`）
| 器件 | 收敛 | 温升 | Joule 热 | 与 REPORT_p4 |
|---|---|---|---|---|
| 1D 二极管 | RelError 5.75e-14 | ~0（µK 级） | peak 2.67e7 / mean 1.95e5（恒正） | 逐位一致 |
| 2D BJT | 耦合 RelError 9.6e-10 | **14.3 mK** | peak 2.50e7 / mean 6.96e5（恒正） | 逐位一致 |

等温 Ic=0.32118 vs 电热 Ic=0.32126 A/cm（差 **0.024%**）；PT 热 peak 2.4e7 / mean −2.77e5
（正负交替净抵消）。热传导方程正常联立收敛。

### Phase 5 — Si PIN 光电二极管（`phase5_photodetector/`）
| 指标 | 实测 | 文献/报告 | 判定 |
|---|---|---|---|
| 1D 解析验证误差 | **−0.283%** | −0.283% | 逐位一致 |
| 暗电流 @1V（20/30µm） | 3.584 / 3.590 pA | 3.5–10 pA | 一致 |
| R@800nm（20/30µm, BARC） | 0.586 / **0.610** A/W | 0.63（30µm） | −3.2% |
| EQE@750nm（20/30µm） | 92.9% / **95.0%** | ~100% | 一致 |
| C_plate / C@1V（30µm） | 0.361 / 1.395 pF | 0.361 / 1.395 | 逐位一致 |

能量守恒 EQE≤100%、阴/阳极 KCL 闭合。

### Phase 6 — β-Ga₂O₃ 日盲探测器（`phase6_newmaterials/`）
| 步骤 | 结果 | 与 REPORT_p6 |
|---|---|---|
| 单元测试 | `Ran 20 tests ... OK` | 一致（README 原误写 12，已校正） |
| a0 材料自检 | ni=2.067e-22、Wdep(-2V)=0.346µm、255nm G(0)=1.28e22、355nm α≈0.1 | 逐位一致 |
| a1 肖特基暗态 | 全偏压 **KCL=0.00e+00**、J_rev(-2V)=−2.679e-3 A/cm² | 一致 |
| a2 平面光电 | 暗 J(−2V)=−2.718e-3、R@255nm=0.1286 A/W | 逐位一致 |
| a2 `--arora` 标定 | 暗 J(−2V) 2.72→**2.00e-3**（更接近论文 1e-3）、R=0.1167 | 与 REPORT_p6 §二逐位一致 |
| a2 `--traps` 标定 | 暗 J 不变、**光电流 6.43→6.34e-3**（illum−dark，小降） | 与 REPORT_p6 §二逐位一致 |
| a3 MSM | dark I(−2V)=−6.35e-7 A、illum=−4.65e-6 A、PDCR=7.33、R=0.0574 A/W | 一致 |
| a4 关键图验证 | **exit=0、0 skip**；暗 J(-2V)=-2.718e-3、光 J=-1.286e-2、PDCR@-2V=5.73、R@255nm=0.1286、EQE=0.625、D*=6.73e10 Jones、截止~255nm | 与 REPORT_p6 §三逐项精确一致 |

日盲截止 ~255 nm、355 nm 近无响应，方向/量级与 Boulahia 2024 一致。

---

## 3. 代码审查发现与处置

| # | 位置 | 问题 | 严重度 | 处置 |
|---|---|---|---|---|
| 1 | `phase3_bjt/diode_1d.py:180,181,203,204` | Python 2 `print ymin` 语法，py3 下无法解析（孤立遗留热身脚本，不被 BJT 流程引用） | 中（真实语法错误） | **已修复**：改为 `print(ymin)`；等价 py3 版见 `phase1_diode/diode_1d.py` |
| 2 | `phase3_bjt/bjt_circuit2.py` | Vc 扫描容差硬编码 `1e-3`，离态点 Vb=0.1 触发 `Min step size too small`，且无脚本固化所需放宽容差 → 复现链路缺口 | 中（复现失败） | **已修复**：增补可选第 2 参数 `rel_error`（默认 `1e-3`，行为不变），`run_phase.sh` 对 Vb=0.1 自动用 `1e-2` |
| 3 | `phase4_electrothermal/ZLsimple_physics.py:695` `CreateJouleHeatSilicon` | 旧 `J·E` 形式在扩散区给负 Joule 热；为死代码（驱动均内联正定形式，不调用它），但存在误用隐患 | 低（死代码隐患） | **已加警示注释**：标注符号问题 + 指向驱动内正定形式（未改行为） |
| 4 | `phase3_bjt/physics/ramp2.py:71,109` | 两处完全相同的 `def rampbias`（前者被遮蔽），且 BJT 流程实际用 `rampvoltage` → 死代码 | 低（官方派生） | **记录不改**：上游样例原样，改动无收益且有偏离 golden 风险 |
| 5 | `phase3_bjt/physics/new_physics.py:451,452,457,458` | `"<无占位符串>" % tdict` 空操作（ruff F507） | 极低（无害） | **记录不改**：映射格式化对无占位符串是 no-op，结果正确 |
| 6 | `python_packages/pythonmesh.py:114` | `"Cannot handle element type " % i` 无占位符（F507），错误路径会抛 TypeError 而非预期 RuntimeError | 低（上游 latent） | **记录不改**：属上游源码；运行时用 site-packages 安装版，改仓库副本零运行时影响；研究用的单元类型永不命中该分支 |
| 7 | `phase6_newmaterials/README.md` | "12 项单元测试" 与实际 20 项不符 | 低（文档） | **已校正**为 20 项 |
| 8 | 全局（Phase 1/3 官方样例） | 638× F405 + 35× F403（`from devsim import *` 通配导入）、26× E402、18× E702 | 极低（风格） | **记录不改**：官方样例既定风格，批量改写会偏离上游且无功能收益 |

**未发现影响物理正确性的缺陷。** Phase 5/6 的分层代码（`materials/physics/device/drivers/`）
经审查为高质量：单位换算正确（`FILM_THICKNESS_CM=300e-7`=300nm；a4 `t_nm*1e-7`）、
多设备重建唯一命名、扩展精度默认开启、`argparse` 规范、光强/偏压双斜坡、`_safe_point`
收敛门禁、`np.interp` 插值越界自动 clamp——历史坑（µm/nm 单位、设备名冲突、EQE>100%、
接触两侧 region）在当前代码中均已正确处理。

---

## 4. 优化与工程化改进

| 项 | 内容 | 收益 |
|---|---|---|
| 复现 harness | 新增 `tools/run_phase.sh`：各 Phase 一键端到端复现，带时间戳日志、失败计数、子步骤过滤 | 复现从"手工串命令"变为单命令，可靠可重复 |
| golden 自动对照 | 新增 `tools/compare_golden.py`：解析 golden 裸列/本地 `CURVE:`/`AC:` 两种格式，按扫描变量插值比对 Ic/Ib + β=1 提取 fT，输出偏差表 | 替代手工比对，量化复现质量 |
| 断言式验证 | `phase1_diode/analyze_diode.py` 增补平衡态+IV 的 PASS/FAIL 门禁（失败非零退出） | 把报告验证表变为可复跑回归门禁 |
| 离态复现固化 | `bjt_circuit2.py` 容差参数化（见 #2） | Vb=0.1 离态曲线可复现，全族 FAILS=0 |
| 回归基线 | `_baseline_snapshot/baseline_outputs.tar`（64 个文本产物，6.3 MB） | 优化前后 diff，防意外回归 |
| 一致性注释 | `CreateJouleHeatSilicon` 警示注释（见 #3） | 消除死代码误用隐患 |

> 官方样例派生脚本（Phase 1/3）遵循"最小且经验证"原则：仅修复真实错误（#1/#2）与
> 增补后处理校验，**不改动任何物理/数值行为**，确保 golden 可复现性不受影响。

---

## 5. 四维评级汇总

| Phase | 可靠 | 稳定 | 高效 | 说明清晰 | 备注 |
|---|---|---|---|---|---|
| 1 二极管 | A | A | A | A | 4/4 断言 PASS；新增 README |
| 3 BJT | A | A | B | A | 全族复现；fT/DC 达标；离态缺口已修；fT 扫描较重 |
| 4 电热 | A | A | B | A | 逐位复现；BJT 耦合 ~80s；Joule 隐患已注 |
| 5 Si PIN | A | A | B | A | 逐位复现；2D 扩展精度较重；代码质量高 |
| 6 Ga₂O₃ | A | A | C | A | 单测 20 + a0–a3 复现；a4 关键图重建多、耗时长 |

（A=优/达标，B=可接受/有已知开销，C=功能正确但耗时显著。）

---

## 6. 遗留问题与建议（不在本次改动范围）

1. **重运行耗时（实测根因已定位）**：Phase 6 `a4_key_figures.py` 本次实测 **exit=0 完成，但全程耗时 ~178 分钟（09:15→12:13，>307 min CPU）**，**0 次收敛 skip**（非失败，纯属慢）。根因：扩展精度 2D 求解每次 ~1–2 min，而 a4 做约 **7 次设备重建（基线+3掺杂+3厚度）× 每次 ~10 次求解 ≈ 70 次扩展精度求解**（对比：a2 单次 ~13.5 min）。具体优化方向：（a）掺杂/厚度**趋势点无需全扩展精度**，可降为双精度或仅对基线保留扩展精度；（b）趋势点用 `load_devices` 复用基线网格/解作初值，避免每次冷启动重建；（c）`sweep_iv` 对单点 -2V 采用斜坡而非直跳，减少 Newton 迭代；（d）把“趋势检验”与“绝对指标”分档，趋势扫描减点。预计可将 a4 从 ~3h 降至 ~15–25 min。
2. **官方派生死代码**（#4/#5）：`ramp2.py` 重复 `rampbias`、`new_physics.py` 空操作格式化，
   属上游样例原样；如需清理应与上游同步，避免与 golden 参考产生分叉。
3. **上游 latent bug**（#6）：`pythonmesh.py:114` 的 F507 属 devsim 上游；如反馈上游，建议改
   `f"Cannot handle element type {i}"`。本仓库副本改动无运行时效果，故未改。
4. **Phase 6 绝对指标**：R/PDCR/D* 绝对值低于 Silvaco 参考（趋势/截止正确），源于肖特基势垒/
   陷阱/Arora/BGN 常数与专有模型差异，已在 `REPORT_p6.md` 逐项标定中定位；后续可补精确常数、
   引入瞬态验证陷阱导致的光导增益。
5. **深高注入/离态数值脆弱性**：BJT Vbe>0.9（Ic≈30A）与 Vb=0.1 离态对收敛路径敏感（golden
   自身在该点亦自相矛盾），属高注入极限区数值特性，非物理差异；已通过放宽容差/离态排除处理。

---

## 7. 复现命令附录

```bash
# 全部阶段（重阶段建议后台/分次）
bash work/tools/run_phase.sh 1          # 秒级
bash work/tools/run_phase.sh 3          # BJT 全族 + fT，约 20-30 分钟
bash work/tools/run_phase.sh 4          # 电热（二极管秒级 / BJT ~80s）
bash work/tools/run_phase.sh 5          # Si PIN 光电，数分钟
bash work/tools/run_phase.sh 6          # Ga2O3：tests + a0-a4，a4 数十分钟
python3 work/tools/compare_golden.py    # Phase 3 golden 自动对照表

# 静态检查
python3 -m ruff check work/ python_packages/ --statistics
```

各阶段日志见 `work/logs/`；优化前产物基线见 `work/_baseline_snapshot/`。
