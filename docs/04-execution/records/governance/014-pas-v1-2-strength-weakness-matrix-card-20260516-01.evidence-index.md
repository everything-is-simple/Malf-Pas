# PAS v1.2 Strength Weakness Matrix Evidence Index

日期：2026-05-16

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `pas-v1-2-strength-weakness-matrix-card-20260516-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/02-modules/03-pas-v1-2-strength-weakness-matrix-v1.md` |
| validated_design_set | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` |
| design_manifest | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2\MANIFEST.json` |
| machine_readable_registry | `governance/pas_v1_2_strength_weakness_matrix_registry.toml` |
| current_malf_anchor | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` |
| current_malf_v1_5 | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` |
| predecessor_pas_reference | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/014-pas-v1-2-strength-weakness-matrix-card-20260516-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| pas_v1_2_status | `successor_authority_definition` |
| pas_v1_2_policy_status | `frozen-by-pas-v1-2-strength-weakness-matrix-card-20260516-01` |
| design_files | `9 markdown files + MANIFEST.json` |
| pas_v1_1_rewritten | `no` |
| malf_v1_5_rewritten | `no` |
| read_statuses | `strong / weak / mixed / ambiguous / not_applicable` |
| setup_postures | `favored / allowed / deferred / blocked` |
| matrix_service_surfaces | `PASStrengthWeaknessMatrix / PASStrengthWeaknessMatrixLatest` |
| candidate_surface_retains_summary_only | `yes` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `malf-pas-scenario-atlas-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check src scripts tests
rg -n "PAS__Three_Part_Design_Set_v1_2|pas_v1_2_strength_weakness_matrix_registry|PASStrengthWeaknessMatrix|strength_weakness_matrix|WaveBehaviorSnapshot|malf-pas-scenario-atlas-card" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| `python -m ruff check src scripts tests` | `passed` |
| exact authority search | `passed` |
