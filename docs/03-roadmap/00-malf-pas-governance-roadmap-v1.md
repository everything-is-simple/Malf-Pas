# Malf-Pas 首张治理路线图 v1

日期：2026-05-15

状态：active / governance-only roadmap

## 1. 定位

本路线图是新系统的第一张路线图，只负责立法，不负责施工实现。

## 2. 共通边界

所有卡共享以下属性：

```text
governance-only
doc-first
read-only-to-previous-assets
six-root-directory-policy
book-and-history-reference-policy
no-formal-db-mutation
no-broker
no-profit-claim
no-legacy-code-migration
```

## 3. 十二张治理卡

| 顺序 | 卡 | 状态 | 目标 |
|---:|---|---|---|
| 1 | `governance-roadmap-freeze-card` | passed | 固定第一张路线图边界与命名口径 |
| 2 | `repo-governance-environment-bootstrap-card` | passed | 从 Asteria 继承治理插件、脚本、环境与机器可读治理层的最小可重建边界 |
| 3 | `system-mainline-module-ownership-card` | passed | 冻结 Data -> System 主线模块、语义所有权、自建/委外边界 |
| 4 | `storage-engine-and-portability-decision-card` | passed | 裁决 DuckDB、SQLite+Parquet、Go 可携带运行与 Python 研究环境的关系 |
| 5 | `historical-ledger-topology-protocol-card` | passed | 冻结系统大账本、子库共同键、run lineage、source manifest 与分账本规则 |
| 6 | `daily-incremental-and-resume-protocol-card` | passed | 冻结每日增量、dirty scope、checkpoint、断点续传与 staging promote 规则 |
| 7 | `backtest-window-and-holdout-protocol-card` | passed | 冻结 2012-2021 十年历史窗口、三年滚动验证、2021-2023/2024-2026 预留样本边界 |
| 8 | `source-authority-and-non-migration-rule-card` | passed | 冻结来源分类与非迁移规则 |
| 9 | `malf-v1-4-immutability-anchor-card` | passed | 锚定 MALF v1.4 的系统位置与不变量 |
| 10 | `predecessor-strength-map-card` | passed | 盘点旧系统与历史资料的最出彩强项 |
| 11 | `pas-axiomatic-state-machine-card` | passed | 冻结 PAS v1.1 三件套正式设计集 |
| 12 | `open-source-adapter-boundary-card` | planned | 固定开源项目的 adapter 边界 |

## 4. 治理环境准备范围

`governance-roadmap-freeze-card` 当前冻结结果如下：

```text
system_name = Malf-Pas
local_repo = H:\Malf-Pas
local_database_root = H:\Malf-Pas-data
backup_root = H:\Malf-Pas-backup
validated_root = H:\Malf-Pas-Validated
report_root = H:\Malf-Pas-reprot
temp_root = H:\Malf-Pas-temp
remote_repo = https://github.com/everything-is-simple/Malf-Pas
stage = governance-only / doc-first / no-formal-db-mutation
```

上一版 `H:\Asteria`、`H:\Asteria-data`、`H:\Asteria-Validated`、`H:\Asteria-report`、
`H:\Asteria-temp` 只作为只读参考，不得作为 `Malf-Pas` 当前 output root 或 scratch。
`G:\《股市浮沉二十载》` 是 PAS 书籍参考与思路风暴来源根，`G:\malf-history` 是曾经做过但未完成的
历史版本与模块取舍参考根；二者只读，不得作为 runtime、正式数据根、broker 指令或旧代码迁移来源。

`repo-governance-environment-bootstrap-card` 必须把上一版系统的治理环境经验纳入第一张路线图，
但不能把上一版 runtime、正式 DB 或模块实现直接迁入。

