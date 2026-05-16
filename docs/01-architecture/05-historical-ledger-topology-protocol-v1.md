# Historical Ledger Topology Protocol v1

日期：2026-05-15

状态：frozen-by-historical-ledger-topology-protocol-card-20260515-01

## 1. 目标

本文件冻结 `Malf-Pas` 第一阶段的历史大账本拓扑协议。

本卡只定义逻辑账本、共同键、run lineage、source manifest 与分账本规则，不创建正式数据库，
不执行 schema migration，不授权 runtime build。

## 2. Historical Ledger Principle

`Malf-Pas` 后续所有事实库、语义账本和读出账本必须被视为同一个历史大账本的分区，
而不是一组互不相干的散库。

首张治理 roadmap 收口后，后续每张模块 roadmap 还必须遵守：

1. 一张 roadmap 只对应一个模块数据库或一个模块账本边界。
2. 当前模块数据库未 ready、未通过检查前，不得开启下一张 roadmap。
3. 后续模块数据库都只是同一个历史大账本里的受治理分账本。

| 原则 | 裁决 |
|---|---|
| ledger model | `one logical historical ledger with multiple governed sub-ledgers` |
| physical storage | `not frozen as runtime implementation in this card` |
| formal DB mutation | `no` |
| cross-ledger consistency | `lineage / manifest / audit first; no cross-DB atomic transaction assumption` |
| source of truth | `repo governance records define authority; data roots provide facts only after authorized release` |

## 3. Sub-Ledger Topology

| ledger_role | future owner | 作用 | 当前裁决 |
|---|---|---|---|
| `source_fact` | `Data Foundation` | 原始行情、基础行情、元数据、可交易事实和 provider adapter 输入 | 必须拥有 source manifest；外部 provider 不得成为 truth owner |
| `structure_fact` | `MALF v1.4` | 波段、transition、boundary、WavePosition 等结构事实 | 以 validated MALF v1.4 为锚点；本卡不重新定义 MALF |
| `semantic_ledger` | `PAS` | context、trigger、strength、lifecycle 与机会解释状态 | 只读上游结构事实，不回写 MALF |
| `decision_ledger` | `Signal` | candidate accept / reject 与候选裁决记录 | 不输出订单、仓位、成交或收益承诺 |
| `management_ledger` | `Position` | T1/T2、保本、跟踪、entry / exit plan 等管理语义 | 后续模块冻结前不得 runtime 化 |
| `portfolio_plan_ledger` | `Portfolio Plan` | 组合准入、目标暴露、trim 与组合计划语义 | 保留独立轻量层，不被 Position 或 Trade 吞并 |
| `execution_ledger` | `Trade` | order intent / fill / rejection 的账本边界 | 真实 broker、paper-live 和成交闭环 deferred |
| `readout_ledger` | `System Readout` | 审计快照、链路读出、回测汇总读出 | 只读历史大账本，不发明上游事实 |
| `orchestration_ledger` | `Pipeline` | run、manifest、checkpoint、batch audit 与调度记录 | 只调度和记录，不拥有业务语义 |

## 4. Common Governance Keys

所有后续子库、事实文件、manifest、checkpoint 和读出表面必须预留以下共同治理键。

| key | 用途 | 规则 |
|---|---|---|
| `symbol` | 标的级定位 | 股票、指数或其他资产标识必须保持可追踪，不得用展示名替代 |
| `timeframe` | 周期定位 | `day / week / month` 等周期必须显式记录 |
| `bar_dt` | bar 事实日期 | 行情、结构事实、机会解释默认使用的时间键 |
| `trade_dt` | 交易或执行日期 | Trade / execution ledger 使用；不得混作分析日期 |
| `plan_dt` | 计划或组合日期 | Portfolio Plan / Position plan 使用 |
| `run_id` | 当前生成 run | 每次构建、审计、proof 或 promote 必须有稳定 run 标识 |
| `source_run_id` | 直接上游 run | 每个派生事实必须指向直接上游 run |
| `schema_version` | schema 合同版本 | schema 变更必须显式版本化 |
| `rule_version` | 业务规则版本 | MALF / PAS / Signal / Position 等规则变更必须显式版本化 |
| `source_manifest_hash` | 输入集合指纹 | 用于证明派生事实对应的 source manifest |
| `checkpoint_key` | 增量与恢复定位 | 每日增量、batch 和 resume 的定位锚点 |

时间键选择规则：

1. 事实 bar 与结构事实优先使用 `bar_dt`。
2. 计划和管理语义可使用 `plan_dt`，但必须保留可回溯到上游 `bar_dt` 的 lineage。
3. 执行边界使用 `trade_dt`，且不得混同 `bar_dt` 或 `plan_dt`。
4. 一个表面如同时跨越多个时间语义，必须显式记录对应字段，不得压成单一 `date`。

## 5. Source Manifest Protocol

`source_manifest` 是历史大账本的输入账册，不是外部 provider 的原样转述。

