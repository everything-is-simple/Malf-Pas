# MALF+PAS Scenario Atlas Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-pas-scenario-atlas-card-20260516-01` |
| card type | `governance` |

## 2. 本次目标

- 新建 `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0`。
- 将 atlas 冻结为 MALF+PAS 的只读场景图谱 companion asset。
- 固定 `5` 个标准案例与 `Markdown + SVG` 图解载体。
- 建立 `governance/malf_pas_scenario_atlas_registry.toml`。
- 将 live next 从第 15 卡推进到 `open-source-adapter-boundary-card`。

## 3. 允许动作

- 写入 validated authority asset：`H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0`。
- 新增 atlas authority doc、registry 与 execution 四件套。
- 更新 README、docs README、AGENTS、来源裁决、主线图、模块所有权、roadmap、结论索引、gate registry 与 repo registry。
- 增强 repo-local governance check，校验 atlas registry。

## 4. 禁止动作

- 不改写 `MALF v1.4`、`MALF v1.5`、`PAS v1.1` 或 `PAS v1.2`。
- 不把 atlas 写成 playbook、runtime contract、formal backtest proof 或收益证明。
- 不新增 broker、订单、仓位、成交、alpha、收益或实盘口径。
- 不写入正式 DB、schema、runner、cache、report 或 scratch 产物。
- 不迁移 legacy code、旧 schema、旧 runner 或旧 DuckDB 表面。

## 5. 通过标准

- `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0` 形成 `7 markdown files + 5 svg files + MANIFEST.json`。
- atlas 的 companion 口径、图解规范、`5` 个标准案例与 reference-only 规则冻结。
- `governance/malf_pas_scenario_atlas_registry.toml` 建立并纳入 governance check。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest、ruff 与 exact authority search 通过。
