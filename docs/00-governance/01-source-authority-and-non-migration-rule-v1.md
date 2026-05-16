# Malf-Pas 来源裁决与非迁移规则 v1

日期：2026-05-15

状态：frozen-by-source-authority-and-non-migration-rule-card-20260515-01

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
| `planned_successor_authority` | 已纳入 roadmap 但尚未施工完成的新版本权威资产 |
| `successor_authority_definition` | 已施工完成、但不替代当前锚点的新版本权威资产 |
| `companion_authority_asset` | 已施工完成、用于图解/案例/阅读伴随的只读权威资产 |
| `rejected_for_semantic_ownership` | 不允许拥有本系统语义定义权 |

## 3. 来源裁决

| 来源 | 分类 | 裁决 |
|---|---|---|
| `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` | `authority_anchor` | 当前系统结构事实、WavePosition、transition、boundary 的唯一上游锚点 |
| `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4.zip` | `authority_anchor_zip_copy` | 随当前 anchor 目录保留的 authority zip 副本；可恢复 snapshot 归属 `H:\Malf-Pas-backup` |
| `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` | `authority_anchor` | 当前 PAS v1.1 Core / Lifecycle / Service 权威设计集 |
| `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1.zip` | `authority_anchor_zip_copy` | 随 PAS v1.1 目录保留的 authority zip 副本；可恢复 snapshot 归属 `H:\Malf-Pas-backup` |
| `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` | `successor_authority_definition` | 第 13 卡已冻结；用于补足 `wave_behavior_snapshot`，不改写 v1.4 原目录 |
| `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5.zip` | `successor_authority_zip_copy` | 随 MALF v1.5 目录保留的 authority zip 副本；可恢复 snapshot 归属 `H:\Malf-Pas-backup` |
| `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` | `successor_authority_definition` | 第 14 卡已冻结；用于发布 `strength_weakness_matrix`，不改写 v1.1 原目录 |
| `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2.zip` | `successor_authority_zip_copy` | 随 PAS v1.2 目录保留的 authority zip 副本；可恢复 snapshot 归属 `H:\Malf-Pas-backup` |
| `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0` | `companion_authority_asset` | 第 15 卡已冻结；用于 MALF+PAS 沙盘模拟与图解案例，不作为收益证明 |
| `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0.zip` | `companion_authority_zip_copy` | 随 Scenario Atlas 目录保留的 authority zip 副本；可恢复 snapshot 归属 `H:\Malf-Pas-backup` |
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` | `authority_anchor` | predecessor/original source reference；只作来源追溯和对照 |
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip` | `authority_anchor` | predecessor/original archive；只作锚点校验和可恢复输入 |
| `H:\Asteria-Validated\Asteria_System_Design_Set_v1_0` | `reference_input` | 治理范式、文档组织、门禁与 execution discipline 参考 |
| `H:\Asteria-Validated\MALF-system-history` | `historical_tradeoff_reference` | MALF / PAS 演化历史、失败教训和 retained gap 来源；不得迁移旧语义 |
| `H:\Asteria-Validated\MALF-reference` | `reference_input` | MALF / PAS 桥接、样本和验证线索参考 |
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
7. 把 `H:\Asteria-Validated` 中的上一版 validated 资产解释成当前系统 runtime、正式 DB 或 broker proof。
8. 把 DuckDB、Arrow、Polars、vectorbt、backtesting.py、Qlib、AKShare 或 baostock 提升为业务语义拥有者。

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
6. `H:\Asteria-Validated` 下的历史资产只能只读吸收 authority、范式、样本和失败教训；不得直接变成当前系统输出根。
7. 外部 provider、开源项目和研究 engine 只能做 adapter / engine，不得取得 `MALF / PAS / Signal` 语义主权。

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

## 9. 冻结不变量

| invariant_id | invariant |
|---|---|
| `SOURCE-AUTHORITY-CLASSIFICATION-FROZEN` | 来源分类枚举与主要来源裁决已冻结 |
| `MALF-V1-4-AUTHORITY-ANCHOR` | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` 是当前结构事实锚点，不授权下游重定义 |
| `PAS-V1-1-DESIGN-SET` | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` 是当前 PAS Core / Lifecycle / Service 权威设计集 |
| `AUTHORITY-ZIP-COPY-BOUNDARY` | `H:\Malf-Pas-Validated` 可保留随权威目录副本存在的 authority zip；正式可恢复 snapshot、batch manifest 与交付包归属 `H:\Malf-Pas-backup` |
| `MALF-PAS-REVISION-ROADMAP` | MALF v1.5 与 PAS v1.2 已沉淀为 successor authority；Scenario Atlas 已沉淀为 companion authority asset，且都尚未成为 runtime 或 DB 事实 |
| `BOOK-ROOT-CONCEPT-ONLY` | 书籍根和 Lance Beggs 概念根只提供 PAS 概念、语境和术语来源 |
| `HISTORY-REFERENCE-NO-MIGRATION` | 历史 repo 和历史 validated 资产只读参考，不得迁移旧 schema、runner、DuckDB 表面或业务语义 |
| `ADAPTER-NO-SEMANTIC-OWNERSHIP` | 外部 provider、开源项目和 research engine 只能做 adapter / engine |
| `NO-FORMAL-DB-MUTATION` | 当前阶段不得写入正式 DB 或正式数据根目录 |
| `NO-BROKER-PROFIT-CLAIM` | 当前阶段不得输出 broker、订单、仓位、成交或收益承诺 |
