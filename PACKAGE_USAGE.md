# 项目压缩包使用说明（PACKAGE USAGE）

本文件说明如何校验、解压、配置环境并使用 `devsim_tcad_research_package.tar.gz`。

---

## 1. 压缩包信息

| 项 | 值 |
|---|---|
| 文件名 | `devsim_tcad_research_package.tar.gz` |
| 体积 | 约 **15 MB**（工作树约 1 GB，已排除可再生大产物） |
| 条目数 | 约 1000 |
| SHA256 | **以随包的 `devsim_tcad_research_package.tar.gz.sha256` 为权威值**（每次重新打包会变） |
| 校验文件 | `devsim_tcad_research_package.tar.gz.sha256` |
| 归档内路径 | 均以 `./` 开头（相对路径），**建议解压到指定空目录** |

> 重新生成压缩包：`bash work/tools/make_package.sh`（排除规则见 `work/tools/package_exclude.txt`）。
> 该脚本会同时重算并覆写 `.sha256` 校验文件，并在终端打印本次的体积/条目数/SHA256。

## 2. 校验完整性

```bash
# 归档与 .sha256 文件需位于同一目录
sha256sum -c devsim_tcad_research_package.tar.gz.sha256
# 期望输出: devsim_tcad_research_package.tar.gz: OK

# 若需人工比对，查看权威校验值：
cat devsim_tcad_research_package.tar.gz.sha256
```

## 3. 解压

```bash
# Linux / macOS
mkdir -p devsim_tcad && tar -xzf devsim_tcad_research_package.tar.gz -C devsim_tcad
cd devsim_tcad
```

```powershell
# Windows 10/11（系统自带 bsdtar），在 PowerShell 或 CMD 中：
mkdir devsim_tcad
tar -xzf devsim_tcad_research_package.tar.gz -C devsim_tcad
cd devsim_tcad
```

也可用 7-Zip / WinRAR 图形界面直接解压（`.tar.gz` 需两次解包：先 `.gz` 再 `.tar`）。

## 4. 环境配置

**验证过的环境组合**（本项目全部阶段已在此组合下端到端跑通）：

| 组件 | 版本 |
|---|---|
| OS | Ubuntu 26.04 LTS（WSL2, x86_64）；上游另支持 macOS / Windows / RHEL8 |
| Python | 3.13.12（上游要求 ≥ 3.9） |
| devsim | **2.10.0**（PyPI 预编译轮子） |
| numpy / scipy / matplotlib | 2.4.4 / 1.17.1 / 3.10.8 |
| gmsh | 4.15.2（Phase 1/3 网格用；Phase 5/6 用 devsim 内建 mesher，非强制） |

安装（建议使用虚拟环境或 conda 环境）：

```bash
python3 -m pip install -r requirements.txt
```

`requirements.txt` 内容：`devsim==2.10.0`、`numpy>=1.26`、`scipy>=1.11`、`matplotlib>=3.8`、`gmsh>=4.11`。

**安装后自检**（应输出 `2.10.0`）：

```bash
python3 -c "import devsim; print(devsim.__version__)"
```

> **无需编译 C++ 引擎**：研究脚本使用的是 PyPI 安装的 devsim（含 `python_packages/` 物理封装）。
> 压缩包内的 `src/`、`cmake/`、`external/` 仅为上游源码留存；只有当你要修改 C++ 求解器本身时，
> 才需按 [BUILD.md](BUILD.md) 构建，且必须先 `git submodule update --init --recursive`
> 拉取 `external/` 依赖（**压缩包未含子模块内容**，见 §7）。

## 5. 快速验证（建议按此顺序）

```bash
# ① 最快：Phase 1 二极管（秒级），自带断言式验证门禁，末尾应打印 "4/4 项全部 PASS"
bash work/tools/run_phase.sh 1

# ② Phase 6 单元测试（秒级，20 项，应输出 "Ran 20 tests ... OK"）
cd work/phase6_newmaterials && python3 -m unittest discover -s tests -v && cd -

# ③ Phase 3 与论文 golden 数据自动对照（秒级，直接读压缩包内已有的 .out 数据）
python3 work/tools/compare_golden.py
```

第 ③ 步预期输出：fT 峰值偏差约 **+3.71%**、DC 曲线均值约 **2.24%**（属 devsim 版本差异，
详见 `work/REPORT_phase1_3.md` §3.3）。

## 6. 完整复现各阶段

```bash
bash work/tools/run_phase.sh 1     # Phase 1 二极管          —— 秒级
bash work/tools/run_phase.sh 3     # Phase 3 BJT 全族 + fT   —— 约 20–30 分钟
bash work/tools/run_phase.sh 4     # Phase 4 电热耦合        —— 二极管秒级 / BJT 约 80 秒
bash work/tools/run_phase.sh 5     # Phase 5 Si PIN 光电     —— 数分钟
bash work/tools/run_phase.sh 6     # Phase 6 β-Ga₂O₃         —— 含 a4 关键图，总计可达数小时
bash work/tools/run_phase.sh all   # 全部（建议分次执行）
```

