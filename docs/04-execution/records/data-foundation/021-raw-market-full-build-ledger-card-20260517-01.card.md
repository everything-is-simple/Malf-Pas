# Raw Market Full Build Ledger Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `raw-market-full-build-ledger-card-20260517-01` |
| roadmap_order | `021` |
| card type | `Data Foundation raw ledger build / first authorized formal DB mutation` |

## 2. 本次目标

- 建立 `raw_market` 文件级历史账本，并把 `source_file / raw_bar / ingest_run / reject_audit / source_manifest / schema_version` 落进正式 `DuckDB`。
- 只 ingest 本地 TDX direct `day` bars；canonical root 固定为 `H:\tdx_offline_Data`，`H:\new_tdx64` 只做补缺和差异审计。
- 交付 `build_raw_market_full_ledger.py` 与 `validate_raw_market_ledger.py` 两个 CLI。
- 证明 `full / bounded / audit-only / resume / daily_incremental` 模式边界可运行，且 `skipped_unchanged` 审计成立。
- 建立第 21 卡四件套、closeout registry 与 conclusion index 入口。

## 3. 允许动作

- 新增 `src/malf_pas/data_foundation/raw_market.py`，实现 source discovery、TDX `*.day` parser、schema writer、audit orchestration。
- 新增 `scripts/data_foundation/build_raw_market_full_ledger.py` 与 `scripts/data_foundation/validate_raw_market_ledger.py`。
- 新增 raw-market 单测、CLI 测试与治理检查测试。
- 写入 `H:\Malf-Pas-data\raw_market.duckdb`。
- 输出 report 到 `H:\Malf-Pas-reprot\data-foundation\raw-market-full-build-ledger-card-20260517-01\`。
- 同步 `governance/raw_market_full_build_registry.toml`、README、docs README、AGENTS、Roadmap 2、conclusion index 与第 21 卡四件套。

## 4. 禁止动作

- 不创建 `market_base_day.duckdb`、`market_base_week.duckdb`、`market_base_month.duckdb`、`market_meta.duckdb` 或 `data_control.duckdb`。
- 不把 `week / month`、`tradability`、`data_control`、`MALF / PAS / Signal` runtime 提前带进第 21 卡。
- 不迁移上一版 Asteria schema、runner、DuckDB 表面或旧数据。
- 不把 `TuShare / baostock / AKShare` 升级为正式 truth owner。
- 不进入 broker、paper-live、backtest、收益证明或 live trading。

## 5. 通过标准

- `raw_market.duckdb` 已创建，且 `source_file / raw_bar / ingest_run / reject_audit / source_manifest / schema_version` 全部存在。
- `raw_bar` 自然键唯一，manifest 绑定完整。
- `source_file` 覆盖两套 truth roots 下全部可读 source family；`raw_bar` 仅 ingest direct `day` bars。
- dual-root divergence、failed/rejected、skipped_unchanged 均可审计。
- 同一输入重跑不重复写业务事实；`daily_incremental` 可以形成 no-op audited closeout。
- 本卡不夸大为 Data Foundation ready，也不替代 `data_control.run_ledger` 的 module-level orchestration 审计。
