# Daily Incremental And Resume Protocol Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `daily-incremental-and-resume-protocol-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/06-daily-incremental-and-resume-protocol-v1.md` |
| machine_readable_registry | `governance/daily_incremental_protocol_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/006-daily-incremental-and-resume-protocol-card-20260515-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| daily_incremental_principle | `source manifest and dirty scope first` |
| dirty_scope_protocol | `frozen` |
| checkpoint_protocol | `frozen` |
| resume_modes | `resume_strict / resume_replan / restart_from_manifest / audit_only / no_op_audited` |
| staging_promote_protocol | `audit passed and lineage complete before promote` |
| replay_boundary | `earliest affected date through target as-of date` |
| runtime_authorized | `false` |
| staging_promote_authorized_now | `false` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "daily-incremental-and-resume-protocol-card|daily_incremental_protocol|06-daily-incremental|backtest-window-and-holdout-protocol-card" README.md AGENTS.md docs governance pyproject.toml
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
