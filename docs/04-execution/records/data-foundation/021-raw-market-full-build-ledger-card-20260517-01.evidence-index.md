# Raw Market Full Build Ledger Evidence Index

日期：2026-05-17

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `raw-market-full-build-ledger-card-20260517-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| closeout_registry | `governance/raw_market_full_build_registry.toml` |
| runtime_module | `src/malf_pas/data_foundation/raw_market.py` |
| build_cli | `scripts/data_foundation/build_raw_market_full_ledger.py` |
| validator_cli | `scripts/data_foundation/validate_raw_market_ledger.py` |
| ledger_tests | `tests/data_foundation/test_raw_market_ledger.py` |
| cli_tests | `tests/data_foundation/test_raw_market_cli.py` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| roadmap_registry | `governance/data_foundation_roadmap_registry.toml` |
| formal_db | `H:\Malf-Pas-data\raw_market.duckdb` |
| report_root | `H:\Malf-Pas-reprot\data-foundation\raw-market-full-build-ledger-card-20260517-01` |
| closeout | `docs/04-execution/records/data-foundation/021-raw-market-full-build-ledger-card-20260517-01.conclusion.md` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| formal_db_created | `true` |
| full_build_manifest_hash | `6d4851273196397bff727aa47ba7b0f5b96a0da6eefa6674b2444e3951821769` |
| latest_manifest_hash | `24b15d9e77c922da7a90a098a9035a57bbd8d0b9b7f0d22a9f7273bee99aa280` |
| current_source_file_rows | `30558` |
| full_build_discovered_source_files | `30556` |
| source_file_revision_rollover_count | `2` |
| raw_bar_rows | `28649022` |
| canonical_file_count | `12196` |
| dual_root_divergence_count | `144743` |
| skipped_unchanged_count | `12196` |
| reject_audit_rows | `156939` |
| source_roots | `H:\tdx_offline_Data = 18261` / `H:\new_tdx64 = 12297` |
| asset_rows | `stock = 22147315` / `index = 2958039` / `block = 3543668` |
| data_foundation_ready | `false / not claimed` |
| next_data_foundation_card | `market-base-day-week-month-build-card` |

## 4. 构建与验证入口

```powershell
python scripts\data_foundation\build_raw_market_full_ledger.py --mode full --db H:/Malf-Pas-data/raw_market.duckdb --report-dir H:/Malf-Pas-reprot/data-foundation/raw-market-full-build-ledger-card-20260517-01/full
python scripts\data_foundation\build_raw_market_full_ledger.py --mode daily_incremental --db H:/Malf-Pas-data/raw_market.duckdb --report-dir H:/Malf-Pas-reprot/data-foundation/raw-market-full-build-ledger-card-20260517-01/daily_incremental
python scripts\data_foundation\validate_raw_market_ledger.py --db H:/Malf-Pas-data/raw_market.duckdb --json
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\data_foundation\build_raw_market_full_ledger.py --mode full ...` | `exit 0`，`source_file_rows = 30556`，`raw_bar_rows = 28649022`，`canonical_file_count = 12196`，`blocked_reject_count = 144743` |
| `python scripts\data_foundation\build_raw_market_full_ledger.py --mode daily_incremental ...` | `exit 0`，`skipped_unchanged_count = 12196`，`blocked_reject_count = 0`，same-input rerun 未新增业务事实 |
| `python scripts\data_foundation\validate_raw_market_ledger.py --db H:/Malf-Pas-data/raw_market.duckdb --json` | `exit 0`，`status = passed`，`raw_bar_row_count = 28649022`，`natural_key_unique = true`，`manifest_binding_complete = true` |
| `python scripts\dev\doctor.py` | `exit 0`，`stage = data-foundation`，`formal_db_mutation = Data Foundation only`，`current_allowed_next_card = market-base-day-week-month-build-card` |
| `python scripts\governance\check_project_governance.py` | `exit 0`，`Malf-Pas governance checks passed.` |
| `python -m unittest discover -s tests -p "test_*.py"` | `exit 0`，全量单测通过 |
