# Data Module DB Contract Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `data-module-db-contract-card-20260517-01` |
| roadmap_order | `020` |
| card type | `Data Foundation contract freeze / validator skeleton` |

## 2. 本次目标

- 冻结 Data Foundation 六库 contract、表族、自然键、共同治理键与 lineage 字段。
- 冻结 `raw_market.ingest_run` 与 `data_control.run_ledger` 的关系。
- 冻结 `data_control` orchestration table families 与 freshness/readout table families 的分离边界。
- 交付 Data validator 最小骨架与 CLI entrypoint。
- 建立第 20 卡 repo-local execution 四件套与 conclusion index 入口。

## 3. 允许动作

- 新增 `governance/data_module_db_contract_registry.toml`。
- 新增 `src/malf_pas/data_foundation/contract.py` 与 `scripts/data_foundation/validate_data_contract.py`。
- 新增 Data contract 单测与治理检查测试。
- 同步 `pyproject.toml`、`governance/repo_governance_registry.toml`、`governance/data_foundation_roadmap_registry.toml`、README、docs README、AGENTS、governance README、Roadmap 2 与 conclusion index。

## 4. 禁止动作

- 不创建 `raw_market.duckdb`、`market_base_day.duckdb`、`market_base_week.duckdb`、`market_base_month.duckdb`、`market_meta.duckdb` 或 `data_control.duckdb`。
- 不写入 `H:\Malf-Pas-data`。
- 不迁移上一版 Asteria schema、runner、DuckDB 表面或旧代码。
- 不让 Data 输出 MALF / PAS / Signal / Position / Trade / System 语义。
- 不进入 broker、paper-live、backtest、收益证明或 live trading。

## 5. 通过标准

- 六库 contract、表族、自然键、治理键、schema_version、rule_version、source manifest 与 lineage 字段全部冻结。
- `run_id` 不进入 bar 类业务事实自然键，只保留为 audit / lineage / checkpoint 线索。
- `raw_market.ingest_run` 明确为 source ingest 局部审计，`data_control.run_ledger` 明确为 Data module-level orchestration 审计。
- `data_control` orchestration table families 与 freshness/readout table families 保持分离。
- `tradability` 当前保持 `blocked`；若后续补来源，必须登记 authorized `source_adapter`。
- Data validator CLI、repo-local doctor、governance check、unittest 与 Ruff 全部通过。
