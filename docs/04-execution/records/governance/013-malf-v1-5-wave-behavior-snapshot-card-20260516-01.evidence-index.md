# MALF v1.5 Wave Behavior Snapshot Evidence Index

日期：2026-05-16

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-v1-5-wave-behavior-snapshot-card-20260516-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/02-modules/02-malf-v1-5-wave-behavior-snapshot-v1.md` |
| validated_design_set | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` |
| design_manifest | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5\MANIFEST.json` |
| backup_snapshot_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_5-snapshot-20260516-151211.manifest.json` |
| validated_assets_batch_manifest | `H:\Malf-Pas-backup\validated-core-algorithm-assets-batch-20260516-151211.manifest.json` |
| standalone_zip_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_5.zip.manifest.json` |
| machine_readable_registry | `governance/malf_v1_5_wave_behavior_snapshot_registry.toml` |
| current_malf_anchor | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` |
| predecessor_malf_reference | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/013-malf-v1-5-wave-behavior-snapshot-card-20260516-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| malf_v1_5_status | `successor_authority_definition` |
| malf_v1_5_policy_status | `frozen-by-malf-v1-5-wave-behavior-snapshot-card-20260516-01` |
| design_files | `9 markdown files + MANIFEST.json` |
| malf_v1_4_anchor_changed | `no` |
| wave_behavior_snapshot_facets | `continuation / stagnation / transition / birth_quality / boundary_pressure / directional_continuity` |
| malf_outputs_only | `WavePosition + WaveBehaviorSnapshot` |
| strength_score_added | `no` |
| setup_family_added | `no` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `pas-v1-2-strength-weakness-matrix-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "MALF_Three_Part_Design_Set_v1_5|malf_v1_5_wave_behavior_snapshot_registry|wave_behavior_snapshot|WaveBehaviorSnapshot|pas-v1-2-strength-weakness-matrix-card|formal_db_mutation|broker_feasibility" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
