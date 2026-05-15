# Malf-Pas 来源裁决与非迁移规则 v1

日期：2026-05-15

## 1. 目的

本文件规定：哪些资料可以成为权威输入，哪些只能作为参考，哪些明确不能直接迁入新系统。

## 2. 治理分类枚举

| enum | 含义 |
|---|---|
| `authority_anchor` | 长期不变的系统锚点 |
| `concept_source` | 提供定义、公理、边界的概念来源 |
| `brainstorming_source` | 提供问题意识、交易语境、术语生成与思路风暴的来源 |
| `historical_tradeoff_reference` | 提供旧版本实现理由、取舍折衷、未完工原因与失败教训的来源 |
| `reference_input` | 提供经验、样本、实现线索的参考输入 |
| `adapter_candidate` | 可提供通用能力，但不拥有语义定义权 |
| `retained_gap` | 目前已识别但未被解决的缺口 |
| `rejected_for_semantic_ownership` | 不允许拥有本系统语义定义权 |

## 3. 来源裁决

| 来源 | 分类 | 裁决 |
|---|---|---|
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` | `authority_anchor` | 结构事实、WavePosition、transition、boundary 的唯一上游锚点 |
| `G:\《股市浮沉二十载》` | `brainstorming_source` | 书籍参考与思路风暴的总来源；用于恢复 PAS 原始问题意识、交易语境与术语根 |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | `concept_source` | 提供 PAS 的 context、trigger、strength、lifecycle 与业务边界概念 |
| `G:\malf-history` | `historical_tradeoff_reference` | 曾经做过但未完成的历史版本根；用于理解各版本、各模块为何这样实现及其权衡折衷 |
| `G:\malf-history\MarketLifespan-Quant` | `reference_input` | 提供 PAS、Signal、ranking、readout 经验 |
| `G:\malf-history\EmotionQuant-gamma` | `reference_input` | 提供 T+1、A 股边界和 risk sidecar 经验 |
| `G:\malf-history\astock_lifespan-alpha` | `reference_input` | 提供早期 Alpha/PAS/Signal/Position 桥接经验 |
| `G:\malf-history\lifespan-0.01` | `reference_input` | 提供 producer、runner、checkpoint、ledger 经验 |
| `DuckDB / Arrow / Polars` | `adapter_candidate` | 可做数据处理底座，不定义业务语义 |
| `vectorbt / backtesting.py` | `adapter_candidate` | 只做 research proof adapter |
| `Qlib` | `adapter_candidate` | 只做隔离研究参考 |
| `AKShare` | `rejected_for_semantic_ownership` | 不进入正式 truth |

## 4. 非迁移规则

以下动作当前明确禁止：

1. 直接复制历史 repo 的 schema、runner、DuckDB 表面进新系统。
2. 直接复制书籍正文或把书中交易管理动作当作 PAS 输出动作。
3. 把外部开源项目当作 `MALF / PAS / Signal` 的语义拥有者。
4. 用历史策略收益、旧回测截图或经验描述替代 formal proof。
5. 把 `G:\malf-history` 中任一未完成版本解释成当前系统的完成品。
6. 把 `G:\《股市浮沉二十载》` 解释成 broker、仓位、订单、成交或收益承诺来源。

## 5. 允许的吸收方式

| 材料类型 | 允许吸收 |
|---|---|
| validated design set | 定义、桥接关系、不变量 |
| 历史 repo | 模块边界、状态机经验、失败教训、测试样本口径 |
| 概念书籍 | 公理、状态转移、交易业务边界、术语映射 |
| 开源项目 | 通用 engine、数据计算、research adapter 能力 |

## 6. 钢铁规则

1. `G:\《股市浮沉二十载》` 是书籍参考与思路风暴来源根；后续 PAS 相关概念问题必须优先回到这里对齐语境。
2. `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` 是当前 PAS context、trigger、strength、lifecycle 的概念锚点。
3. `G:\malf-history` 是历史版本与模块取舍参考根；后续判断旧实现为何如此设计时，必须先把它视为经验输入。
4. `G:\malf-history` 不得成为 legacy code migration、schema transplant、runner transplant 或正式 runtime 来源。
5. 任何从书籍或历史版本吸收的内容，都必须经过本仓库文档、公理、contract 或执行四件套重新冻结。

## 7. retained gaps

当前明确保留但不在第一阶段解决：

- profit proof
- broker feasibility
- formal DB topology
- runner contract
- fill / account loop
- A 股硬过滤数据源落地

## 8. adapter boundary

| adapter | 允许角色 | 禁止角色 |
|---|---|---|
| `DuckDB / Arrow / Polars` | 数据处理底座 | 拥有 `MALF / PAS / Signal` 语义 |
| `vectorbt / backtesting.py` | research proof adapter | 充当正式交易账本 |
| `Qlib` | 隔离研究参考 | 定义 MALF 或 PAS 语义 |
| `baostock` | source adapter 候选 | 充当正式 truth owner |
| `AKShare` | 参考或实验输入 | 进入正式 truth |
