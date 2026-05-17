# Market Base Day Week Month Build Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-base-day-week-month-build-card-20260517-01` |
| roadmap_order | `022` |
| card type | `Data Foundation market_base materialized base ledger build` |

## 2. 本次目标

- 建立 `market_base_day.duckdb`、`market_base_week.duckdb`、`market_base_month.duckdb` 三个正式基础行情物化账本。
- 把 `base_bar / latest_pointer / base_run / dirty_scope / source_manifest / schema_version` 落进三库。
- 固定 `market_base_day.base_bar.analysis_price_line = backward`。
- 固定 `market_base_week/month.base_bar.derived_from_timeframe = day`，并让 `source_run_id` 直接指向本次 `:day` 子 run。
- 交付 `build_market_base_day_week_month.py` 与 `validate_market_base_day_week_month.py` 两个 CLI。
- 建立第 22 卡四件套、closeout registry 与 conclusion index 入口。

## 3. 允许动作

- 新增 `src/malf_pas/data_foundation/market_base.py`，实现 day 构建、week/month 聚合、validator 与 report 输出。
- 新增 `scripts/data_foundation/build_market_base_day_week_month.py` 与 `scripts/data_foundation/validate_market_base_day_week_month.py`。
- 新增 market-base 单测、CLI 测试与治理检查测试。
- 写入 `H:\Malf-Pas-data\market_base_day.duckdb`、`H:\Malf-Pas-data\market_base_week.duckdb`、`H:\Malf-Pas-data\market_base_month.duckdb`。
- 输出 report 到 `H:\Malf-Pas-reprot\data-foundation\market-base-day-week-month-build-card-20260517-01\`。
- 同步 `governance/market_base_day_week_month_registry.toml`、README、docs README、AGENTS、Roadmap 2、conclusion index 与第 22 卡四件套。

## 4. 禁止动作

- 不创建或写入 `market_meta.duckdb`、`data_control.duckdb`，也不提前打开 `tradability`、checkpoint/resume orchestration 或 freshness/readout。
- 不接 direct `week / month` source；当前 live 结论继续保持 `day-derived`。
- 不迁移上一版 Asteria schema、runner、DuckDB 表面或旧数据。
- 不把 `TuShare / baostock / AKShare` 升级为正式 truth owner。
- 不进入 MALF / PAS / Signal runtime、broker、paper-live、backtest、收益证明或 live trading。

## 5. 通过标准

- `market_base_day/week/month.duckdb` 已创建，且三库的 `base_bar / latest_pointer / base_run / dirty_scope / source_manifest / schema_version` 全部存在。
- day/week/month 的 row count、symbol count、日期跨度可审计。
- `latest_pointer` 唯一，自然键唯一，lineage 完整。
- `market_base_day.base_bar` 固定包含 `analysis_price_line = backward`。
- `market_base_week/month.base_bar` 固定包含 `derived_from_timeframe = day`，且 `source_run_id` 直接指向本次 `:day` 子 run。
- 同一输入再次 full build 不膨胀业务事实。
- 本卡不夸大为 Data Foundation ready，也不替代后续 `market_meta` / `data_control` 的模块级闭环。
