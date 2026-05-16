# PAS Axiomatic State Machine Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `pas-axiomatic-state-machine-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 将第 11 卡从“冻结 PAS 最小状态机与七层语义”升级为“冻结 PAS v1.1 三件套正式设计集”。
- 在 `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` 建立 PAS Core / Lifecycle / Service 设计集。
- 明确 PAS v1.1 从 MALF v1.4 `WavePosition` 出发，不从 `PriceBar` 出发。
- 建立 `governance/pas_axiomatic_state_machine_registry.toml`，用机器可读治理层固定 PAS 边界。
- 将 live next 从第 11 卡推进到 `open-source-adapter-boundary-card`。

## 3. 允许动作

- 修订 roadmap，将第 11 卡交付物升级为 PAS v1.1 Three-Part Design Set。
- 写入 validated authority asset：`H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1`。
- 更新 PAS authority doc、source authority、MALF anchor、predecessor strength、module gate、repo registry、conclusion index 与 AGENTS 当前状态。
- 新增 PAS registry，并把它纳入 repo-local governance check。
- 建立第 11 卡 execution 四件套。

## 4. 禁止动作

- 不修改 MALF v1.4 定义、WavePosition、transition、boundary 或 Lifespan 规则。
- 不从 `PriceBar` 直接构造 PAS 结构事实。
- 不创建 `PAS_07` 或额外设计文件。
- 不复制 YTC 书籍正文。
- 不写入正式 DB、schema、runner、cache、report 或 scratch 产物。
- 不输出 broker、paper-live、实盘、仓位、订单、成交、收益或 alpha 证明。
- 不迁移历史 repo 代码、旧 schema、queue、checkpoint、DuckDB 表面或 pipeline 行为。

## 5. 通过标准

- `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` 形成 8 份正文加 `MANIFEST.json`。
- PAS 主链固定为 `MALF WavePosition -> PAS-Core -> PAS-Lifecycle -> PAS-Service -> Signal`。
- PAS 宗旨固定为 `identify strength / weakness; reject weakness; join strength`。
- `governance/pas_axiomatic_state_machine_registry.toml` 登记设计集、MALF 锚点、lifecycle、setup family、禁令与 handoff 边界。
- repo-local governance check 校验 PAS registry。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest 与 exact authority search 通过。