- 可选子步骤过滤：`bash work/tools/run_phase.sh 6 a2`（只跑 a2）；
  `bash work/tools/run_phase.sh 6 arora`（只跑 Arora 标定变体）。
- 运行日志写入 `work/logs/`（该目录不在压缩包内，运行时自动创建）。
- **耗时提示**：Phase 6 的 `a4_key_figures.py` 含约 7 次 2D 扩展精度设备重建、约 70 次求解，
  实测单次运行可达 3 小时；若只需验证物理正确性，跑 `tests` + `a0`–`a3` 即可（数分钟至十几分钟）。
- 建议用 `nohup ... &` 或 `tmux`/`screen` 后台运行重型阶段。

## 7. 压缩包内容说明

**已包含**：全部源码（`src/`、`python_packages/`、`work/`）、全部文档与报告（含本说明文件）、
运行输入网格（`.msh`）、结果数据（`.dat`、`.out`）、图（`.png`）、
Phase 3 golden 对照数据（`devsim_bjt_example/data/*.out` 共 50 个 + `work/phase3_bjt/*_new.out` 共 20 个）、
两篇参考论文（PDF + markdown）、`requirements.txt`、`LICENSE`/`NOTICE`。

**已排除**（均为可再生或元数据，规则见 `work/tools/package_exclude.txt`）：

| 排除项 | 原体积 | 如何再生 |
|---|---|---|
| `work/**/*.vtu`、`*.vtm`、`*.visit` | ~848 MB | 重跑对应 Phase（`write_devices(type="vtk")`） |
| `*.tec`（含 Phase 4 无扩展名 tecplot 转储 25 MB） | ~89 MB | 重跑对应 Phase（`write_devices(type="tecplot")`） |
| `work/logs/`、`work/**/*.log` | ~22 MB | 运行 `run_phase.sh` 自动生成 |
| `work/_baseline_snapshot/` | 6.3 MB | 审查用基线快照，非必需 |
| `.git/`、`devsim_bjt_example/.git/` | ~21 MB | **不含版本历史**；如需 git 请自行 `git init` |
| `__pycache__/`、`.ruff_cache/` 等缓存 | — | 运行时自动重建 |
| `external/` 各子模块内容 | — | `git submodule update --init --recursive`（需 git 仓库） |

> 注意：`external/` 下仅保留目录骨架与构建脚本，**第三方库源码（eigen/boost/superlu/symdiff/umfpack）
> 未包含**。这只影响"从源码编译 C++ 引擎"，**不影响运行任何研究脚本**（研究脚本用 PyPI 版 devsim）。

## 8. 文档导读

| 想了解 | 看这里 |
|---|---|
| 项目总览、阶段状态矩阵、标准流程链 | [`README.md`](README.md) → [`work/README.md`](work/README.md) |
| Phase 5–6 工作汇报（原理/架构/结果/展望 + 两篇文献附录） | [`work/工作报告_Phase5-6.md`](work/工作报告_Phase5-6.md) |
| 代码审查 / 验证 / 优化结论与遗留问题 | [`work/REVIEW_REPORT.md`](work/REVIEW_REPORT.md) |
| Phase 1–3 复现细节与 golden 偏差分析 | [`work/REPORT_phase1_3.md`](work/REPORT_phase1_3.md) |
| 各阶段技术报告 | `work/phase4_electrothermal/REPORT_p4.md`、`work/phase5_photodetector/REPORT_p5.md`、`work/phase6_newmaterials/REPORT_p6.md` |
| 可迁移方法学模板 | `work/phase5_photodetector/METHOD_TEMPLATE.md`、`work/phase6_newmaterials/METHOD_TEMPLATE_v2.md` |
| 上游 DEVSIM 官方文档 | `doc/devsim.pdf`、`doc/devsim_doc_markdown.md`、<https://devsim.net> |

## 9. 许可与署名

- 上游 DEVSIM（`src/`、`python_packages/`、`examples/`、`testing/` 等）版权归 DEVSIM LLC，
  采用 **Apache-2.0** 许可，详见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。
- `work/` 研究工作层同样以 Apache-2.0 发布；其中 `work/phase1_diode`、`work/phase3_bjt`、
  `work/phase4_electrothermal` 的部分脚本派生自官方样例（保留原始版权头）。
- `devsim_bjt_example/` 为上游官方样例仓库的副本（Apache-2.0），其 golden 数据由 2016 年
  devsim "Beta 0.01" 生成。
- 引用 DEVSIM 本身请遵循 [CITATION.md](CITATION.md)（请勿引用本仓库）。
