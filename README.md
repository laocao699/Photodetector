
# DEVSIM TCAD 器件仿真研究项目

> 本仓库 = **上游 DEVSIM 2.10.0 源码树** + **`work/` 研究工作层**（多阶段器件仿真与文献复现）。
> 上游 DEVSIM 部分版权归 DEVSIM LLC，采用 Apache-2.0 许可（见 [LICENSE](LICENSE) / [NOTICE](NOTICE)）；
> `work/` 为本人的研究工作，同样以 Apache-2.0 发布。
> **如果你是来看研究内容的，请直接跳到 [`work/README.md`](work/README.md)。**

## 研究工作层 `work/`

基于开源 DEVSIM 开展的递进式 TCAD 器件仿真研究：**自建光学与宽禁带物理模型**，完成从
「网格 → 掺杂 → 漂移扩散 → DC/AC/瞬态 → 后处理 → 文献 golden 对照」的全流程，全部阶段均已
在本环境**端到端重跑验证**。

| Phase | 目录 | 器件 / 物理 | 基准 | 状态 |
|---|---|---|---|---|
| 1 | [`work/phase1_diode`](work/phase1_diode) | Si PN 二极管 1D/2D/3D，DC/AC/瞬态 | 理论公式 | 4/4 断言 PASS |
| 2 | *(见报告)* | 框架原理（FVM / 模型三层 / SYMDIFF / Newton） | 官方文档 | 理论梳理 |
| 3 | [`work/phase3_bjt`](work/phase3_bjt) | 2D Si BJT，Gummel / Ic-Vce / fT，混合仿真 | devsim_bjt_example golden | fT +3.71%、DC 均 2.24% |
| 4 | [`work/phase4_electrothermal`](work/phase4_electrothermal) | 1D 二极管 + 2D BJT 电热耦合 | 跨材料交叉验证 | 逐位一致 |
| 5 | [`work/phase5_photodetector`](work/phase5_photodetector) | 2D 轴对称 Si PIN 光电二极管 | Roger et al. 2018 | R@800nm 0.610 A/W（−3.2%） |
| 6 | [`work/phase6_newmaterials`](work/phase6_newmaterials) | β-Ga₂O₃ 宽禁带日盲紫外探测器 | Boulahia 2024 / Labed 2022 | 单测 20 项、日盲截止 ~255nm |

**文档索引**

| 文档 | 内容 |
|---|---|
| [`work/README.md`](work/README.md) | 研究工作台总索引、阶段状态矩阵、标准流程链 |
| [`work/工作报告_Phase5-6.md`](work/工作报告_Phase5-6.md) | Phase 5–6 工作报告（参考对象 / 数学物理原理 / 工程架构 / 实验结果 / 展望 + 附录 A、B 文献要点与对照） |
| [`work/REVIEW_REPORT.md`](work/REVIEW_REPORT.md) | 全项目代码审查 / 验证 / 优化报告 |
| [`work/REPORT_phase1_3.md`](work/REPORT_phase1_3.md) | Phase 1–3 复现总结 |
| `work/phase*/REPORT_p*.md`、`METHOD_TEMPLATE*.md` | 各阶段技术报告与可迁移方法学模板 |
| [`PACKAGE_USAGE.md`](PACKAGE_USAGE.md) | **项目压缩包使用说明**（校验 / 解压 / 环境配置 / 复现命令 / 内容取舍） |

## 环境配置

实测环境（全部 Phase 已在此组合下验证通过）：

| 组件 | 版本 |
|---|---|
| OS | Ubuntu 26.04 LTS（WSL2, x86_64）；上游另支持 macOS / Windows / RHEL8 |
| Python | 3.13.12（上游要求 ≥ 3.9） |
| devsim | **2.10.0**（PyPI 预编译轮子，含 `python_packages/` 物理封装） |
| numpy / scipy / matplotlib | 2.4.4 / 1.17.1 / 3.10.8 |
| gmsh | 4.15.2（Phase 1/3 网格生成与导入；Phase 5/6 用 devsim 内建 2D mesher，非强制） |

安装（**运行研究脚本只需这一步**，无需编译 C++ 引擎）：

```bash
python3 -m pip install -r requirements.txt
# 校验：应输出 devsim 2.10.0
python3 -c "import devsim; print(devsim.__version__)"
```

仅当需要修改 `src/` 下的 C++ 引擎时，才需按 [BUILD.md](BUILD.md) 从源码构建，并先初始化子模块：

```bash
git submodule update --init --recursive   # external/ 下的 eigen、boost、superlu、symdiff、umfpack
```

## 快速开始（复现研究结果）

```bash
bash work/tools/run_phase.sh 1        # Phase 1 二极管，秒级，含断言式验证门禁
bash work/tools/run_phase.sh 3        # Phase 3 BJT 全族 + fT，约 20-30 分钟
python3 work/tools/compare_golden.py  # Phase 3 与论文 golden 数据自动对照
bash work/tools/run_phase.sh 4        # Phase 4 电热耦合（BJT 约 80s）
bash work/tools/run_phase.sh 5        # Phase 5 Si PIN 光电，数分钟
bash work/tools/run_phase.sh 6        # Phase 6 β-Ga₂O₃（含 20 项单测；a4 关键图较重）
```

各阶段日志输出至 `work/logs/`。静态检查：`python3 -m ruff check work/ python_packages/`。

## 分发压缩包

本项目可以压缩包形式分发（已排除可再生大产物，约 15 MB）：

```bash
bash work/tools/make_package.sh    # 生成 devsim_tcad_research_package.tar.gz + .sha256
```

接收方的校验、解压、环境配置与复现步骤详见 [`PACKAGE_USAGE.md`](PACKAGE_USAGE.md)。

