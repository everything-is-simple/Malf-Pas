# Historical Ledger Topology Protocol Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `historical-ledger-topology-protocol-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `Malf-Pas` 第一阶段的系统大账本拓扑。
- 冻结子库共同治理键、run lineage、source manifest 与分账本规则。
- 明确第 5 卡只定义逻辑协议，不执行正式 DB mutation 或 runtime build。

## 3. 允许动作

- 修改治理文档、architecture 文档、roadmap、结论索引与 execution 四件套。
- 更新 machine-readable database topology registry。
- 更新 gate registry 的当前卡与下一卡状态。
- 只读参考 `H:\Asteria-data` 的数据库根目录与语义索引边界经验。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite`、`*.parquet` 或正式数据根目录。
- 新增 runtime、runner、schema migration、业务模块实现或 legacy code migration。
- 打开 broker、paper-live、实盘、收益证明、订单、仓位或成交回路。
- 把 `H:\Asteria-data` 解释为 `Malf-Pas` 的权威资产根或 scratch 根。

## 5. 通过标准

- historical ledger principle 冻结。
- sub-ledger topology 冻结。
- common governance keys 冻结。
- source manifest protocol 冻结。
- run lineage protocol 冻结。
- cross-ledger consistency rule 冻结。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
