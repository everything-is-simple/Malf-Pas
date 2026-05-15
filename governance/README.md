# Malf-Pas 机器可读治理层

本目录预留给后续 machine-readable governance artifacts，例如：

```text
module registries
storage engine registries
API contracts
database topology
historical ledger registries
root directory registries
source authority registries
```

第一阶段不在此目录定义正式 runtime 合同。`module_ownership_registry.toml` 只冻结模块语义所有权，
不授权 runtime、正式 DB mutation、broker 或收益证明。

`storage_engine_registry.toml` 只冻结 DuckDB、SQLite、Parquet、Hybrid、Python、Go 的第一阶段角色，
不授权正式存储切换或便携 runtime。

`database_topology_registry.toml` 只冻结历史大账本、子库共同键、source manifest、run lineage 与分账本规则，
不授权正式 DB mutation、schema migration、runtime、broker 或收益证明。

`daily_incremental_protocol_registry.toml` 只冻结每日增量、dirty scope、checkpoint、resume 与
staging promote 的治理协议，不授权正式 DB mutation、schema migration、runtime、broker 或收益证明。

`backtest_window_holdout_registry.toml` 只冻结 `2012..2021` 历史覆盖、`2012..2020` 选择窗口、
三年滚动段、`2021..2023 / 2024..2026` reserved holdout 与 `2021` 用途隔离边界，
不授权回测执行、正式 DB mutation、runtime、broker 或收益证明。

`root_directory_registry.toml` 只冻结 `Malf-Pas` 六根目录和上一版 `Asteria` 只读参考边界，
不授权创建 DB、写入正式数据根、迁移旧运行产物或复用上一版 scratch。

`source_authority_registry.toml` 只冻结 MALF authority anchor、`G:\《股市浮沉二十载》` 书籍/思路风暴来源、
`G:\malf-history` 历史版本取舍参考与非迁移边界，不授权旧代码迁移、书籍正文复制、runtime 或 broker。