## 仓库体积与忽略规则

仿真产生的大体积可再生产物**不纳入版本控制**（详见 [.gitignore](.gitignore)）：

- `work/**/*.vtu`（VTK 场数据，共约 848MB）、`*.tec`、`*.log`、`work/logs/`、`work/_baseline_snapshot/`
- Phase 4 无扩展名设备转储（`write_devices(type="tecplot")`，单个达 25MB）

**保留**的是小体积且复现必需的内容：`.dat`（结果表）、`.out`（golden 对照数据）、`.png`（图）、
`.msh`（运行输入网格）。因此克隆后可直接跑 `compare_golden.py` 与出图脚本；需要场分布可视化时
重跑对应 Phase 即可再生 `.vtu`。

## 仓库来源与结构说明

- **提交历史**：本仓库为重新初始化，**不携带上游 devsim 的提交历史**；首个提交即当前完整快照。
  上游源码以文件形式保留，版权与许可见 [LICENSE](LICENSE) / [NOTICE](NOTICE)（Apache-2.0）。
- **`devsim_bjt_example/`**：为上游 [devsim/devsim_bjt_example](https://github.com/devsim/devsim_bjt_example)
  的**内置副本**（非 submodule，已去除其嵌套 `.git`），目的是让克隆者无需额外步骤即可跑
  Phase 3 的 golden 对照（`data/*.out` 共 50 个）。其中大体积 `.tec` 中间产物已忽略。
- **`external/`**：保留为 7 个 submodule（eigen / boost ×3 / superlu / symdiff / umfpack_lgpl），
  commit 固定值与上游一致，**默认未初始化**。运行 `work/` 下任何研究脚本都**不需要**它们
  （研究脚本使用 PyPI 版 devsim）；仅当从源码构建 C++ 引擎时才需
  `git submodule update --init --recursive`。
- **Python 依赖**：见 [requirements.txt](requirements.txt)（仓库原本无任何依赖清单，为本研究层补上）。
- **压缩包分发**：若不想用 git，可直接使用 `work/tools/make_package.sh` 生成的压缩包，
  详见 [PACKAGE_USAGE.md](PACKAGE_USAGE.md)。

---

[![DOI](https://joss.theoj.org/papers/10.21105/joss.03898/status.svg)](https://doi.org/10.21105/joss.03898)

# DEVSIM

## Introduction:
**DEVSIM** - TCAD Device Simulator

**DEVSIM** is a tool for TCAD Device Simulation, using finite volume methods.  The source code is provided by DEVSIM LLC.

## Website:

The official website is here:

[https://devsim.org](https://devsim.org)

## Software Features:

* Python scripting 
* DC, small-signal AC, impedance field method, transient
* User specified partial differential equations (PDE).
* Extended floating point precision
* 1D, 2D, and 3D simulation
* 1D, 2D mesher
* Import 3D meshes.
* 2D cylindrical coordinate simulation
* ASCII file format with PDE embedded.

## Usage In Research:

Please see this [link](https://docs.google.com/spreadsheets/d/11TpoCrNzKwWDDmjKtP1d5bCiwn8WYNJkm1ZleJI0_k4/edit?usp=sharing) for a list of published research papers using or referring to the DEVSIM simulator.

## Installation:

Please see [INSTALL.md](INSTALL.md) for installation instructions.  Please see [BUILD.md](BUILD.md) for instructions to build from source.

## Citing This Work:

Please see [CITATION.md](CITATION.md).  *Please do not cite this GitHub Repository as it will be moving in the future.*

## License:

DEVSIM is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).  Example scripts are also provided under this license.  Other files are subject to the license terms of their copyright owners.
Please see [LICENSE](LICENSE) and [NOTICE](NOTICE) for license terms.

## Documentation:

The PDF documentation is located in ``doc/devsim.pdf``.  An online version of the documentation is available at [https://devsim.net](https://devsim.net).  A list of documentation resources is available [online](https://devsim.org/introduction.html#documentation).  Recent changes are available in [CHANGES.md](CHANGES.md).

The repository for the documentation is at [https://github.com/devsim/devsim_documentation](https://github.com/devsim/devsim_documentation).

## Supported Platforms:

| OS | Version | Architecture |
| --- | --- | --- |
| macOS | Sonoma 14.7.6 | `arm64` |
| Microsoft Windows | Windows 10 | `x64` |
| Linux | AlmaLinux 8 (Red Hat Enterprise Linux 8 Compatible) | `aarch64`, `x86_64` |

## Supported Python Versions

DEVSIM is designed to work with Python versions 3.9 or higher.

## Code of Conduct:

Please see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Support:

For support and general discussion, please join our forum:
[https://forum.devsim.org](https://forum.devsim.org)

## Contributing:

Please see:
[Contribution guidelines for this project](CONTRIBUTING.md)

## Testing

Please see [TEST.md](TEST.md).

## Related Projects

### Used directly by the simulator
| Name | Description |
| --- | --- |
| [symdiff](https://github.com/devsim/symdiff) | Symbolic differentiation engine for the simulator |
| [devsim_documentation](https://github.com/devsim/devsim_documentation) | Documentation for the simulator |

### Extended examples
| Name | Description |
| --- | --- |
| [devsim_bjt_example](https://github.com/devsim/devsim_bjt_example) | Bipolar Junction Transistor example |
| [devsim_density_gradient](https://github.com/devsim/devsim_density_gradient) | Quantum Corrections to Drift Diffusion simulation |
| [devsim_3dmos](https://github.com/devsim/devsim_3dmos) | 3D Mosfet example used in publication |
| [devsim_misc](https://github.com/devsim/devsim_misc) | Miscellaneous scripts |

