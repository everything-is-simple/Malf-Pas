# Predecessor Strength Map Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `predecessor-strength-map-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/02-predecessor-strength-map-v1.md` |
| machine_readable_registry | `governance/predecessor_strength_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/010-predecessor-strength-map-card-20260515-01.conclusion.md` |
| source_authority_registry | `governance/source_authority_registry.toml` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_assets | `H:\Asteria* / G:\malf-history / G:\《股市浮沉二十载》 (read-only reference)` |
| report_dir | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| predecessor_strength_map_status | `frozen-by-predecessor-strength-map-card-20260515-01` |
| major_sources_registered | `12` |
| absorbable_strength_registered | `yes` |
| forbidden_migration_registered | `yes` |
| downstream_use_boundary_registered | `yes` |
| legacy_code_migration_authorized | `false` |
| schema_transplant_authorized | `false` |
| runner_transplant_authorized | `false` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `pas-axiomatic-state-machine-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "predecessor-strength-map-card|predecessor_strength_registry|pas-axiomatic-state-machine-card|formal_db_mutation|broker_feasibility|legacy code migration|schema transplant|runner transplant" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
