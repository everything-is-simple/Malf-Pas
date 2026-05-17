# Market Base Day Week Month Build Evidence Index

日期：2026-05-17

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-base-day-week-month-build-card-20260517-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| closeout_registry | `governance/market_base_day_week_month_registry.toml` |
| runtime_module | `src/malf_pas/data_foundation/market_base.py` |
| build_cli | `scripts/data_foundation/build_market_base_day_week_month.py` |
| validator_cli | `scripts/data_foundation/validate_market_base_day_week_month.py` |
| ledger_tests | `tests/data_foundation/test_market_base_ledger.py` |
| cli_tests | `tests/data_foundation/test_market_base_cli.py` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| roadmap_registry | `governance/data_foundation_roadmap_registry.toml` |
| day_db | `H:\Malf-Pas-data\market_base_day.duckdb` |
| week_db | `H:\Malf-Pas-data\market_base_week.duckdb` |
| month_db | `H:\Malf-Pas-data\market_base_month.duckdb` |
| report_root | `H:\Malf-Pas-reprot\data-foundation\market-base-day-week-month-build-card-20260517-01` |
| closeout | `docs/04-execution/records/data-foundation/022-market-base-day-week-month-build-card-20260517-01.conclusion.md` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| source_manifest_hash | `24b15d9e77c922da7a90a098a9035a57bbd8d0b9b7f0d22a9f7273bee99aa280` |
| raw_source_run_id | `raw-market-full-build-ledger-card-20260517-01` |
| day_run_id | `market-base-day-week-month-build-card-20260517-01:day` |
| week_run_id | `market-base-day-week-month-build-card-20260517-01:week` |
| month_run_id | `market-base-day-week-month-build-card-20260517-01:month` |
| bounded_symbol_scope | `bj430017 / bj430047 / bj430090 / bj430139 / bj430198` |
| bounded_day_rows | `4720` |
| bounded_week_rows | `998` |
| bounded_month_rows | `237` |
| full_day_rows | `28649022` |
| full_week_rows | `6071205` |
| full_month_rows | `1454045` |
| day_symbol_count | `12194` |
| week_symbol_count | `12194` |
| month_symbol_count | `12194` |
| day_date_span | `1990-12-19 .. 2026-04-23` |
| week_date_span | `1990-12-20 .. 2026-04-23` |
| month_date_span | `1990-12-25 .. 2026-04-23` |
| analysis_price_line | `backward` |
| week_month_lineage | `day-derived` |
| full_rerun_growth | `0 / same-input rerun did not inflate rows` |
| data_foundation_ready | `false / not claimed` |
| next_data_foundation_card | `market-meta-tradability-calendar-card` |

## 4. 构建与验证入口

```powershell
python scripts\data_foundation\build_market_base_day_week_month.py --mode bounded --raw-db H:/Malf-Pas-data/raw_market.duckdb --day-db H:/Malf-Pas-temp/market_base_day.bounded.duckdb --week-db H:/Malf-Pas-temp/market_base_week.bounded.duckdb --month-db H:/Malf-Pas-temp/market_base_month.bounded.duckdb --report-dir H:/Malf-Pas-reprot/data-foundation/market-base-day-week-month-build-card-20260517-01/bounded --limit-symbols 5
python scripts\data_foundation\build_market_base_day_week_month.py --mode full --raw-db H:/Malf-Pas-data/raw_market.duckdb --day-db H:/Malf-Pas-data/market_base_day.duckdb --week-db H:/Malf-Pas-data/market_base_week.duckdb --month-db H:/Malf-Pas-data/market_base_month.duckdb --report-dir H:/Malf-Pas-reprot/data-foundation/market-base-day-week-month-build-card-20260517-01/full
python scripts\data_foundation\build_market_base_day_week_month.py --mode full --raw-db H:/Malf-Pas-data/raw_market.duckdb --day-db H:/Malf-Pas-data/market_base_day.duckdb --week-db H:/Malf-Pas-data/market_base_week.duckdb --month-db H:/Malf-Pas-data/market_base_month.duckdb --report-dir H:/Malf-Pas-reprot/data-foundation/market-base-day-week-month-build-card-20260517-01/full-rerun
python scripts\data_foundation\validate_market_base_day_week_month.py --day-db H:/Malf-Pas-data/market_base_day.duckdb --week-db H:/Malf-Pas-data/market_base_week.duckdb --month-db H:/Malf-Pas-data/market_base_month.duckdb --json
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\data_foundation\build_market_base_day_week_month.py --mode bounded ... --limit-symbols 5` | `exit 0`，`status = passed`，`day = 4720`，`week = 998`，`month = 237` |
| `python scripts\data_foundation\build_market_base_day_week_month.py --mode full ...` | `exit 0`，`status = passed`，`day = 28649022`，`week = 6071205`，`month = 1454045` |
| `python scripts\data_foundation\build_market_base_day_week_month.py --mode full ... full-rerun` | `exit 0`，同输入二次 full build 后 row count 未膨胀 |
| `python scripts\data_foundation\validate_market_base_day_week_month.py --day-db ... --json` | `exit 0`，`status = passed`，三库 `natural_key_unique = true`、`latest_pointer_unique = true`、`lineage_complete = true` |
| `python scripts\dev\doctor.py` | 待本轮 closeout 后复跑 |
| `python scripts\governance\check_project_governance.py` | 待本轮 closeout 后复跑 |
| `python -m unittest discover -s tests -p "test_*.py"` | 待本轮 closeout 后复跑 |