| Asteria 来源 | Malf-Pas 第一阶段裁决 |
|---|---|
| `H:\Asteria\plugins` | 评估是否建立 `plugins/`，并只迁入治理 workflow 插件形态 |
| `H:\Asteria\plugins\asteria-workflow` | 改造成 `malf-pas-workflow` 或同等插件；hooks 必须指向 `H:\Malf-Pas`，不得保留 `H:\Asteria` 写死路径 |
| `H:\Asteria\scripts` | 只迁入治理检查、dev doctor、文档/结论一致性检查脚本；不迁入业务模块 runner |
| `H:\Asteria\AGENTS.md` | 已作为本仓库 agent 规则范式输入，后续需补齐 workflow card 执行纪律 |
| `H:\Asteria\README.md` | 作为五根目录、阅读入口、权威状态写法参考，不复制 Asteria 当前 release state |
| `H:\Asteria\pyproject.toml` | 建立 Malf-Pas 自己的 package、test、ruff、mypy、governance 配置 |
| `H:\Asteria\environment.yml` | 建立可重建环境说明；`.venv` 本身不得提交 |
| `H:\Asteria\.gitignore` | 补齐缓存、DB、report、temp 产物忽略规则 |
| `H:\Asteria\.codex` | 只迁入本仓库需要的 Codex 配置/技能规则；不得迁入个人秘密或绝对旧路径 |
| `H:\Asteria\.venv` | 只作为依赖可行性参考，不复制进 repo |
| `H:\Asteria\governance` | 迁入机器可读治理层的最小结构，如 registry、contract、topology 的占位与校验规则 |

本卡通过后，本仓库应具备：

```text
repo-local workflow hooks
repo-local governance checks
reproducible environment config
machine-readable governance skeleton
clean ignore rules
no copied virtualenv
no copied business runtime
```

本卡已落成的 repo-local 面：

| 面 | 当前落点 |
|---|---|
| workflow hooks | `plugins/malf-pas-workflow` |
| governance checks | `scripts/governance/check_project_governance.py` |
| dev doctor | `scripts/dev/doctor.py` |
| reproducible env config | `pyproject.toml` / `environment.yml` |
| machine-readable governance skeleton | `governance/*.toml` |
| clean ignore rules | `.gitignore` |
| agent rules | `AGENTS.md` |
| repo entry | `README.md` |
| Codex repo-local boundary | `.codex/README.md` / `.codex/skills/malf-pas-governance/SKILL.md` |
| boundary freeze doc | `docs/00-governance/03-repo-governance-environment-bootstrap-v1.md` |
| root directory policy | `docs/00-governance/04-root-directory-policy-v1.md` / `governance/root_directory_registry.toml` |
| source authority policy | `docs/00-governance/01-source-authority-and-non-migration-rule-v1.md` / `governance/source_authority_registry.toml` |

## 5. 系统主线与自建/委外边界

`system-mainline-module-ownership-card-20260515-01` 已把从 `Data` 到 `System` 的模块边界冻结。

| 模块 | 第一阶段裁决 | 说明 |
|---|---|---|
| `Data Foundation` | `self-owned contract / adapter-fed` | 数据合同、source manifest、ledger key、可交易事实必须自建；外部 provider 只能做 source adapter |
| `MALF v1.4` | `self-owned immutable authority` | 结构事实层，继续作为不可变锚点 |
| `PAS` | `self-owned semantic core` | 机会解释、公理化状态机、强弱与 lifecycle 必须自建 |
| `Signal` | `self-owned decision ledger` | 候选聚合与接受/拒绝账本必须自建 |
| `Position` | `self-owned management semantics` | 持仓候选、entry / exit plan 语义自建 |
| `Portfolio Plan` | `self-owned lightweight layer` | 组合准入、目标暴露、trim 语义保留独立层，可早期轻量化 |
| `Trade` | `self-owned execution ledger boundary` | order intent / fill / rejection 语义自建；真实 broker 延后 |
| `System Readout` | `self-owned readout` | 全链路读出、审计快照、回测汇总自建 |
| `Pipeline` | `self-owned orchestration ledger` | 只调度、记录 run、checkpoint、manifest，不定义业务语义 |
| 外部项目 | `adapter / engine only` | 可做 source、计算、回测、调度 adapter，不拥有业务语义 |

本卡的正式冻结入口：

