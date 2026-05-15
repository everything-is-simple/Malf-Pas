# Historical Ledger Topology Protocol Evidence Index

日期：2026-05-15

## 1. 基本信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `historical-ledger-topology-protocol-card-20260515-01` |
| status | `passed` |

## 2. 资产入口

| 资产 | 路径 |
|---|---|
| authority_doc | `docs/01-architecture/05-historical-ledger-topology-protocol-v1.md` |
| machine_readable_registry | `governance/database_topology_registry.toml` |
| roadmap_entry | `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md` |
| closeout | `docs/04-execution/records/governance/005-historical-ledger-topology-protocol-card-20260515-01.conclusion.md` |
| read_only_reference | `H:\Asteria-data` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 3. 关键结果

| 指标 | 值 |
|---|---|
| historical_ledger_principle | `one logical historical ledger with governed sub-ledgers` |
| sub_ledger_topology | `frozen` |
| common_governance_keys | `frozen` |
| source_manifest_protocol | `frozen` |
| run_lineage_protocol | `frozen` |
| cross_ledger_consistency | `lineage / manifest / audit first` |
| cross_db_atomicity_assumption | `false` |
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
