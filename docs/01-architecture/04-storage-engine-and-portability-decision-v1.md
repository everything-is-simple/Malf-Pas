# Storage Engine And Portability Decision v1

日期：2026-05-15

状态：frozen-by-storage-engine-and-portability-decision-card-20260515-01

## 1. 目标

本文件冻结 `Malf-Pas` 第一阶段对存储引擎、便携运行和研究环境的角色裁决。

本卡只裁决治理边界，不切换正式存储，不写入正式数据库，不授权 runtime build。

## 2. Storage Role Matrix

| 面 | 第一阶段角色 | 裁决 | 禁止越界 |
|---|---|---|---|
| `DuckDB` | research / proof 默认候选 | 继续适合作为本地分析、列式扫描、多表审计和研究查询 adapter | 不得因为既有经验而成为正式 truth owner；不得绕过后续 proof 直接固化为正式存储 |
| `SQLite` | portable manifest / checkpoint / run ledger 候选 | 适合 Go 便携发行时承载轻量账本、manifest、checkpoint、run audit 元数据 | 当前不得替代正式 DB；不得承载 MALF / PAS / Signal 语义定义权 |
| `Parquet` | portable columnar fact 候选 | 适合长期列式事实文件、跨语言读取和静态归档 proof | 当前不得单独充当事务账本；不得在无 manifest / lineage 时成为正式事实 |
| `SQLite + Parquet` | Go 可携带发行候选 | 作为后续便携运行的重点候选组合：SQLite 管账本元数据，Parquet 管列式事实 | 未经独立 proof 不得替代 DuckDB research surface 或正式存储 |
| `Hybrid` | 重点评估候选 | SQLite 管 manifest / checkpoint / run ledger，Parquet 管列式事实，DuckDB 作为研究查询 adapter | 当前只是裁决方向，不是 schema freeze 或 runtime 实现 |
| `Python` | 当前研究主环境 | 继续承载研究、proof、生态集成、审计脚本和治理检查 | 不得被 Go 便携目标提前替代 |
| `Go compiled binary` | 后续便携发行目标 | 预留为离线分发、轻量读出、可携带运行和部署简化方向 | 当前不得输出 broker、订单、仓位、收益承诺或正式运行闭环 |

## 3. Portable Runtime Boundary

便携运行当前只被定义为后续目标，不是第一阶段授权事项。

| 项 | 裁决 |
|---|---|
| runtime implementation | `not authorized` |
| formal DB mutation | `no` |
| Go binary | `candidate only` |
| portable storage switch | `not authorized without independent proof` |
| broker / paper-live | `deferred` |

未来若启动便携运行 proof，必须先具备：

1. 模块设计文档冻结。
2. 历史大账本与每日增量协议冻结。
3. storage proof 四件套。
4. repo-local validation 通过。
5. 结论索引登记。

## 4. Python Research Boundary

Python 当前继续作为研究与 proof 主环境。

允许使用：

- repo-local governance checks。
- proof / audit 脚本。
- DuckDB / Arrow / Polars 等 research adapter。
- 文档与 registry 一致性校验。

禁止解释为：

- 正式 runtime 已授权。
- 正式 DB 可以写入。
- Python 环境已经等于生产发行环境。
- research proof 可以替代模块合同冻结。

## 5. Go Distribution Candidate Boundary

Go 的地位是便携发行候选，不是当前施工目标。

允许保留的方向：

- 单文件或少依赖离线读出。
- SQLite manifest / checkpoint / run ledger 读取。
- Parquet columnar facts 读取。
- System Readout 或 audit reader 的后续候选实现。

当前禁止：

- 在第一阶段新增 Go runtime。
- 用 Go 改写业务语义。
- 让 Go binary 输出 broker 指令、订单、仓位、成交或收益承诺。
- 绕过 Python research proof 直接进入可交易闭环。

## 6. No Storage Switch Without Proof

本卡冻结以下不变量：

| invariant_id | invariant |
|---|---|
| `STORAGE-ROLE-MATRIX-FROZEN` | DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色已冻结 |
| `NO-STORAGE-SWITCH-WITHOUT-PROOF` | 未经独立 proof，不得把任何候选直接提升为正式存储 |
| `NO-FORMAL-DB-MUTATION` | 当前阶段不得写入 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录 |
| `PYTHON-RESEARCH-FIRST` | Python 仍是研究、proof 和生态集成主环境 |
| `GO-PORTABLE-CANDIDATE-ONLY` | Go compiled binary 只是后续便携发行候选 |
| `HYBRID-CANDIDATE-ONLY` | Hybrid 只是后续重点评估方向，不是当前 schema 或 runtime |

## 7. 后续卡影响

`historical-ledger-topology-protocol-card` 可以基于本卡继续细化：

```text
SQLite = manifest / checkpoint / run ledger candidate
Parquet = columnar facts candidate
DuckDB = research query adapter candidate
Python = research / proof environment
Go = portable distribution candidate
```

但第五卡仍不得直接执行正式存储切换；它只能冻结历史大账本拓扑、共同键和 lineage 规则。