```text
docs/01-architecture/03-system-mainline-module-ownership-v1.md
governance/module_ownership_registry.toml
docs/04-execution/records/governance/003-system-mainline-module-ownership-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段主线裁决固定为：

```text
Data -> MALF v1.4 -> PAS -> Signal -> Position -> Portfolio Plan -> Trade -> System Readout
Pipeline = orchestration ledger only
External providers / projects = adapter or engine only
Portfolio Plan = retained independent lightweight layer
Runtime / formal DB / broker / profit claims = not authorized
```

## 6. 存储引擎与便携性裁决范围

`storage-engine-and-portability-decision-card` 必须裁决以下问题，但不得在第一张 roadmap 里直接切换正式存储：

| 方案 | 第一阶段裁决 |
|---|---|
| `DuckDB` | 继续作为当前研究/proof 默认候选，适合本地分析、列式扫描、多表审计 |
| `SQLite + Parquet` | 作为 Go 便携发行与长期文件格式候选，必须经过独立 proof 后才能替代 |
| `Hybrid` | 重点评估：SQLite 管 manifest/checkpoint/run ledger，Parquet 管列式事实，DuckDB 作为研究查询 adapter |
| `Go compiled binary` | 作为后续便携运行目标预留，不替代当前 Python 研究生态 |
| `Python` | 当前仍是研究、proof、生态集成主环境 |

本卡必须输出：

```text
storage_role_matrix
portable_runtime_boundary
python_research_boundary
go_distribution_candidate_boundary
no_storage_switch_without_proof
```

本卡已冻结的正式入口：

```text
docs/01-architecture/04-storage-engine-and-portability-decision-v1.md
governance/storage_engine_registry.toml
docs/04-execution/records/governance/004-storage-engine-and-portability-decision-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段存储与便携性裁决固定为：

```text
DuckDB = research / proof default candidate
SQLite = portable manifest / checkpoint / run ledger candidate
Parquet = portable columnar fact candidate
Hybrid = future evaluation candidate
Python = research / proof primary environment
Go compiled binary = portable distribution candidate only
No storage switch without independent proof
Runtime / formal DB / broker / profit claims = not authorized
```

## 7. 历史大账本与增量协议范围

`historical-ledger-topology-protocol-card` 与 `daily-incremental-and-resume-protocol-card`
必须把系统建成逻辑上的一个历史大账本，而不是一堆散库。

所有子库必须预留共同治理键：

```text
symbol
timeframe
bar_dt / trade_dt / plan_dt
run_id
source_run_id
schema_version
rule_version
source_manifest_hash
checkpoint_key
```

协议必须裁决：

| 项 | 必须回答 |
|---|---|
| 子库关系 | 哪些库是 source fact、structure fact、semantic ledger、execution ledger、readout ledger |
| 每日增量 | 如何从 source manifest / dirty scope 推导需要重算的范围 |
| 断点续传 | checkpoint / batch ledger / resume mode 如何表达 |
| staging promote | working facts 如何审计后 promote，不允许半成品污染正式账本 |
| 跨库一致性 | 不假设跨库事务原子性，靠 run lineage、manifest、audit 补齐 |
| 统一更新 | 更新数据库时按共同键和 dirty scope 定位影响面 |

本卡已冻结的正式入口：

```text
docs/01-architecture/05-historical-ledger-topology-protocol-v1.md
governance/database_topology_registry.toml
docs/04-execution/records/governance/005-historical-ledger-topology-protocol-card-20260515-01.conclusion.md
```

`daily-incremental-and-resume-protocol-card-20260515-01` 已继续冻结第六卡协议：

