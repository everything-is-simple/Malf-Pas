# Data Module DB Contract Evidence Index

日期：2026-05-17

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `data-module-db-contract-card-20260517-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| contract_registry | `governance/data_module_db_contract_registry.toml` |
| contract_module | `src/malf_pas/data_foundation/contract.py` |
| validator_cli | `scripts/data_foundation/validate_data_contract.py` |
| contract_tests | `tests/data_foundation/test_data_contract.py` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| roadmap_registry | `governance/data_foundation_roadmap_registry.toml` |
| closeout | `docs/04-execution/records/data-foundation/020-data-module-db-contract-card-20260517-01.conclusion.md` |
| formal_db | `not applicable / no DB mutation` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| database_count | `6` |
| table_family_count | `38` |
| raw_ingest_audit | `raw_market.ingest_run / source ingest local audit` |
| module_orchestration_audit | `data_control.run_ledger / module-level orchestration audit` |
| week_month_availability_status | `day-derived` |
| tradability_availability_status | `blocked` |
| current_card_writes_data_root | `false` |
| current_card_creates_db | `false` |
| data_foundation_ready | `false / not claimed` |
| next_data_foundation_card | `raw-market-full-build-ledger-card` |

## 4. 验证入口

```powershell
python scripts\data_foundation\validate_data_contract.py --json
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check src tests scripts
```

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\data_foundation\validate_data_contract.py --json` | `exit 0`，`database_count = 6`，`table_family_count = 38` |
| `python scripts\dev\doctor.py` | `exit 0`，`formal_db_mutation = no` |
| `python scripts\governance\check_project_governance.py` | `Malf-Pas governance checks passed.` |
| `python -m unittest discover -s tests -p "test_*.py"` | `Ran 25 tests ... OK` |
| `python -m ruff check src tests scripts` | `All checks passed!` |
