# Source Authority And Non-Migration Rule Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `source-authority-and-non-migration-rule-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `Malf-Pas` 第一阶段来源分类、来源裁决与非迁移规则。
- 补齐 MALF v1.4、上一版 validated 资产、历史 repo、书籍概念来源和外部 adapter 的分类边界。
- 将 live next 从第 8 卡推进到 `malf-v1-4-immutability-anchor-card`。

## 3. 允许动作

- 修改治理文档、roadmap、结论索引、machine-readable registry 与 execution 四件套。
- 增强 repo-local source authority registry 校验。
- 更新 gate registry 与 repo governance registry 的下一卡状态。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 访问、读取、改写或 promote `H:\Malf-Pas-data`、`H:\Asteria-data` 中的正式数据资产。
- 迁移历史 repo schema、runner、DuckDB 表面、业务语义或旧代码。
- 复制书籍正文，或把书中交易管理动作解释为 PAS 输出动作。
- 新增 runtime、runner、schema migration、broker、paper-live、实盘、仓位、订单、成交或收益证明。

## 5. 通过标准

- 来源分类枚举、主要来源分类、非迁移规则和 adapter 边界冻结。
- `governance/source_authority_registry.toml` 覆盖主要来源，并由 repo-local governance check 校验关键来源。
- roadmap、结论索引、gate registry、repo registry 与 AGENTS 当前状态同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local doctor、governance check、unittest 与 exact authority search 通过。