```text
docs/01-architecture/06-daily-incremental-and-resume-protocol-v1.md
governance/daily_incremental_protocol_registry.toml
docs/04-execution/records/governance/006-daily-incremental-and-resume-protocol-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段历史大账本拓扑固定为：

```text
Historical ledger = one logical ledger with governed sub-ledgers
Sub-ledgers = source_fact / structure_fact / semantic_ledger / decision_ledger / management_ledger / portfolio_plan_ledger / execution_ledger / readout_ledger / orchestration_ledger
Common keys = symbol / timeframe / bar_dt / trade_dt / plan_dt / run_id / source_run_id / schema_version / rule_version / source_manifest_hash / checkpoint_key
Source manifest = required input ledger binding
Run lineage = required direct-parent proof chain
Cross-ledger consistency = lineage / manifest / audit first
Cross-DB atomicity assumption = not allowed
Runtime / formal DB / broker / profit claims = not authorized
```

本卡通过后，第一阶段每日增量与断点续传裁决固定为：

```text
Daily incremental = source manifest and dirty scope first
Dirty scope = symbol / timeframe / date range / ledger role / reason / lineage bound
Replay boundary = earliest affected date through target as-of date
Checkpoint = batch progress only, bound to dirty scope / manifest / schema / rule / lineage
Resume = resume_strict by default; blocked upstream, audit failed, or lineage gap cannot be skipped
Staging promote = audit passed and lineage complete before formal promote
Runtime / formal DB / broker / profit claims = not authorized
```

## 8. 回测窗口与留出样本协议范围

`backtest-window-and-holdout-protocol-card` 必须进入第一张 roadmap，因为它决定数据账本不能随便回填污染。

当前需求先登记为：

```text
main historical backtest candidate window = 2012..2021
rolling validation style = three-year rolling backtest
historical rolling segments = 2012..2014, 2015..2017, 2018..2020
reserved rolling segment 1 = 2021..2023
reserved rolling segment 2 = 2024..2026
```

本卡已裁决 `2021` 的边界：`2012..2021` 是十年历史覆盖和数据盘点口径，选择、调参和策略筛选
默认只允许使用 `2012..2020`；`2021` 在验证 / 留出意义上归入 `2021..2023` reserved holdout。
因此任何收益 proof 都不得混用训练 / 选择窗口与预留窗口。

本卡已冻结的正式入口：

```text
docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md
governance/backtest_window_holdout_registry.toml
docs/04-execution/records/governance/007-backtest-window-and-holdout-protocol-card-20260515-01.conclusion.md
```

本卡通过后，后续回测必须在历史大账本上运行，并且遵守：

```text
daily incremental update
resume from checkpoint
lineage-preserving rebuild
no holdout leakage
```

本卡通过后，第一阶段回测窗口与留出样本裁决固定为：

```text
Historical coverage = 2012..2021
Selection / tuning / strategy screening window = 2012..2020
Historical rolling segments = 2012..2014 / 2015..2017 / 2018..2020
Reserved holdout segments = 2021..2023 / 2024..2026
2021 boundary = purpose-isolated, holdout side for validation
Runtime / formal DB / broker / profit claims = not authorized
```

## 9. 来源裁决与非迁移规则范围

`source-authority-and-non-migration-rule-card-20260515-01` 已把第一阶段来源分类、
非迁移规则、只读参考边界和 adapter 语义主权边界冻结。

本卡已冻结的正式入口：

```text
docs/00-governance/01-source-authority-and-non-migration-rule-v1.md
governance/source_authority_registry.toml
docs/04-execution/records/governance/008-source-authority-and-non-migration-rule-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段来源裁决固定为：

```text
MALF v1.4 directory and zip = authority anchor
Asteria_System_Design_Set_v1_0 = governance pattern reference
MALF-system-history and G:\malf-history = historical tradeoff reference
MALF-reference and selected historical repos = reference input only
G:\《股市浮沉二十载》 = brainstorming source
G:\《股市浮沉二十载》\2020.(Au)LanceBeggs = PAS concept source
DuckDB / Arrow / Polars / vectorbt / backtesting.py / Qlib / baostock = adapter or research engine only
AKShare = rejected for semantic ownership
Legacy schema / runner / DuckDB surface migration = not authorized
Runtime / formal DB / broker / profit claims = not authorized
```

第 8 卡通过后，live next 推进为：

```text
malf-v1-4-immutability-anchor-card
```

## 10. MALF v1.4 不可变锚点范围

`malf-v1-4-immutability-anchor-card-20260515-01` 已冻结 MALF v1.4 的系统位置、
锚点资产边界、MANIFEST 角色和下游不可重定义不变量。

本卡已冻结的正式入口：

```text
docs/01-architecture/01-malf-v1-4-anchor-position-v1.md
governance/malf_v1_4_immutability_registry.toml
docs/04-execution/records/governance/009-malf-v1-4-immutability-anchor-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段 MALF v1.4 锚点裁决固定为：

```text
MALF v1.4 directory = immutable authority anchor
MALF v1.4 zip = recoverable archive copy
MANIFEST.json = package boundary evidence, not runtime proof
MALF v1.4 = structure fact owner
PAS / Signal / Position / Portfolio Plan / Trade = no MALF rewrite
External adapters / engines = no MALF semantic ownership
Anchor existence = no runtime, formal DB, broker, or profit authorization
Legacy schema / runner / DuckDB surface migration = not authorized
```

第 9 卡通过后，live next 推进为：

```text
predecessor-strength-map-card
```

## 11. 旧系统强项地图范围

`predecessor-strength-map-card-20260515-01` 已冻结旧系统、历史资料、书籍来源与历史 repo 的
可吸收强项、禁止迁移 / 禁止继承边界和后续使用边界。

本卡已冻结的正式入口：

```text
docs/01-architecture/02-predecessor-strength-map-v1.md
governance/predecessor_strength_registry.toml
docs/04-execution/records/governance/010-predecessor-strength-map-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段旧系统强项地图裁决固定为：

