# MALF+PAS Revision Roadmap Evidence Index

日期：2026-05-16

## 1. Evidence Summary

| 资产 | 路径 |
|---|---|
| roadmap | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| machine_readable_registry | `governance/malf_pas_revision_roadmap_registry.toml` |
| governance_check | `src/malf_pas/governance/checks.py` |
| repo_registry | `governance/repo_governance_registry.toml` |
| module_gate_registry | `governance/module_gate_registry.toml` |
| conclusion_index | `docs/04-execution/00-conclusion-index-v1.md` |
| closeout | `docs/04-execution/records/governance/012-malf-pas-revision-roadmap-card-20260516-01.conclusion.md` |

## 2. Planned Successor Assets

| 资产 | 状态 |
|---|---|
| `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` | planned by card 13, not created by card 12 |
| `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` | planned by card 14, not created by card 12 |
| `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0` | planned by card 15, not created by card 12 |

## 3. Verification Commands

| command | result |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| `python -m ruff check src scripts tests` | `passed` |
| exact authority search | `passed` |

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "MALF_Three_Part_Design_Set_v1_5|PAS__Three_Part_Design_Set_v1_2|wave_behavior_snapshot|strength_weakness_matrix|malf-pas-scenario-atlas-card|open-source-adapter-boundary-card" README.md AGENTS.md docs governance pyproject.toml src tests
```
