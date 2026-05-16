# PAS Axiomatic State Machine Evidence Index

日期：2026-05-16

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `pas-axiomatic-state-machine-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/02-modules/01-pas-axiomatic-state-machine-v1.md` |
| validated_design_set | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` |
| design_manifest | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1\MANIFEST.json` |
| machine_readable_registry | `governance/pas_axiomatic_state_machine_registry.toml` |
| current_malf_anchor | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` |
| predecessor_malf_reference | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/011-pas-axiomatic-state-machine-card-20260515-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| pas_design_set_status | `authority_definition` |
| pas_policy_status | `frozen-by-pas-axiomatic-state-machine-card-20260515-01` |
| design_files | `8 markdown files + MANIFEST.json` |
| extra_pas_07_created | `no` |
| pas_starts_from | `MALF WavePosition` |
| pas_does_not_start_from | `PriceBar` |
| malf_owns_structure | `true` |
| pas_owns_opportunity_interpretation | `true` |
| signal_owns_accept_reject | `true` |
| position_trade_own_action | `true` |
| religion | `identify strength / weakness; reject weakness; join strength` |
| lifecycle_states_frozen | `observing / forming / waiting / triggered / cancelled / modified / invalidated / reentry_candidate / submitted_to_signal / accepted_by_signal / rejected_by_signal` |
| setup_families_frozen | `TST / BOF / BPB / PB / CPB` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| live_next | `open-source-adapter-boundary-card` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "PAS__Three_Part_Design_Set_v1_1|pas_axiomatic_state_machine_registry|reject weakness|join strength|MALF owns structure|formal_db_mutation|broker_feasibility|open-source-adapter-boundary-card" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
