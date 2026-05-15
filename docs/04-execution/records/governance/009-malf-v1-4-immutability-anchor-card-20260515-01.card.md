# MALF v1.4 Immutability Anchor Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-v1-4-immutability-anchor-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `MALF v1.4` 在 `Malf-Pas` 第一阶段中的系统位置。
- 明确 MALF v1.4 目录、zip 与 `MANIFEST.json` 的锚点角色。
- 建立 `governance/malf_v1_4_immutability_registry.toml`，用机器可读治理层锁定不可变不变量。
- 将 live next 从第 9 卡推进到 `predecessor-strength-map-card`。

## 3. 允许动作

- 修改 MALF anchor 文档、roadmap、结论索引、machine-readable registry 与 execution 四件套。
- 增强 repo-local governance check，校验 MALF v1.4 immutability registry。
- 更新 gate registry 与 repo governance registry 的下一卡状态。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 访问、读取、改写或 promote `H:\Malf-Pas-data`、`H:\Asteria-data` 中的正式数据资产。
- 迁移历史 repo schema、runner、DuckDB 表面、业务语义或旧代码。
- 重新定义 MALF v1.4、创建新 MALF schema 或执行 MALF runtime proof。
- 新增 runtime、runner、schema migration、broker、paper-live、实盘、仓位、订单、成交或收益证明。

## 5. 通过标准

- `docs/01-architecture/01-malf-v1-4-anchor-position-v1.md` 状态冻结到第 9 卡 run_id。
- `governance/malf_v1_4_immutability_registry.toml` 登记锚点目录、zip、MANIFEST 和关键禁令。
- repo-local governance check 校验 MALF v1.4 immutability registry。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest 与 exact authority search 通过。
