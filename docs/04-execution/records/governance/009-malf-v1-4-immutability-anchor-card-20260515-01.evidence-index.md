# MALF v1.4 Immutability Anchor Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-v1-4-immutability-anchor-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/01-malf-v1-4-anchor-position-v1.md` |
| machine_readable_registry | `governance/malf_v1_4_immutability_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/009-malf-v1-4-immutability-anchor-card-20260515-01.conclusion.md` |
| anchor_directory | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4 (current authority anchor)` |
| anchor_manifest | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4\MANIFEST.json (package boundary evidence, not runtime proof)` |
| current_anchor_zip | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4.zip` |
| current_anchor_zip_sha256 | `05B0C99170AAE5C1ECA36FC5981829CE397E721F93A5095E32586672D23BBFC7` |
| predecessor_anchor_directory | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4 (read-only predecessor/original reference)` |
| predecessor_anchor_zip | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip (read-only predecessor/original archive)` |
| predecessor_anchor_manifest | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4\MANIFEST.json (read-only predecessor/original reference)` |
| backup_snapshot_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_4-snapshot-20260516-192716.manifest.json` |
| backup_snapshot_zip_sha256 | `95C2613FCAA29AB81BD2C5C30A8E7323D22D098357CE210324325BA31F84209B` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |
| report_dir | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| malf_v1_4_policy_status | `frozen-by-malf-v1-4-immutability-anchor-card-20260515-01` |
| anchor_directory_role | `immutable authority anchor` |
| anchor_zip_role | `authority zip copy; backup_root snapshot is the recoverable package owner` |
| anchor_manifest_role | `package boundary evidence, not runtime proof` |
| structure_fact_owner | `MALF v1.4` |
| downstream_redefinition_authorized | `false` |
| runtime_authorized | `false` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| legacy_schema_migration_authorized | `false` |
| live_next | `predecessor-strength-map-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "malf-v1-4-immutability-anchor-card|malf_v1_4_immutability_registry|predecessor-strength-map-card|runtime_authorized|formal_db_mutation|broker_feasibility|downstream_redefinition_authorized" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
