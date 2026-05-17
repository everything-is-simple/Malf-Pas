# Local TDX Source Inventory Evidence Index

日期：2026-05-17

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `local-tdx-source-inventory-card-20260517-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| source_inventory_cli | `scripts/data_foundation/inventory_local_tdx_sources.py` |
| source_inventory_module | `src/malf_pas/data_foundation/source_inventory.py` |
| inventory_registry | `governance/local_tdx_source_inventory_registry.toml` |
| roadmap_registry | `governance/data_foundation_roadmap_registry.toml` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| source_inventory_tests | `tests/data_foundation/test_source_inventory.py` |
| closeout | `docs/04-execution/records/data-foundation/019-local-tdx-source-inventory-card-20260517-01.conclusion.md` |
| formal_db | `not applicable / no DB mutation` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| current_truth_roots | `H:\tdx_offline_Data`, `H:\new_tdx64` |
| previous_reference_root | `H:\Asteria-data` |
| previous_reference_role | `reference_baseline_only` |
| previous_data_dbs_checked | `raw_market`, `market_base_day`, `market_base_week`, `market_base_month`, `market_meta` |
| week_month_availability_status | `day-derived` |
| tradability_availability_status | `blocked` |
| current_card_writes_data_root | `false` |
| current_card_creates_db | `false` |
| next_data_foundation_card | `data-module-db-contract-card` |

## 4. 验证入口

```powershell
python scripts\data_foundation\inventory_local_tdx_sources.py --json
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check src tests scripts
```

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\data_foundation\inventory_local_tdx_sources.py --json` | `exit 0` |
| `python scripts\dev\doctor.py` | `exit 0`，`formal_db_mutation = no` |
| `python scripts\governance\check_project_governance.py` | `Malf-Pas governance checks passed.` |
| `python -m unittest discover -s tests -p "test_*.py"` | `Ran 18 tests ... OK` |
| `python -m ruff check src tests scripts` | `All checks passed!` |
