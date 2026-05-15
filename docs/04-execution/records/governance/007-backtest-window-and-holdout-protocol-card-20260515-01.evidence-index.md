# Backtest Window And Holdout Protocol Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `backtest-window-and-holdout-protocol-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md` |
| machine_readable_registry | `governance/backtest_window_holdout_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/007-backtest-window-and-holdout-protocol-card-20260515-01.conclusion.md` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| historical_coverage_window | `2012..2021` |
| selection_window | `2012..2020` |
| rolling_validation_style | `three-year rolling backtest` |
| historical_rolling_segments | `2012..2014 / 2015..2017 / 2018..2020` |
| reserved_holdout_segments | `2021..2023 / 2024..2026` |
| year_2021_boundary | `purpose-isolated` |
| no_holdout_leakage | `required` |
| lineage_preserving_rebuild | `required before future proof` |
| runtime_authorized | `false` |
| profit_proof_authorized | `false` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
rg -n "backtest-window-and-holdout-protocol-card|backtest_window_holdout|07-backtest-window|2012\\.\\.2021|2021\\.\\.2023|2024\\.\\.2026|source-authority-and-non-migration-rule-card" README.md AGENTS.md docs governance pyproject.toml
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| exact authority search | `passed` |
