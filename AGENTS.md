# Malf-Pas Agent 规则

本仓库是 `Malf-Pas` 新系统的治理先行工作区。

修改任何文件前，每个 agent 必须先读：

1. `README.md`
2. `docs/00-governance/00-malf-pas-reconstruction-charter-v1.md`
3. `docs/00-governance/01-source-authority-and-non-migration-rule-v1.md`
4. `docs/00-governance/02-execution-record-protocol-v1.md`
5. `docs/00-governance/03-repo-governance-environment-bootstrap-v1.md`
6. `docs/00-governance/05-post-terminal-roadmap-and-module-db-discipline-v1.md`
7. `docs/01-architecture/00-mainline-authoritative-map-v1.md`
8. `docs/01-architecture/01-malf-v1-4-anchor-position-v1.md`
9. `docs/01-architecture/03-system-mainline-module-ownership-v1.md`
10. `docs/01-architecture/04-storage-engine-and-portability-decision-v1.md`
11. `docs/01-architecture/05-historical-ledger-topology-protocol-v1.md`
12. `docs/01-architecture/06-daily-incremental-and-resume-protocol-v1.md`
13. `docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md`
14. `docs/01-architecture/08-open-source-adapter-boundary-v1.md`
15. `docs/00-governance/04-root-directory-policy-v1.md`
16. `docs/02-modules/02-malf-v1-5-wave-behavior-snapshot-v1.md`
17. `docs/02-modules/03-pas-v1-2-strength-weakness-matrix-v1.md`
18. `docs/02-modules/04-malf-pas-scenario-atlas-v1.md`
19. `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md`
20. `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md`
21. `docs/04-execution/README.md`
22. `docs/04-execution/00-conclusion-index-v1.md`
23. `governance/repo_governance_registry.toml`
24. `governance/root_directory_registry.toml`
25. `governance/source_authority_registry.toml`
26. `governance/post_terminal_roadmap_discipline_registry.toml`（治理纪律 `12` 条）

## 当前权威资产

- `H:\Malf-Pas`
- `H:\Malf-Pas-data`
- `H:\Malf-Pas-backup`
- `H:\Malf-Pas-Validated`
- `H:\Malf-Pas-reprot`
- `H:\Malf-Pas-temp`
- `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4`（current authority anchor）
- `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1`（current PAS predecessor authority）
- `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5`（successor authority design set；已由第13卡冻结）
- `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2`（successor authority design set；已由第14卡冻结）
- `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0`（frozen companion atlas；已由第15卡冻结）
- `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4`（predecessor/original reference）
- `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip`（predecessor/original archive）
- `H:\Asteria-Validated\Asteria_System_Design_Set_v1_0`
- `H:\Asteria-Validated\MALF-system-history`
- `H:\Asteria-Validated\MALF-reference`
- `G:\malf-history`
- `G:\《股市浮沉二十载》`
- `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs`

## 硬规则

