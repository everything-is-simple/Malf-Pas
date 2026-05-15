# Malf-Pas Agent 规则

本仓库是 `Malf-Pas` 新系统的治理先行工作区。

修改任何文件前，每个 agent 必须先读：

1. `README.md`
2. `docs/00-governance/00-malf-pas-reconstruction-charter-v1.md`
3. `docs/00-governance/01-source-authority-and-non-migration-rule-v1.md`
4. `docs/01-architecture/00-mainline-authoritative-map-v1.md`
5. `docs/01-architecture/01-malf-v1-4-anchor-position-v1.md`
6. `docs/01-architecture/03-system-mainline-module-ownership-v1.md`
7. `docs/01-architecture/04-storage-engine-and-portability-decision-v1.md`
8. `docs/01-architecture/05-historical-ledger-topology-protocol-v1.md`
9. `docs/01-architecture/06-daily-incremental-and-resume-protocol-v1.md`
10. `docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md`
11. `docs/00-governance/04-root-directory-policy-v1.md`
12. `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md`
13. `docs/04-execution/00-conclusion-index-v1.md`
14. `governance/repo_governance_registry.toml`
15. `governance/root_directory_registry.toml`
16. `governance/source_authority_registry.toml`

## 当前权威资产

- `H:\Malf-Pas`
- `H:\Malf-Pas-data`
- `H:\Malf-Pas-backup`
- `H:\Malf-Pas-Validated`
- `H:\Malf-Pas-reprot`
- `H:\Malf-Pas-temp`
- `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4`
- `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip`
- `H:\Asteria-Validated\Asteria_System_Design_Set_v1_0`
- `H:\Asteria-Validated\MALF-system-history`
- `H:\Asteria-Validated\MALF-reference`
- `G:\malf-history`
- `G:\《股市浮沉二十载》`
- `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs`

## 硬规则

- 第一阶段是治理文档施工，不是业务模块施工。
- `MALF v1.4` 是固定结构锚点；任何下游不得重定义 MALF。
- 目标模块设计文档冻结前，不得把 legacy code 迁入主线。
- 一次 construction turn 不得并行改写多个业务模块语义。
- `PAS` 不得输出订单、仓位、成交、收益承诺或 broker 指令。
- `Signal` 不得回写 `MALF` 或 `PAS` 定义。
- 正式 DB mutation 当前固定为 `no`。
- broker / live trading / paper-live 当前固定为 `deferred`。
- `H:\Malf-Pas-data` 是当前系统唯一数据根；当前阶段仍不得正式写入。
- `H:\Malf-Pas-backup` 只放备份包、交付 zip 与可恢复快照。
- `H:\Malf-Pas-Validated` 只放本系统沉淀后的历史经验、权威材料与经验索引。
- `H:\Malf-Pas-reprot` 只放 report、audit readout 与运行报告输出；当前目录名固定为 `reprot`。
- `H:\Malf-Pas-temp` 只放临时产物、cache 与 smoke-run scratch。
- 上一版 `H:\Asteria*` 目录只作只读参考，不得作为当前系统 output root 或 scratch。
- `G:\《股市浮沉二十载》` 是 PAS 概念、思路风暴、context/trigger/strength/lifecycle 的来源根；不得解释成运行代码、正式数据或交易指令来源。
- `G:\malf-history` 是曾经做过但未完成的历史版本与模块取舍参考根；可读实现理由、权衡折衷、样本和失败教训，不得迁移旧 schema、runner 或代码表面。
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
- no-formal-db-mutation：不得写入 `*.duckdb`、`*.db`、`*.sqlite`。
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
stage = governance initialization
live next = source-authority-and-non-migration-rule-card
formal DB mutation = no
broker feasibility = deferred
repo status = backtest window and holdout protocol passed
```
