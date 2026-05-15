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
| anchor_directory | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4 (read-only reference)` |
| anchor_zip | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip (read-only reference)` |
| anchor_manifest | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4\MANIFEST.json (read-only reference)` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |
| report_dir | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| malf_v1_4_policy_status | `frozen-by-malf-v1-4-immutability-anchor-card-20260515-01` |
| anchor_directory_role | `immutable authority anchor` |
| anchor_zip_role | `recoverable archive copy` |
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
