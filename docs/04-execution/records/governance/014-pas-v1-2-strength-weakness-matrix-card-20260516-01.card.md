# PAS v1.2 Strength Weakness Matrix Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `pas-v1-2-strength-weakness-matrix-card-20260516-01` |
| card type | `governance` |

## 2. 本次目标

- 新建 `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2`。
- 将 `strength_weakness_matrix` 冻结为 PAS-owned discrete opportunity-interpretation layer。
- 明确 v1.2 只能消费 `WavePosition + WaveBehaviorSnapshot`，不得回头读 `PriceBar`。
- 建立 `governance/pas_v1_2_strength_weakness_matrix_registry.toml`。
- 将 live next 从第 14 卡推进到 `malf-pas-scenario-atlas-card`。

## 3. 允许动作

- 写入 validated authority asset：`H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2`。
- 新增 PAS v1.2 authority doc、registry 与 execution 四件套。
- 更新 README、docs README、AGENTS、主线图、来源裁决、MALF 锚点、模块所有权、roadmap、结论索引、gate registry 与 repo registry。
- 增强 repo-local governance check，校验 PAS v1.2 registry。

## 4. 禁止动作

- 不改写 `PAS v1.1` 原目录或原定义。
- 不改写 `MALF v1.4` 或 `MALF v1.5`。
- 不新增 `strength_score`、数值排序、accept/reject、订单、仓位、成交或收益语义。
- 不写入正式 DB、schema、runner、cache、report 或 scratch 产物。
- 不输出 broker、paper-live、实盘、仓位、订单、成交、收益或 alpha 证明。
- 不提前施工第 15 卡的跨模块场景图谱。

## 5. 通过标准

- `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` 形成 `9 markdown files + MANIFEST.json`。
- `strength_weakness_matrix` 的离散 read、setup posture、matrix service surface 与降档规则冻结。
- `governance/pas_v1_2_strength_weakness_matrix_registry.toml` 建立并纳入 governance check。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest、ruff 与 exact authority search 通过。
