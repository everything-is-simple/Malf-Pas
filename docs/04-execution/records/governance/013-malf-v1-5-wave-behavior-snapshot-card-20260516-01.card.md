# MALF v1.5 Wave Behavior Snapshot Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-v1-5-wave-behavior-snapshot-card-20260516-01` |
| card type | `governance` |

## 2. 本次目标

- 新建 `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5`。
- 将 `wave_behavior_snapshot` 冻结为 MALF-owned structure behavior facts。
- 明确 v1.5 只能消费 MALF v1.4 事实，不得替 PAS 生成强弱结论。
- 建立 `governance/malf_v1_5_wave_behavior_snapshot_registry.toml`。
- 将 live next 从第 13 卡推进到 `pas-v1-2-strength-weakness-matrix-card`。

## 3. 允许动作

- 写入 validated authority asset：`H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5`。
- 新增 MALF v1.5 authority doc、registry 与 execution 四件套。
- 更新 README、docs README、AGENTS、主线图、来源裁决、MALF 锚点、模块所有权、roadmap、结论索引、gate registry 与 repo registry。
- 增强 repo-local governance check，校验 MALF v1.5 registry。

## 4. 禁止动作

- 不改写 `MALF v1.4` 原目录或原定义。
- 不让 PAS 反向定义 MALF 结构行为字段。
- 不新增 `strength_score`、`setup_family`、`accept/reject` 或交易动作语义。
- 不写入正式 DB、schema、runner、cache、report 或 scratch 产物。
- 不输出 broker、paper-live、实盘、仓位、订单、成交、收益或 alpha 证明。
- 不迁移历史 repo 代码、旧 schema、queue、checkpoint、DuckDB 表面或 pipeline 行为。

## 5. 通过标准

- `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` 形成 `9 markdown files + MANIFEST.json`。
- `wave_behavior_snapshot` 的 six-facet boundary 冻结。
- `governance/malf_v1_5_wave_behavior_snapshot_registry.toml` 建立并纳入 governance check。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest 与 exact authority search 通过。
