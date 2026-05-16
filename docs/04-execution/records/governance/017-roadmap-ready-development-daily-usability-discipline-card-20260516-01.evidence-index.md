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

## 3. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 4. 负向校验

新增单测覆盖缺失纪律场景：当 `repo_governance_registry.toml` 或
`post_terminal_roadmap_discipline_registry.toml` 缺少 development usable / daily usable
两条 ready 纪律时，governance check 必须产生 finding。

## 5. 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `exit 0` |
| `python scripts\governance\check_project_governance.py` | `Malf-Pas governance checks passed.` |
| `python -m unittest discover -s tests -p "test_*.py"` | `Ran 7 tests ... OK` |
| `python -m ruff check src tests scripts` | `All checks passed!` |
