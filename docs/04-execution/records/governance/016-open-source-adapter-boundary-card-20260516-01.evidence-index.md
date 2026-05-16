# Open-Source Adapter Boundary Evidence Index

日期：2026-05-16

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `open-source-adapter-boundary-card-20260516-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/08-open-source-adapter-boundary-v1.md` |
| machine_readable_registry | `governance/open_source_adapter_boundary_registry.toml` |
| source_authority_doc | `docs/00-governance/01-source-authority-and-non-migration-rule-v1.md` |
| source_authority_registry | `governance/source_authority_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| module_gate | `governance/module_gate_registry.toml` |
| repo_registry | `governance/repo_governance_registry.toml` |
| closeout | `docs/04-execution/records/governance/016-open-source-adapter-boundary-card-20260516-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| adapter_role_count | `5` |
| project_count | `5` |
| AKShare_policy | `reference_or_experimental_input_only + rejected_for_semantic_ownership` |
| global_forbidden_boundary | `no semantic ownership / no formal truth ownership / no broker or profit authority` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |
| current_allowed_next_card | `""` |
| governance_roadmap_state | `none / terminal` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "none / terminal|open_source_adapter_boundary_registry|current_allowed_next_card = \"\"" README.md AGENTS.md docs governance pyproject.toml src tests
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