- 首张治理路线图已收口；当前 live route 是 `Data Foundation` 窄授权施工，不是下游业务模块施工。
- `MALF v1.4` 是固定结构锚点；任何下游不得重定义 MALF。
- 目标模块设计文档冻结前，不得把 legacy code 迁入主线。
- 一次 construction turn 不得并行改写多个业务模块语义。
- `PAS` 不得输出订单、仓位、成交、收益承诺或 broker 指令。
- `Signal` 不得回写 `MALF` 或 `PAS` 定义。
- 正式 DB mutation 当前固定为 `Data Foundation only`，且 live write scope 只到 `H:\Malf-Pas-data\market_base_day.duckdb / market_base_week.duckdb / market_base_month.duckdb / market_meta.duckdb`。
- broker / live trading / paper-live 当前固定为 `deferred`。
- `H:\Malf-Pas-data` 是当前系统唯一数据根；当前 live 授权只允许写入 `market_base_day.duckdb / market_base_week.duckdb / market_base_month.duckdb / market_meta.duckdb`，其他正式 DB 仍不得写入。
- `H:\Malf-Pas-backup` 只放备份包、交付 zip 与可恢复快照。
- `H:\Malf-Pas-Validated` 只放本系统沉淀后的历史经验、权威材料与经验索引。
- `H:\Malf-Pas-reprot` 只放 report、audit readout 与运行报告输出；当前目录名固定为 `reprot`。
- `H:\Malf-Pas-temp` 只放临时产物、cache 与 smoke-run scratch。
- 上一版 `H:\Asteria*` 目录只作只读参考，不得作为当前系统 output root 或 scratch。
- `G:\《股市浮沉二十载》` 是 PAS 概念、思路风暴、context/trigger/strength/lifecycle 的来源根；不得解释成运行代码、正式数据或交易指令来源。
- `G:\malf-history` 是曾经做过但未完成的历史版本与模块取舍参考根；可读实现理由、权衡折衷、样本和失败教训，不得迁移旧 schema、runner 或代码表面。
- 首张治理 roadmap 收口后，后续工作必须新开独立 roadmap，不得继续占用 `none / terminal` 的路线图。
- 每一张后续 roadmap 必须只对应一个模块数据库或一个模块账本边界。
- 当前模块数据库未建好、未通过检查、未形成闭环前，不得开启下一张 roadmap。
- 每张后续 roadmap 宣告 ready 前必须同时做到 `development_usable = true` 与 `daily_usable = true`；只够后续开发、不够日常使用，不得叫 ready。
- `development_usable` 必须证明下游可稳定消费 contract、schema、manifest、lineage 和最小接口，不得靠临时 mock 或猜 schema。
- `daily_usable` 必须证明本模块具备 ledger、daily incremental 或显式等价机制、dirty scope、checkpoint/resume、freshness/audit 闭环；若模块天然不需要 daily incremental，必须写明替代日常维护机制。
- `Data` 之后的核心兵力优先投入 `MALF -> PAS -> Signal`。
- 正式输入真值优先来自 `H:\tdx_offline_Data` 与 `H:\new_tdx64`。
- `TuShare / baostock / AKShare` 不得成为正式 truth owner。
- mock 只能用于 `unit test / contract test / proof harness`，不得冒充正式 truth。
- `H:\Asteria-data` 只能作为 `Data Foundation` bootstrap 只读参考，不得成为当前 output root 或 scratch。
- 后续各模块数据库都属于同一个历史大账本的受治理分账本，不得被理解成散库集合。
- 任何模块 roadmap 都必须先通过 doc / registry / doctor / governance / unittest 检查，才能推进下一步。
- repo 根目录不得落缓存、临时 DB、临时报告或运行产物。

## 工具顺序

固定顺序为：

```text
codebase-retrieval -> context7 -> fetch -> sequential-thinking -> codex apps
```

本地 exact search 只在 repo 语义检索之后用于穷尽已知字符串。

## 施工规则

- doc-first：先写或修正文档，再谈实现。
- governance-only：第一张 roadmap 期间只允许治理卡与说明文档施工。
- read-only-to-previous-assets：可读上一版 `H:\Asteria*` 与历史资料，不得改写它们。
- data-foundation-only-formal-db-mutation：当前只允许 `H:\Malf-Pas-data\market_base_day.duckdb / market_base_week.duckdb / market_base_month.duckdb / market_meta.duckdb`；其他 `*.duckdb`、`*.db`、`*.sqlite` 仍不得写入。
- no-legacy-code-migration：不得把历史 repo 代码原样搬入本仓库。

## 执行闭环

- 每张卡后续都必须具备 `card / evidence-index / record / conclusion` 四件套。
- 四件套文件名必须使用三位 roadmap 顺序号前缀，例如 `001-<run_id>.card.md`。
- `docs/04-execution/00-conclusion-index-v1.md` 是 repo 内结论索引入口。
- 没有四件套，不得宣告闭环完成。
- blocked 卡也必须 truthful 落档，不得用 roadmap 代替结论。
- 每张卡的 `conclusion` 必须固定包含一段 `人话版结论`，说明完成了什么、没做什么、下一步是什么。

## repo-local 治理检查

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

`plugins/malf-pas-workflow` 是本仓库 workflow skeleton；任何 hook、脚本或技能规则都不得保留
`H:\Asteria` 的执行路径。

## 当前阶段口径

```text
stage = post-terminal roadmap 2 data-foundation card 23 closed
live next = data-control-run-ledger-checkpoint-card
formal DB mutation = Data Foundation only
broker feasibility = deferred
repo status = roadmap 1 terminal + roadmap 2 active-after-card-023
first day work = closed
current roadmap = docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md
next Data Foundation card = data-control-run-ledger-checkpoint-card
```
