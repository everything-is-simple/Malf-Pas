# Market Meta Tradability Calendar Evidence Index

日期：2026-05-17

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-meta-tradability-calendar-card-20260517-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| closeout_registry | `governance/market_meta_tradability_calendar_registry.toml` |
| static_parser | `src/malf_pas/data_foundation/tdx_meta.py` |
| runtime_module | `src/malf_pas/data_foundation/market_meta.py` |
| build_cli | `scripts/data_foundation/build_market_meta_tradability_calendar.py` |
| validator_cli | `scripts/data_foundation/validate_market_meta_tradability_calendar.py` |
| ledger_tests | `tests/data_foundation/test_market_meta_ledger.py` |
| cli_tests | `tests/data_foundation/test_market_meta_cli.py` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| roadmap_registry | `governance/data_foundation_roadmap_registry.toml` |
| meta_db | `H:\Malf-Pas-data\market_meta.duckdb` |
| report_root | `H:\Malf-Pas-reprot\data-foundation\market-meta-tradability-calendar-card-20260517-01` |
| closeout | `docs/04-execution/records/data-foundation/023-market-meta-tradability-calendar-card-20260517-01.conclusion.md` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| source_manifest_hash | `fab73a6078b5571cca76306ad28cc076587d8c9c741f4404e2e47e1ba22903d8` |
| raw_source_manifest_hash | `24b15d9e77c922da7a90a098a9035a57bbd8d0b9b7f0d22a9f7273bee99aa280` |
| day_source_manifest_hash | `24b15d9e77c922da7a90a098a9035a57bbd8d0b9b7f0d22a9f7273bee99aa280` |
| bounded_symbol_scope | `bj920000 / bj920001 / bj920002 / bj920003 / bj920005` |
| bounded_instrument_rows | `5` |
| bounded_tradability_rows | `2777` |
| bounded_unresolved_gap_count | `4178` |
| full_instrument_rows | `7669` |
| full_trade_calendar_rows | `18676` |
| full_tradability_rows | `19212175` |
| full_relation_rows | `7898` |
| block_relation_rows | `2390` |
| industry_relation_rows | `5508` |
| trade_calendar_span | `1990-12-19 .. 2026-04-23` |
| instrument_list_dt_span | `1990-12-01 .. 2026-04-03` |
| tradability_unresolved_symbol_count | `7669` |
| tradability_unresolved_gap_count | `44854914` |
| tradability_policy | `tdx_direct_only / no_inferred_negative_facts` |
| snapshot_policy | `industry_block_relation = current-snapshot-only` |
| next_data_foundation_card | `data-control-run-ledger-checkpoint-card` |
| data_foundation_ready | `false / not claimed` |

## 4. 构建与验证入口

```powershell
python scripts\data_foundation\build_market_meta_tradability_calendar.py --mode bounded --raw-db H:/Malf-Pas-data/raw_market.duckdb --day-db H:/Malf-Pas-data/market_base_day.duckdb --meta-db H:/Malf-Pas-temp/market_meta.bounded.duckdb --hq-cache-root H:/new_tdx64/T0002/hq_cache --blocknew-root H:/new_tdx64/T0002/blocknew --report-dir H:/Malf-Pas-reprot/data-foundation/market-meta-tradability-calendar-card-20260517-01/bounded --limit-symbols 5
python scripts\data_foundation\build_market_meta_tradability_calendar.py --mode full --raw-db H:/Malf-Pas-data/raw_market.duckdb --day-db H:/Malf-Pas-data/market_base_day.duckdb --meta-db H:/Malf-Pas-data/market_meta.duckdb --hq-cache-root H:/new_tdx64/T0002/hq_cache --blocknew-root H:/new_tdx64/T0002/blocknew --report-dir H:/Malf-Pas-reprot/data-foundation/market-meta-tradability-calendar-card-20260517-01
python scripts\data_foundation\validate_market_meta_tradability_calendar.py --meta-db H:/Malf-Pas-data/market_meta.duckdb --json
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\data_foundation\build_market_meta_tradability_calendar.py --mode bounded ... --limit-symbols 5` | `exit 0`，`status = passed`，`instrument = 5`，`tradability = 2777`，`unresolved_gap_count = 4178` |
| `python scripts\data_foundation\build_market_meta_tradability_calendar.py --mode full ...` | `exit 0`，`status = passed`，`instrument = 7669`，`calendar = 18676`，`tradability = 19212175`，`relation = 7898` |
| `python scripts\data_foundation\validate_market_meta_tradability_calendar.py --meta-db ... --json` | `exit 0`，`status = passed`，六表族齐全，四类自然键唯一，`lineage_complete = true` |
| `python scripts\dev\doctor.py` | 待本轮 closeout 后复跑 |
| `python scripts\governance\check_project_governance.py` | 待本轮 closeout 后复跑 |
| `python -m unittest discover -s tests -p "test_*.py"` | 待本轮 closeout 后复跑 |
