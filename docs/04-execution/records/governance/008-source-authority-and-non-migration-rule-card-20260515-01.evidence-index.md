# Source Authority And Non-Migration Rule Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `source-authority-and-non-migration-rule-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/00-governance/01-source-authority-and-non-migration-rule-v1.md` |
| machine_readable_registry | `governance/source_authority_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/008-source-authority-and-non-migration-rule-card-20260515-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| source_authority_policy_status | `frozen-by-source-authority-and-non-migration-rule-card-20260515-01` |
| malf_v1_4_anchor | `authority_anchor` |
| book_root | `brainstorming_source` |
| lance_beggs_concept_root | `concept_source` |
| malf_history_root | `historical_tradeoff_reference` |
| selected_historical_repos | `reference_input` |
| external_engines | `adapter_candidate / rejected_for_semantic_ownership` |
| legacy_code_migration | `not authorized` |
| schema_runner_duckdb_surface_transplant | `not authorized` |
| runtime_authorized | `false` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `malf-v1-4-immutability-anchor-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "source-authority-and-non-migration-rule-card|source-authority-and-non-migration-rule-card-20260515-01|malf-v1-4-immutability-anchor-card|source_authority_registry|legacy code migration|schema transplant|runner transplant" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
