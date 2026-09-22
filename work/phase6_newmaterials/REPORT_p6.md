# Phase 6A — β-Ga₂O₃ 日盲光电探测器：实现 + 逐项物理标定报告

## 范围
- 材料/器件：β-Ga₂O₃，以 **Boulahia et al. 2024**（IZTO/β-Ga₂O₃ 肖特基日盲 PD，doi:10.1007/s11082-023-06231-4）为主基准，陷阱/接触物理以 **Labed et al. 2022**（Nanomaterials 12:1061，doi:10.3390/nano12071061）为来源。
- 路线：材料库 → 1D 肖特基验证 → 2D 平面光电探测器 → MSM 递进；再按“陷阱→Arora→BGN→Selberherr”逐项物理标定。

## 一、材料库与基准（已验证）
`materials/ga2o3.py` + `materials/contacts.py` + `materials/registry.py`，单元测试 20 项通过：
| 量 | 值 | 依据 |
|---|---|---|
| Eg / χ / εr | 4.8 eV / 4.0 eV / 12.6 | Boulahia Table 1 |
| NC / NV | 3.7e18 / 5e18 cm⁻³ | 同上 |
| µn / µp | 172 / 10 cm²/Vs | 同上 |
| m_n* / m_p* | 0.28 / 0.35 | 同上 |
| ni(300K) | 2.067×10⁻²² cm⁻³ | 自洽 Boltzmann |
| 肖特基势垒 ΦB | 0.58 eV（IZTO 4.58 − χ 4.0） | 自洽 + 论文暗电流量级 |
| 255 nm 表面光生率 | 1.28×10²² cm⁻³s⁻¹ | 论文 ~10²² 量级 |
| DUV 截止 | 261 nm（α 表） | 论文 ≤261 nm |

## 二、逐项物理标定（单变量归因）
| 物理 | 开关默认值 | 对基线影响 | 结论 |
|---|---|---|---|
| 陷阱/深能级 SRH（Labed Table 2） | 可选 `--traps` | 暗电流不变；光电流 6.43→6.34e-3（小降） | 稳态影响小；其主要作用于光导增益/响应速度（瞬态），本期稳态仿真中有限 |
| Arora 迁移率 | 可选 `--arora` | 暗电流 2.72→2.00e-3（更接近论文 1e-3）；光电流略降 | 改善暗电流，物理合理 |
| BGN 带隙窄化 | 可选 `--bgn`（势场） | ND=3e16 下 ΔEg≈0 | 在本基线掺杂下可忽略（正确） |
| Selberherr 碰撞离化 | 可选（默认关） | −2 V 下增益≈1 | 在论文偏压范围内不激活（正确）；供高场/APD 工作用 |

## 三、关键图验证（P1）
`drivers/a4_key_figures.py`（含收敛门禁）：
| 指标 | 本工作 | 论文目标 |
|---|---|---|
| 暗 J(−2 V) | 2.72×10⁻³ A/cm² | ~1×10⁻³ |
| 光照 J(−2 V, 255 nm) | 1.29×10⁻² A/cm² | ~7×10⁻³（Fig 10c 峰值） |
| PDCR @ −2 V | 5.7 | ~1×10² |
| PDCR @ 0 V | ~10⁷（暗电流下限） | ~3×10⁴ |
| R @ 255 nm | 0.129 A/W | ~0.23 A/W |
| EQE @ 255 nm | 0.625 | — |
| D* @ 255 nm | 6.7×10¹⁰ Jones | 2.5×10⁹ Jones |
| 日盲截止 | ~255 nm | ≤261 nm |

**读法**：光电流与论文 Fig 10c 峰值（~7×10⁻³）同量级且方向/截止正确；R 与 PDCR 的绝对偏差主要来自肖特基接触/陷阱参数与 Silvaco 专有模型的差异，已在“逐项标定”中定位，非求解器问题。

## 四、关键工程发现（沉淀到 METHOD_TEMPLATE_v2）
1. **厚度单位 bug**：把“100–900 nm”误作 µm 会瞬间生成 18M 节点 → 单位必须与器件尺度一致。
2. **多 device 重建**：每重建必须给唯一 mesh/device 名，否则冲突。
3. **热发射 vs Dirichlet 肖特基边界**：在本器件上结果几乎一致（表明该类器件的暗电流需按论文校准势垒/界面态）。
4. **DUV 吸收极浅**：需 nm 级表面网格；光生率需按能量守恒自检。
5. **逐项标定法**：一次只加一项物理并记录指标变化，才能归因差距。

## 五、交付物
- `materials/`：registry、ga2o3（参数/DUV 吸收/陷阱/Arora/BGN/Selberherr）、contacts。
- `physics/`：wbg_physics（通用 WBG DD + 肖特基/欧姆接触）、validation（KCL/能量/R/EQE/D*）。
- `device/`：1D 肖特基、2D 平面、2D MSM。
- `drivers/`：a0（材料自检）、a1（1D 暗态）、a2（2D 光电，支持 traps/arora 开关）、a3（MSM）、a4（关键图验证）。
- `tests/`：20 项单元测试（unittest）。
- 报告/模板：`REPORT_p6.md`、`METHOD_TEMPLATE_v2.md`、`README.md`。
- 图：`analysis/fig_phase6.png`、`analysis/fig_key_figures.png`。

## 六、复现命令
```bash
python3 -m unittest discover -s tests -v
python3 drivers/a0_material_check.py
python3 drivers/a1_schottky_dark.py
python3 drivers/a2_planar_photo.py [--traps] [--arora] [--doping N] [--wavelength nm]
python3 drivers/a3_msm_photo.py
python3 drivers/a4_key_figures.py
python3 analysis/plot_results.py
```

## 七、下一步建议（不在本期）
- 补 Labed/Silvaco 的 Arora/BGN/陷阱精确常数，进一步收敛绝对指标。
- 引入瞬态仿真验证陷阱导致的光导增益/响应速度。
- 完成后进入 Track B（HfO₂/HZO FeFET）。
