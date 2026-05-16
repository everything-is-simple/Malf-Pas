# Open-Source Adapter Boundary v1

日期：2026-05-16

状态：frozen-by-open-source-adapter-boundary-card-20260516-01

## 1. 目标

本文件冻结 `Malf-Pas` 当前 authority surface 里主要外部项目的 adapter 法规面。

`docs/00-governance/01-source-authority-and-non-migration-rule-v1.md` 继续负责来源分类总原则；
本文件只负责把当前会被提到的外部项目逐项立法为：

- 允许扮演什么 adapter 角色
- 不得越过哪些边界
- 适用到哪些模块
- 明确不负责什么

本卡只冻结治理边界，不授权 runtime、正式 DB mutation、broker、order、position、fill 或 profit claim。

## 2. 统一 adapter 角色法

| role | 含义 |
|---|---|
| `source_adapter` | 只负责把外部来源接到 `Data Foundation` 输入边界 |
| `research_query_or_data_processing_adapter` | 只负责研究查询、列式处理、数据加工与审计辅助 |
| `research_proof_adapter` | 只负责 research proof、回放、沙盘或只读验证辅助 |
| `isolated_research_reference` | 只作为隔离研究参考，不进入当前系统主线 authority |
| `reference_or_experimental_input_only` | 只作参考或实验输入，不进入正式 truth 与正式语义链 |

## 3. 全局禁止越界

以下边界对全部外部项目一律写死：

1. 不得取得 `MALF / PAS / Signal / Position / Trade / System Readout / Pipeline` 语义主权。
2. 不得充当正式 truth owner。
3. 不得充当 order owner、position owner、fill owner。
4. 不得充当 broker instruction source。
5. 不得充当 profit proof source。
6. 不得把外部项目存在，解释成 runtime 已授权、formal DB mutation 已打开或 live trading 已讨论。

## 4. 项目映射总表

| 项目 | 允许角色 | 适用模块 | 来源裁决关系 | 明确非目标 |
|---|---|---|---|---|
| `DuckDB / Arrow / Polars` | `research_query_or_data_processing_adapter` | `Data Foundation` 到 `System Readout` 的研究查询、加工、审计辅助面 | 与 `source_authority` 中的 `adapter_candidate` 对齐 | 不是 formal truth owner，不是模块语义 owner |
| `vectorbt / backtesting.py` | `research_proof_adapter` | `MALF / PAS / Signal / Position / Portfolio Plan / Trade / System Readout` 的只读 proof 辅助面 | 与 `source_authority` 中的 `adapter_candidate` 对齐 | 不是 candidate decision owner，不是 formal trading ledger |
| `Qlib` | `isolated_research_reference` | `PAS / Signal / Position / Portfolio Plan / Trade / System Readout` 的隔离研究参考面 | 与 `source_authority` 中的 `adapter_candidate` 对齐 | 不进入当前主线 authority，不定义 MALF/PAS 语义 |
| `baostock` | `source_adapter` | `Data Foundation` | 与 `source_authority` 中的 `adapter_candidate` 对齐 | 不是 formal truth owner |
| `AKShare` | `reference_or_experimental_input_only` | `Data Foundation` 的参考或实验输入面 | 保留 `rejected_for_semantic_ownership` | 不进入正式 truth，不定义任何业务语义 |

## 5. 逐项边界

### 5.1 `DuckDB / Arrow / Polars`

允许：

- 做 `research_query_or_data_processing_adapter`
- 做列式扫描、研究查询、数据加工、审计 readout
- 服务 `Data Foundation -> System Readout` 的只读研究面

禁止：

- 成为 formal truth owner
- 成为 `MALF / PAS / Signal / Position / Trade / System Readout / Pipeline` semantic owner
- 成为 order owner、position owner、fill owner、broker instruction source、profit proof source

明确非目标：

- 不把 `DuckDB / Arrow / Polars` 写成模块定义包
- 不把已有列式处理能力解释成正式 DB 已冻结

### 5.2 `vectorbt / backtesting.py`

允许：

- 做 `research_proof_adapter`
- 做只读 research proof、回放、窗口验证和沙盘辅助
- 消费已经冻结的上游语义输出，帮助 `System Readout` 或独立 proof 阅读

禁止：

- 成为 formal truth owner
- 成为 formal trading ledger
- 成为 `Signal` 的 candidate decision owner
- 成为 order owner、position owner、fill owner、broker instruction source、profit proof source
- 借 research engine 反向定义 `MALF / PAS / Signal`

明确非目标：

- 不把回测框架解释成主线语义 owner
- 不把 research proof 解释成 broker feasibility 或收益承诺

### 5.3 `Qlib`

允许：

- 做 `isolated_research_reference`
- 作为隔离研究参考、能力比较、问题分解或实验思路输入

禁止：

- 进入当前主线 authority 链
- 成为 `MALF` 或 `PAS` semantic owner
- 成为 formal truth owner、order owner、position owner、fill owner、broker instruction source、profit proof source

明确非目标：

- 不迁入 `Qlib` 语义表面、schema、runner 或模块定义
- 不把 `Qlib` 结果直接解释成当前系统 formal proof

### 5.4 `baostock`

允许：

- 做 `source_adapter`
- 只服务 `Data Foundation` 的来源接入面
- 提供 provider 输入、覆盖范围参考和来源侧实验读取

禁止：

- 成为 formal truth owner
- 成为 `MALF / PAS / Signal / Position / Trade / System Readout / Pipeline` semantic owner
- 成为 order owner、position owner、fill owner、broker instruction source、profit proof source

明确非目标：

- 不把 provider 可读性解释成当前 formal source ledger 已完成
- 不把 `baostock` 解释成可以直接替代 `source manifest`

### 5.5 `AKShare`

允许：

- 只做 `reference_or_experimental_input_only`
- 只用于 `Data Foundation` 的参考或实验输入

禁止：

- 进入正式 truth
- 取得任何业务语义主权
- 成为 order owner、position owner、fill owner、broker instruction source、profit proof source

特殊裁决：

```text
AKShare keeps rejected_for_semantic_ownership.
```

明确非目标：

- 不把 `AKShare` 提升为当前正式来源根
- 不把实验输入解释成当前主线授权输入

## 6. 机器可读入口

```text
governance/open_source_adapter_boundary_registry.toml
```

本 registry 只登记：

- authority doc
- run_id
- 角色枚举
- 项目清单
- 每项 allowed / forbidden boundary
- terminal closeout 口径

它不重写 `source_authority` 的大表。

## 7. 闭环结论

第 16 卡通过后：

```text
current_allowed_next_card = ""
doc state = none / terminal
first governance roadmap = completed
next step = open a separate roadmap
```

也就是说，首张治理 roadmap 到这里闭环完成；下一步不应继续占用这张治理 roadmap，
而应另开独立 roadmap 再讨论后续工作。
