# Storage Engine And Portability Decision Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `storage-engine-and-portability-decision-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色矩阵。
- 明确 Go 可携带运行只是后续候选，不替代当前 Python 研究生态。
- 明确未经独立 proof，不得把任何候选直接提升为正式存储。

## 3. 允许动作

- 修改治理文档、architecture 文档、roadmap、结论索引与 execution 四件套。
- 新增 machine-readable storage engine registry。
- 更新 gate registry 的当前卡与下一卡状态。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 新增 runtime、runner、schema migration、Go binary、业务模块实现或 legacy code migration。
- 打开 broker、paper-live、实盘、收益证明、订单、仓位或成交回路。
- 将 DuckDB、SQLite、Parquet、Go 或 Python 任一技术栈解释成业务语义 owner。

## 5. 通过标准

- `storage_role_matrix` 冻结。
- `portable_runtime_boundary` 冻结。
- `python_research_boundary` 冻结。
- `go_distribution_candidate_boundary` 冻结。
- `no_storage_switch_without_proof` 冻结。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
