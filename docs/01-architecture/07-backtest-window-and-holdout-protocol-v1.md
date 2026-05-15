# Backtest Window And Holdout Protocol v1

日期：2026-05-15

状态：frozen-by-backtest-window-and-holdout-protocol-card-20260515-01

## 1. 目标

本文件冻结 `Malf-Pas` 第一阶段的回测窗口、三年滚动验证与留出样本边界。

本卡只定义治理协议，不运行回测，不读取或写入正式数据库，不证明收益，不授权 runtime build、
broker、paper-live 或 live trading。

## 2. Window Principle

回测窗口是历史大账本上的治理边界，不是策略收益结论。

| 原则 | 裁决 |
|---|---|
| historical coverage window | `2012..2021` |
| model selection window | `2012..2020` |
| rolling validation style | `three-year rolling backtest` |
| holdout policy | `reserved segments must not be used for selection or tuning` |
| 2021 boundary | `purpose-isolated reserved boundary` |
| formal DB mutation | `no` |
| broker feasibility | `deferred` |

`2012..2021` 可以作为十年历史覆盖口径和数据盘点口径，但不得被解释成 2021 可以参与模型选择、
调参、策略筛选或收益叙事。选择、调参与筛选默认只能落在 `2012..2020`。

## 3. Rolling Segments

第一阶段冻结以下三年段：

| segment_id | years | segment_type | allowed role | forbidden role |
|---|---|---|---|---|
| `historical_rolling_2012_2014` | `2012..2014` | `historical_rolling` | 结构化历史回测候选段 | 直接生成收益承诺 |
| `historical_rolling_2015_2017` | `2015..2017` | `historical_rolling` | 结构化历史回测候选段 | 直接生成收益承诺 |
| `historical_rolling_2018_2020` | `2018..2020` | `historical_rolling` | 结构化历史回测候选段 | 直接生成收益承诺 |
| `reserved_holdout_2021_2023` | `2021..2023` | `reserved_holdout` | 留出验证、泄漏检查和后续独立 proof 候选 | 参与选择、调参或策略筛选 |
| `reserved_holdout_2024_2026` | `2024..2026` | `reserved_holdout` | 后续二级留出验证和未来样本边界 | 参与选择、调参或策略筛选 |

`2021..2023` 与 `2024..2026` 当前只冻结为 reserved holdout 段。没有独立卡批准前，
不得用这两个预留段产出策略收益结论、broker 结论或 production readiness 结论。

## 4. 2021 Boundary Decision

`2021` 的边界固定为 `purpose-isolated`：

| 问题 | 裁决 |
|---|---|
| 是否属于十年历史覆盖口径 | `yes, coverage only` |
| 是否可用于模型选择 / 调参 / 策略筛选 | `no` |
| 是否归入 reserved holdout 段 | `yes, 2021..2023` |
| 是否允许双重使用 | `no` |

这意味着：后续文档可以说系统覆盖 `2012..2021` 十年历史样本，但任何选择、调参、筛选、
规则挑选、阈值选择和策略叙事都必须把 `2021` 当作 holdout 起点处理。

## 5. No Holdout Leakage Protocol

后续任何回测、研究 proof 或读出，如果触达 reserved holdout 段，必须先证明：

1. 选择、调参和筛选没有使用 `2021..2023` 或 `2024..2026`。
2. source manifest、dirty scope、checkpoint、run lineage 与 rule_version 能证明窗口边界。
3. `2021` 没有因为十年覆盖口径被混入选择窗口。
4. holdout 读出只作为独立验证，不反向改写上游规则。
5. reserved holdout 结果不得被写成 broker、订单、仓位、成交或收益承诺。

无法证明以上条件时，结果必须判定为 `blocked` 或 `research-only`，不得登记为 formal proof passed。

## 6. Historical Ledger Binding

后续回测必须建立在已冻结的历史大账本与每日增量协议上：

```text
source_manifest
-> dirty_scope
-> checkpoint / resume
-> lineage-preserving rebuild
-> window-bounded readout
```

窗口边界必须绑定以下治理字段：

| field | 规则 |
|---|---|
| `window_id` | 稳定窗口标识 |
| `segment_id` | 三年段或覆盖段标识 |
| `segment_type` | `historical_coverage / selection_window / historical_rolling / reserved_holdout` |
| `start_year` | 窗口起始年份 |
| `end_year` | 窗口结束年份 |
| `allowed_use` | 当前允许用途 |
| `forbidden_use` | 当前禁止用途 |
| `source_manifest_hash` | 输入集合指纹 |
| `rule_version` | 规则版本 |
| `run_id` | 当前 run |
| `source_run_id` | 直接上游 run |

没有 manifest、lineage、checkpoint 和 window metadata 的回测读出，不得作为正式结论。

## 7. Non-Goals

本卡不做以下事项：

- 不运行回测。
- 不读取或写入 `H:\Malf-Pas-data`。
- 不读取或改写 `H:\Asteria-data`。
- 不创建 `*.duckdb`、`*.db`、`*.sqlite`。
- 不实现 runner、schema migration 或 runtime。
- 不证明收益、不输出 broker / paper-live / live trading 结论。
- 不把 `vectorbt`、`backtesting.py`、`Qlib` 或任何外部 engine 提升为语义 owner。

## 8. Invariants

| invariant_id | invariant |
|---|---|
| `BACKTEST-WINDOW-GOVERNANCE-ONLY` | 回测窗口卡只冻结治理边界，不运行回测或证明收益 |
| `HISTORICAL-COVERAGE-2012-2021` | `2012..2021` 是历史覆盖口径 |
| `SELECTION-WINDOW-2012-2020` | 选择、调参和策略筛选默认只允许 `2012..2020` |
| `YEAR-2021-PURPOSE-ISOLATED` | `2021` 可作为覆盖口径末年，但验证用途归入 `2021..2023` reserved holdout |
| `RESERVED-HOLDOUT-NO-SELECTION` | `2021..2023` 与 `2024..2026` 不得参与选择、调参或策略筛选 |
| `NO-HOLDOUT-LEAKAGE` | 后续 proof 必须证明 holdout 没有泄漏 |
| `LINEAGE-PRESERVING-REBUILD-REQUIRED` | 回测必须能从 manifest、dirty scope、checkpoint 与 lineage 证明窗口边界 |
| `NO-FORMAL-DB-MUTATION` | 当前阶段不得写入正式 DB 或正式数据根目录 |
