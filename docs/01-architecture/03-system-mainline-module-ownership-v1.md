# System Mainline Module Ownership v1

日期：2026-05-15

状态：active / ownership-freeze

## 1. 目标

本文件冻结 `system-mainline-module-ownership-card` 的结果：从 `Data Foundation` 到 `System Readout`
的主线顺序、语义所有权、自建边界、外部 adapter / engine 边界。

本文件不授权 runtime、正式数据库写入、broker、paper-live、收益证明或 legacy code migration。

## 2. 主线顺序

```text
Data Foundation
-> MALF v1.4
-> MALF v1.5
-> PAS
-> Signal
-> Position
-> Portfolio Plan
-> Trade
-> System Readout
```

`Pipeline` 是横向编排账本：它可以调度、记录 run / checkpoint / manifest，但不得定义任何业务模块语义。

## 3. 模块所有权矩阵

| order | 模块 | semantic owner | self-owned boundary | external boundary |
|---:|---|---|---|---|
| 1 | `Data Foundation` | `source_fact_contract_owner` | source manifest、ledger key、tradeable facts、数据质量规则 | provider 只能做 source adapter；不得成为 truth owner |
| 2 | `MALF v1.4` | `structure_fact_owner` | wave、transition、boundary、WavePosition 结构语义 | validated asset 只读；下游不得重定义 |
| 3 | `MALF v1.5` | `structure_behavior_fact_owner` | `wave_behavior_snapshot` 六个行为面与审计理由 | 只能消费 MALF 输出；不得变成 PAS 强弱解释 |
| 4 | `PAS` | `opportunity_interpreter` | context、directional premise、strength_weakness_matrix、lifecycle、candidate 语义 | 概念来源可参考；不得输出订单、仓位、成交或 broker 指令 |
| 5 | `Signal` | `candidate_decision_ledger` | candidate accept / reject、decision reason、candidate ledger | 可用 engine 辅助计算；不得回写 MALF / PAS 定义 |
| 6 | `Position` | `management_semantics_owner` | entry / exit plan、T1/T2、保本、跟踪、分批语义 | 不生成成交事实，不修改上游机会定义 |
| 7 | `Portfolio Plan` | `portfolio_plan_owner` | 组合准入、目标暴露、trim 语义 | 第一阶段轻量保留；不得被 Position 或 Trade 吞并 |
| 8 | `Trade` | `execution_ledger_boundary_owner` | order intent / fill / rejection 的账本边界 | broker / live trading / paper-live 固定 deferred |
| 9 | `System Readout` | `readout_owner` | 全链路读出、审计快照、回测汇总读出 | 只读出和汇总，不替上游做语义定义 |
| 10 | `Pipeline` | `orchestration_ledger_owner` | run、checkpoint、manifest、resume trace | 只编排，不拥有业务语义 |

## 4. 自建 / 委外裁决

| 面 | 裁决 |
|---|---|
| 业务语义 | 必须自建，不能交给 provider、开源项目、历史 repo 或 engine |
| 数据来源接入 | 可委外为 adapter 输入，但 source manifest、ledger key、可交易事实规则自建 |
| 结构事实 | `MALF v1.4` 是 immutable authority；`MALF v1.5` 只允许追加只读结构行为事实，不回写 v1.4 |
| PAS 机会解释 | 必须重新公理化；不能复制历史系统旧语义 |
| 候选裁决 | `Signal` 自建决策账本；不得让回测框架替代 accept / reject 语义 |
| 组合计划 | `Portfolio Plan` 保留独立轻量层；早期可少字段，但不可取消 |
| 执行账本 | `Trade` 只冻结账本边界；真实 broker、成交回路、paper-live 延后 |
| 编排系统 | `Pipeline` 可以自建调度与 lineage，但不得借调度权定义业务语义 |

## 5. Portfolio Plan 保留边界

`Portfolio Plan` 当前冻结为独立轻量层。

必须保留：

- 组合级准入。
- 目标暴露。
- trim 意图。
- 多候选之间的组合协调边界。

当前不得扩展为：

- broker 下单。
- 成交回写。
- 收益承诺。
- 替代 `Position` 的 entry / exit plan。
- 替代 `Trade` 的 execution ledger。

## 6. 外部 adapter / engine 禁止越界

| 外部能力 | 允许 | 禁止 |
|---|---|---|
| source provider | 作为 Data Foundation adapter 输入 | 成为正式 truth owner |
| DuckDB / Arrow / Polars | 数据处理和研究查询底座 | 定义 MALF / PAS / Signal 语义 |
| vectorbt / backtesting.py | research proof adapter | 成为正式交易账本或候选裁决者 |
| Qlib | 隔离研究参考 | 拥有本系统语义定义权 |
| 历史 repo | 提供经验、样本、失败教训 | 原样迁入 schema、runner 或业务语义 |

## 7. 下游卡边界

本卡只冻结模块所有权。以下问题仍由后续卡负责：

| 后续卡 | 仍待冻结内容 |
|---|---|
| `storage-engine-and-portability-decision-card` | DuckDB、SQLite+Parquet、Hybrid、Go/Python 角色矩阵 |
| `historical-ledger-topology-protocol-card` | 历史大账本、子库共同键、run lineage、source manifest 规则 |
| `daily-incremental-and-resume-protocol-card` | 每日增量、dirty scope、checkpoint、resume、staging promote |
| `backtest-window-and-holdout-protocol-card` | 2012..2021、三年滚动、留出样本边界 |
| `pas-axiomatic-state-machine-card` | PAS v1.1 三件套设计集、MALF-first Core / Lifecycle / Service |
| `malf-pas-revision-roadmap-card` | MALF v1.5、PAS v1.2、场景图谱与 adapter 后移路线 |
| `malf-v1-5-wave-behavior-snapshot-card` | 已冻结 MALF-owned `wave_behavior_snapshot` 结构行为事实 |
| `pas-v1-2-strength-weakness-matrix-card` | 已冻结 PAS `strength_weakness_matrix`、强弱证据规则与独立 matrix service surface |
| `malf-pas-scenario-atlas-card` | MALF+PAS 沙盘模拟、图解案例与 companion atlas 资产（已冻结） |
| `open-source-adapter-boundary-card` | 开源项目逐项 adapter 边界（已闭环；首张 roadmap terminal） |

## 8. 冻结结论

```text
Data -> System module order is frozen.
Semantic ownership must remain self-owned.
External projects and providers are adapter / engine only.
Portfolio Plan remains an independent lightweight layer.
Runtime, formal DB mutation, broker, and profit claims remain not authorized.
```