每个后续正式 source manifest 必须至少回答：

| manifest_field | 说明 |
|---|---|
| `manifest_id` | manifest 自身稳定标识 |
| `source_manifest_hash` | 输入集合、版本和关键范围的稳定指纹 |
| `source_root` | 输入根目录或 provider adapter 边界 |
| `provider_role` | `adapter only`，不得是 truth owner |
| `dataset_scope` | 覆盖的数据族、周期、标的范围和时间范围 |
| `input_version` | source adapter 或输入合同版本 |
| `schema_version` | 输出 schema 合同版本 |
| `generated_by_run_id` | 生成 manifest 的 run |
| `audit_status` | `pending / passed / blocked / failed` |

`H:\Asteria-data` 是上一版 Asteria 数据根，只能作为只读参考与 lineage 经验输入；
它不是 `Malf-Pas` 当前系统数据落点，也不得作为 scratch。

在 `Malf-Pas` 中，`H:\Malf-Pas-data` 才是重构后当前系统的本地数据库根目录。
当前阶段仍不授权写入正式 DB、不执行 schema migration、不授权 runtime build。

首选正式 truth source 根当前进一步收紧为：

```text
H:\tdx_offline_Data
H:\new_tdx64
```

`TuShare / baostock / AKShare` 不得成为正式 truth owner；mock 也不得冒充正式输入真值。

当前系统根目录必须按 `docs/00-governance/04-root-directory-policy-v1.md` 拆分：
`H:\Malf-Pas-data` 放未来正式数据，`H:\Malf-Pas-backup` 放备份包，
`H:\Malf-Pas-Validated` 放本系统沉淀后的历史经验，`H:\Malf-Pas-reprot` 放报告，
`H:\Malf-Pas-temp` 放临时产物。上一版 `H:\Asteria-*` 目录均不得作为当前 output root。

## 6. Run Lineage Protocol

run lineage 是跨库一致性的第一证明链。

| lineage_rule | 裁决 |
|---|---|
| direct parent | 派生账本必须记录直接上游 `source_run_id` |
| manifest binding | 派生账本必须记录输入对应的 `source_manifest_hash` |
| version binding | 派生账本必须记录 `schema_version` 与 `rule_version` |
| replay boundary | 后续重放必须从 manifest、checkpoint 和 direct parent run 定位 |
| promote boundary | working facts 只有在 audit passed 后才能 promote 到正式账本 |
| broken lineage | lineage 缺失时不得宣告正式 released 或 passed |

lineage 方向固定为：

```text
source_fact
-> structure_fact
-> semantic_ledger
-> decision_ledger
-> management_ledger
-> portfolio_plan_ledger
-> execution_ledger
-> readout_ledger
```

`Pipeline` 只记录和调度这条链路，不改变任一业务账本的语义。

## 7. Cross-Ledger Consistency

本卡不假设多个 DuckDB、SQLite、Parquet 或未来混合存储之间存在跨库事务原子性。

后续一致性证明必须依赖：

1. 共同治理键。
2. `run_id -> source_run_id` lineage。
3. `source_manifest_hash`。
4. `schema_version` 与 `rule_version`。
5. checkpoint / batch audit。
6. conclusion index 与 execution 四件套。

任何无法通过这些证据串起来的输出，都只能是临时研究结果或 blocked 结果，不得成为正式历史大账本事实。

## 8. Boundary With Next Card

本卡冻结“历史大账本长什么样、靠哪些共同键和 lineage 连起来”。

`daily-incremental-and-resume-protocol-card` 继续冻结：

```text
daily incremental
dirty scope
checkpoint
resume mode
staging promote
```

因此，本卡不替第六卡定义具体 dirty scope 算法，也不实现增量 runner。

## 9. Invariants

| invariant_id | invariant |
|---|---|
| `HISTORICAL-LEDGER-ONE-LOGICAL-LEDGER` | 系统必须被治理成一个逻辑历史大账本，而不是散库集合 |
| `COMMON-GOVERNANCE-KEYS-REQUIRED` | 所有后续子库必须预留共同治理键 |
| `SOURCE-MANIFEST-REQUIRED` | source fact 及其派生账本必须绑定 source manifest |
| `RUN-LINEAGE-REQUIRED` | 派生事实必须保留 `run_id` 与 `source_run_id` |
| `NO-CROSS-DB-ATOMICITY-ASSUMPTION` | 跨库一致性靠 lineage、manifest 和 audit，不靠隐含事务原子性 |
| `NO-FORMAL-DB-MUTATION` | 当前阶段不得写入正式 DB 或正式数据根目录 |
| `ONE-ROADMAP-ONE-MODULE-DB` | 首张治理 roadmap 收口后，后续每张 roadmap 只允许推进一个模块数据库 |
| `NEXT-ROADMAP-REQUIRES-CURRENT-MODULE-DB-READY` | 当前模块数据库未 ready、未通过检查前，不得开启下一张 roadmap |
