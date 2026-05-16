# Roadmap Ready Development Daily Usability Discipline Evidence Index

日期：2026-05-16

## 1. Evidence Summary

| 资产 | 路径 |
|---|---|
| discipline_doc | `docs/00-governance/05-post-terminal-roadmap-and-module-db-discipline-v1.md` |
| discipline_registry | `governance/post_terminal_roadmap_discipline_registry.toml` |
| repo_registry | `governance/repo_governance_registry.toml` |
| agent_rules | `AGENTS.md` |
| governance_check | `src/malf_pas/governance/checks.py` |
| governance_tests | `tests/governance/test_governance_checks.py` |
| conclusion_index | `docs/04-execution/00-conclusion-index-v1.md` |
| closeout | `docs/04-execution/records/governance/017-roadmap-ready-development-daily-usability-discipline-card-20260516-01.conclusion.md` |
| validated_assets_batch_manifest | `H:\Malf-Pas-backup\validated-core-algorithm-assets-batch-20260516-151211.manifest.json` |
| malf_v1_4_backup_snapshot_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_4-snapshot-20260516-192716.manifest.json` |
| pas_v1_1_backup_snapshot_manifest | `H:\Malf-Pas-backup\PAS__Three_Part_Design_Set_v1_1-snapshot-20260516-192716.manifest.json` |
| roadmap_standalone_zip_manifest | `H:\Malf-Pas-backup\00-malf-pas-governance-roadmap-v1.md.zip.manifest.json` |
| malf_v1_5_standalone_zip_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_5.zip.manifest.json` |
| pas_v1_2_standalone_zip_manifest | `H:\Malf-Pas-backup\PAS__Three_Part_Design_Set_v1_2.zip.manifest.json` |

## 2. Key Frozen Values

| 指标 | 值 |
|---|---|
| discipline_count | `12` |
| development_usable_required_before_next_roadmap | `true` |
| daily_usable_required_before_next_roadmap | `true` |
| development_rule_id | `ROADMAP-READY-REQUIRES-DEVELOPMENT-USABLE` |
| daily_rule_id | `ROADMAP-READY-REQUIRES-DAILY-USABLE` |
| repo_hard_rule_development | `roadmap-ready-requires-development-usable` |
| repo_hard_rule_daily | `roadmap-ready-requires-daily-usable` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `none / terminal` |

## 3. Backup Snapshot Coverage

| asset | backup evidence |
|---|---|
| `MALF_Three_Part_Design_Set_v1_4` | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_4-snapshot-20260516-192716.zip` / SHA256 `95C2613FCAA29AB81BD2C5C30A8E7323D22D098357CE210324325BA31F84209B` |
| `PAS__Three_Part_Design_Set_v1_1` | `H:\Malf-Pas-backup\PAS__Three_Part_Design_Set_v1_1-snapshot-20260516-192716.zip` / SHA256 `1D2776C30728DC6F8BC7AC26CFC231674C1AA58A3140EA49FB9D815A41287C23` |
| `MALF_Three_Part_Design_Set_v1_5` | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_5-snapshot-20260516-151211.zip` |
| `PAS__Three_Part_Design_Set_v1_2` | `H:\Malf-Pas-backup\PAS__Three_Part_Design_Set_v1_2-snapshot-20260516-151211.zip` |
| `MALF_PAS_Scenario_Atlas_v1_0` | `H:\Malf-Pas-backup\MALF_PAS_Scenario_Atlas_v1_0-snapshot-20260516-151211.zip` |
| batch manifest | `H:\Malf-Pas-backup\validated-core-algorithm-assets-batch-20260516-151211.manifest.json` now covers all five validated core authority assets |
| standalone zip manifests | the three retained standalone backup zips now have sibling `.manifest.json` files; snapshot packages remain the preferred recoverable copies |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 负向校验

新增单测覆盖缺失纪律场景：当 `repo_governance_registry.toml` 或
`post_terminal_roadmap_discipline_registry.toml` 缺少 development usable / daily usable
两条 ready 纪律时，governance check 必须产生 finding。

## 6. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `exit 0` |
| `python scripts\governance\check_project_governance.py` | `Malf-Pas governance checks passed.` |
| `python -m unittest discover -s tests -p "test_*.py"` | `Ran 10 tests ... OK` |
| `python -m ruff check src tests scripts` | `All checks passed!` |
