# MALF+PAS Scenario Atlas Evidence Index

日期：2026-05-16

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-pas-scenario-atlas-card-20260516-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/02-modules/04-malf-pas-scenario-atlas-v1.md` |
| validated_atlas | `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0` |
| atlas_manifest | `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0\MANIFEST.json` |
| backup_snapshot_manifest | `H:\Malf-Pas-backup\MALF_PAS_Scenario_Atlas_v1_0-snapshot-20260516-151211.manifest.json` |
| validated_assets_batch_manifest | `H:\Malf-Pas-backup\validated-core-algorithm-assets-batch-20260516-151211.manifest.json` |
| machine_readable_registry | `governance/malf_pas_scenario_atlas_registry.toml` |
| current_malf_anchor | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` |
| current_malf_v1_5 | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` |
| current_pas_v1_1 | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` |
| current_pas_v1_2 | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/015-malf-pas-scenario-atlas-card-20260516-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| atlas_status | `companion_authority_asset` |
| atlas_policy_status | `frozen-by-malf-pas-scenario-atlas-card-20260516-01` |
| atlas_files | `7 markdown files + 5 svg files + MANIFEST.json` |
| case_count | `5` |
| visual_format | `Markdown + SVG` |
| historical_reference_policy | `reference only / not proof` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `open-source-adapter-boundary-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check src scripts tests
rg -n "MALF_PAS_Scenario_Atlas_v1_0|malf_pas_scenario_atlas_registry|companion_authority_asset|open-source-adapter-boundary-card|reference only / not proof" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| `python -m ruff check src scripts tests` | `passed` |
| exact authority search | `passed` |
