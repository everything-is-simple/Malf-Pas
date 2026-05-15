# System Mainline Module Ownership Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `system-mainline-module-ownership-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/03-system-mainline-module-ownership-v1.md` |
| machine_readable_registry | `governance/module_ownership_registry.toml` |
| updated_mainline_map | `docs/01-architecture/00-mainline-authoritative-map-v1.md` |
| closeout | `docs/04-execution/records/governance/003-system-mainline-module-ownership-card-20260515-01.conclusion.md` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| module_order_frozen | `Data Foundation -> MALF v1.4 -> PAS -> Signal -> Position -> Portfolio Plan -> Trade -> System Readout` |
| pipeline_role | `orchestration ledger only` |
| semantic_ownership | `self-owned` |
| external_role | `adapter / engine only` |
| portfolio_plan_boundary | `retained independent lightweight layer` |
| runtime_implementation | `not authorized` |
| formal_db_mutation | `no` |
| broker_feasibility | `deferred` |

## 4. 验证入口

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 验证结果

| 验证 | 结果 |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
