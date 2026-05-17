# Malf-Pas 机器可读治理层

## Normative registry terms

| registry | role |
|---|---|
| `environment_bootstrap_registry.toml` | freezes repo-local workflow skeleton, hook, script, virtualenv, and governance-environment bootstrap boundary |
| `repo_governance_registry.toml` | freezes repo-wide stage, hard rules, required docs, required plugin files, and current governance-roadmap state |
| `root_directory_registry.toml` | freezes the six current roots plus previous/external read-only root boundaries |
| `source_authority_registry.toml` | freezes authority, predecessor, successor, companion, reference, and adapter-source roles plus non-migration boundaries |
| `post_terminal_roadmap_discipline_registry.toml` | freezes post-terminal roadmap discipline, including development usable and daily usable ready gates |
| `data_foundation_roadmap_registry.toml` | freezes Roadmap 2 handoff, Data Foundation-only scope, and card 18 no-downstream authorization boundary |
| `data_module_db_contract_registry.toml` | freezes Data Foundation six-DB contract, table families, natural keys, lineage, and validator skeleton boundary |
| `raw_market_full_build_registry.toml` | records card 21 raw-market full-build closeout, formal DB path, report root, and live counts for source/raw/audit tables |
| `market_base_day_week_month_registry.toml` | records card 22 market-base day/week/month closeout, three formal DB paths, report root, and live counts / uniqueness / lineage status |

本目录预留给后续 machine-readable governance artifacts，例如：

```text
module registries
storage engine registries
API contracts
database topology
historical ledger registries
root directory registries
source authority registries
```

第一阶段不在此目录定义正式 runtime 合同。`module_ownership_registry.toml` 只冻结模块语义所有权，
不授权 runtime、正式 DB mutation、broker 或收益证明。

`storage_engine_registry.toml` 只冻结 DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色，
不授权正式存储切换或便携 runtime。

`database_topology_registry.toml` 只冻结历史大账本、子库共同键、source manifest、run lineage 与分账本规则，
不授权正式 DB mutation、schema migration、runtime、broker 或收益证明。

`daily_incremental_protocol_registry.toml` 只冻结每日增量、dirty scope、checkpoint、resume 与
staging promote 的治理协议，不授权正式 DB mutation、schema migration、runtime、broker 或收益证明。

`post_terminal_roadmap_discipline_registry.toml` 冻结首张治理 roadmap 收口后的后续路线纪律。
每张模块 roadmap 宣告 ready 前，必须同时证明开发可用与日常可用；只够下游开发、不够日常增量、
断点续传和 freshness/audit 的模块库，不得推进下一张 roadmap。

`data_foundation_roadmap_registry.toml` 冻结系统第二张 roadmap 的接力关系：第一张治理 roadmap
保持 `none / terminal`，第二张 roadmap 只对应 `Data Foundation` 模块数据库边界。第 18 卡不创建 DB，
不写入 `H:\Malf-Pas-data`，只把后续 Data 卡可申请的范围收窄为 `Data Foundation only`。

`data_module_db_contract_registry.toml` 冻结第 20 卡的 Data 六库 contract、表族、自然键、
共同治理键、manifest / lineage 和最小 validator 骨架。本 registry 不创建 DB，不写入
`H:\Malf-Pas-data`，也不授权 MALF / PAS / Signal runtime。

`raw_market_full_build_registry.toml` 冻结第 21 卡的 `raw_market` 文件级历史账本闭环结果。
它登记 canonical root、secondary audit root、`raw_market.duckdb` 正式路径、报告路径、full build
与 daily incremental 的 manifest/hash 结果，以及 `source_file / raw_bar / reject_audit` 的 live row counts。

`market_base_day_week_month_registry.toml` 冻结第 22 卡的 `market_base_day/week/month` 物化账本闭环结果。
它登记三库正式路径、报告路径、row count、symbol count、date span、natural key / latest pointer 唯一性，
以及 week/month 当前仍为 `day-derived` 的 lineage 结论。

`backtest_window_holdout_registry.toml` 只冻结 `2012..2021` 历史覆盖、`2012..2020` 选择窗口、
三年滚动段、`2021..2023 / 2024..2026` reserved holdout 与 `2021` 用途隔离边界，
不授权回测执行、正式 DB mutation、runtime、broker 或收益证明。

`root_directory_registry.toml` 只冻结 `Malf-Pas` 六根目录和上一版 `Asteria` 只读参考边界，
不授权创建 DB、写入正式数据根、迁移旧运行产物或复用上一版 scratch。

`source_authority_registry.toml` 只冻结 MALF authority anchor、`G:\《股市浮沉二十载》` 书籍/思路风暴来源、
`G:\malf-history` 历史版本取舍参考与非迁移边界，不授权旧代码迁移、书籍正文复制、runtime 或 broker。

`malf_v1_4_immutability_registry.toml` 只冻结 MALF v1.4 锚点目录、归档、MANIFEST 与下游不可重定义不变量，
不授权 runtime、正式 DB mutation、schema migration、broker 或收益证明。

`predecessor_strength_registry.toml` 只冻结旧系统、历史资料、书籍来源与历史 repo 的可吸收强项、
禁止迁移边界和后续使用边界，不授权旧代码、旧 schema、runner、DuckDB 表面、runtime、正式 DB mutation、
broker 或收益证明。
