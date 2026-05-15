# Repo Governance Environment Bootstrap Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `repo-governance-environment-bootstrap-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| report_dir | `not applicable` |
| closeout | `docs/04-execution/records/governance/repo-governance-environment-bootstrap-card-20260515-01.conclusion.md` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| workflow_plugin_skeleton | `plugins/malf-pas-workflow` |
| governance_check_script | `scripts/governance/check_project_governance.py` |
| dev_doctor_script | `scripts/dev/doctor.py` |
| environment_config | `pyproject.toml` / `environment.yml` |
| machine_readable_governance | `governance/*.toml` |
| ignore_rules | `.gitignore` |
| agent_rules | `AGENTS.md` |
| repo_entry | `README.md` |
| codex_repo_boundary | `.codex/README.md` / `.codex/skills/malf-pas-governance/SKILL.md` |
| repo_local_virtualenv | `H:\Malf-Pas\.venv` recreated locally with Python 3.11 editable dev install |
| copied_virtualenv | `no` |
| copied_business_runtime | `no` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```
