# Predecessor Strength Map Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `predecessor-strength-map-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结旧系统、历史资料、书籍来源与历史 repo 的可吸收强项。
- 明确每个主要来源的禁止迁移 / 禁止继承边界。
- 建立 `governance/predecessor_strength_registry.toml`，用机器可读治理层固定后续使用边界。
- 将 live next 从第 10 卡推进到 `pas-axiomatic-state-machine-card`。

## 3. 允许动作

- 修改旧系统强项地图、roadmap、结论索引、machine-readable registry 与 execution 四件套。
- 增强 repo-local governance check，校验 predecessor strength registry。
- 更新 gate registry 与 repo governance registry 的下一卡状态。
- 只读参考上一版 `H:\Asteria*`、`G:\malf-history` 和 `G:\《股市浮沉二十载》` 的来源边界。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 迁移历史 repo 代码、旧 schema、runner、queue、checkpoint、DuckDB 表面或 pipeline 行为。
- 复制书籍正文进 repo，或把书籍交易管理动作直接解释成 PAS 输出动作。
- 新增 runtime、runner、schema migration、broker、paper-live、实盘、仓位、订单、成交或收益证明。
- 把旧版本未完工状态、历史回测结果或旧报告解释成当前系统完成证据。

## 5. 通过标准

- `docs/01-architecture/02-predecessor-strength-map-v1.md` 状态冻结到第 10 卡 run_id。
- 每个主要来源都有 `可吸收强项`、`禁止迁移 / 禁止继承` 和 `后续使用边界`。
- `governance/predecessor_strength_registry.toml` 登记主要来源、分类、强项、禁令与下游用法。
- repo-local governance check 校验 predecessor strength registry。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest 与 exact authority search 通过。
