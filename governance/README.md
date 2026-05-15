# Malf-Pas 机器可读治理层

本目录预留给后续 machine-readable governance artifacts，例如：

```text
module registries
storage engine registries
API contracts
database topology
historical ledger registries
```

第一阶段不在此目录定义正式 runtime 合同。`module_ownership_registry.toml` 只冻结模块语义所有权，
不授权 runtime、正式 DB mutation、broker 或收益证明。

`storage_engine_registry.toml` 只冻结 DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色，
不授权正式存储切换或便携 runtime。

`database_topology_registry.toml` 只冻结历史大账本、子库共同键、source manifest、run lineage 与分账本规则，
不授权正式 DB mutation、schema migration、runtime、broker 或收益证明。