```text
MALF v1.4 anchor = immutable structure authority
Asteria_System_Design_Set_v1_0 = governance pattern reference
MALF-system-history / MALF-reference = historical and bridge reference only
G:\《股市浮沉二十载》 = PAS brainstorming source, not runtime or broker source
G:\《股市浮沉二十载》\2020.(Au)LanceBeggs = PAS context / trigger / strength / lifecycle concept source
G:\malf-history and selected historical repos = tradeoff and failure-lesson reference
Legacy code / schema / runner / DuckDB surface migration = not authorized
Runtime / formal DB / broker / profit claims = not authorized
```

第 10 卡通过后，live next 推进为：

```text
pas-axiomatic-state-machine-card
```

## 12. PAS v1.1 三件套设计集范围

`pas-axiomatic-state-machine-card-20260515-01` 已把第 11 卡从“最小状态机”升级为
PAS v1.1 三件套正式设计集冻结。

本卡已冻结的正式入口：

```text
H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1
docs/02-modules/01-pas-axiomatic-state-machine-v1.md
governance/pas_axiomatic_state_machine_registry.toml
docs/04-execution/records/governance/011-pas-axiomatic-state-machine-card-20260515-01.conclusion.md
```

本卡通过后，第一阶段 PAS 裁决固定为：

```text
PAS v1.1 starts from MALF WavePosition, not PriceBar
MALF owns structure
PAS owns opportunity interpretation
Signal owns accept/reject
Position / Trade own management and action
PAS purpose = identify strength / weakness, reject weakness, join strength
PAS output = PASCandidate / PASCandidateLatest / PASLifecycleTrace
PAS forbidden outputs = order / position / fill / profit / broker instruction
Runtime / formal DB / broker / profit claims = not authorized
```

第 11 卡通过后，live next 推进为：

```text
open-source-adapter-boundary-card
```

## 13. 通过标准

| 卡 | 通过标准 |
|---|---|
| `governance-roadmap-freeze-card` | 主落点、远端、阶段边界写死 |
| `repo-governance-environment-bootstrap-card` | 插件、脚本、环境、`.codex`、`.gitignore`、`governance` 的迁入/不迁入边界冻结 |
| `system-mainline-module-ownership-card` | Data -> System 模块顺序、自建/委外边界、Portfolio Plan 保留/轻量化边界冻结 |
| `storage-engine-and-portability-decision-card` | DuckDB、SQLite+Parquet、Hybrid、Go/Python 的角色矩阵冻结 |
| `historical-ledger-topology-protocol-card` | 大账本、子库共同键、run lineage、source manifest 规则冻结 |
| `daily-incremental-and-resume-protocol-card` | 每日增量、dirty scope、checkpoint、resume、staging promote 规则冻结 |
| `backtest-window-and-holdout-protocol-card` | 2012..2021 十年历史窗口、2012-2014 / 2015-2017 / 2018-2020、2021-2023 / 2024-2026 预留三年段边界冻结 |
| `source-authority-and-non-migration-rule-card` | 分类枚举与非迁移规则冻结 |
| `malf-v1-4-immutability-anchor-card` | MALF 锚点与不变量列明 |
| `predecessor-strength-map-card` | 每个主要来源都有可吸收强项与禁止迁移说明 |
| `pas-axiomatic-state-machine-card` | PAS v1.1 三件套设计集、MALF-first Core / Lifecycle / Service、handoff 边界冻结 |
| `open-source-adapter-boundary-card` | 每个主要开源项目都有允许角色与禁止越界说明 |

## 14. 当前结论

```text
This roadmap is legislation-first.
It does not authorize runtime, DB, broker, or strategy claims.
```
