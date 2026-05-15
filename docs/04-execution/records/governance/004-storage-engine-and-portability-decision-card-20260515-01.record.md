# Storage Engine And Portability Decision Record

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `storage-engine-and-portability-decision-card-20260515-01` |
| result | `passed` |

## 2. 执行顺序

1. 复核 `README.md`、`AGENTS.md`、重构总纲、来源裁决、主线权威图、MALF 锚点、roadmap、结论索引和 repo registry。
2. 确认当前 live next 为 `storage-engine-and-portability-decision-card`。
3. 新增 storage engine / portability 裁决文档，冻结 DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色。
4. 新增 machine-readable storage engine registry。
5. 更新 roadmap、docs entry、governance README、pyproject、repo registry、gate registry 和结论索引。
6. 建立第四卡 execution 四件套，并将下一卡推进到 `historical-ledger-topology-protocol-card`。

## 3. 关键验证

| 验证 | 结果 |
|---|---|
| authority docs reviewed before edit | `passed` |
| storage_role_matrix frozen | `passed` |
| portable_runtime_boundary frozen | `passed` |
| python_research_boundary frozen | `passed` |
| go_distribution_candidate_boundary frozen | `passed` |
| no_storage_switch_without_proof frozen | `passed` |
| dev doctor | `passed` |
| project governance check | `passed` |
| governance tests | `passed` |
| formal DB artifact created | `no` |
| runtime implementation created | `no` |

## 4. 外部证据资产

| 资产 | 路径 |
|---|---|
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |

## 5. 文档更新

- `docs/README.md`
- `AGENTS.md`
- `docs/01-architecture/04-storage-engine-and-portability-decision-v1.md`
- `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
- `docs/04-execution/records/governance/004-storage-engine-and-portability-decision-card-20260515-01.*`
- `governance/README.md`
- `governance/module_gate_registry.toml`
- `governance/repo_governance_registry.toml`
- `governance/storage_engine_registry.toml`
- `pyproject.toml`
