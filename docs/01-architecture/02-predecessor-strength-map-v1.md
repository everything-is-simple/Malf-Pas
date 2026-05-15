# 旧系统强项地图 v1

日期：2026-05-15

状态：frozen-by-predecessor-strength-map-card-20260515-01

## 1. 目标

本文件只回答：旧系统和历史资料各自最值得吸收的强项是什么，以及哪些内容必须留在参考层。

本文件不授权旧代码迁移、旧 schema 继承、runner 搬运、正式 DB mutation、runtime、broker、仓位、
订单、成交或收益证明。

## 2. 强项地图

| 来源 | 分类 | 可吸收强项 | 禁止迁移 / 禁止继承 | 后续使用边界 |
|---|---|---|---|---|
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` | `authority_anchor` | MALF v1.4 的结构事实、WavePosition、transition、boundary 与三件套权威边界 | 不得被 PAS、Signal、Position、Trade 或 adapter 重定义；不得解释成 runtime proof | 只作为结构事实锚点，向 PAS / Signal / Position 提供不可变上游结构 |
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip` | `authority_anchor` | MALF v1.4 锚点的可恢复归档副本 | 不得替代目录锚点，不得作为迁移旧 schema 或 runner 的来源 | 只用于锚点包边界与恢复性校验 |
| `H:\Asteria-Validated\Asteria_System_Design_Set_v1_0` | `reference_input` | 治理范式、文档组织、门禁、execution 四件套与 validated archive discipline | 不得解释成当前 release 状态、runtime 来源或语义拥有者 | 只吸收治理方法与交付纪律 |
| `H:\Asteria-Validated\MALF-system-history` | `historical_tradeoff_reference` | MALF / PAS 历次沉淀、定义演进脉络、retained gap 与失败教训 | 不得迁移旧代码、旧 schema、runner、DuckDB 表面或当前语义所有权 | 后续 PAS 公理化时只读参考演化原因与边界教训 |
| `H:\Asteria-Validated\MALF-reference` | `reference_input` | MALF / PAS 桥接材料、定义旁证、样本和验证线索 | 不得替代当前 repo formal proof，不得成为 runtime source 或 semantic owner | 只作为旁证和样本线索 |
| `G:\《股市浮沉二十载》` | `brainstorming_source` | PAS 原始问题意识、交易语境、术语生成和思路风暴来源 | 不得复制书籍正文进 repo，不得解释成运行代码、正式数据、broker 指令或收益承诺 | 后续 PAS 概念讨论必须回到这里对齐语境，但要经本 repo 重新公理化 |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | `concept_source` | context、trigger、strength、lifecycle、机会边界与交易管理语境 | 不得把 position、order、fill、profit promise 或书中动作直接变成 PAS 输出 | 只提供 PAS 状态机和业务边界概念来源 |
| `G:\malf-history` | `historical_tradeoff_reference` | 曾经做过但未完成的历史版本集合、模块实现理由、权衡折衷、样本和失败教训 | 不得作为 legacy code migration、schema transplant、runner transplant 或当前 semantic owner | 后续判断旧实现为何如此设计时，只读吸收取舍理由和 retained gap |
| `G:\malf-history\MarketLifespan-Quant` | `reference_input` | PAS 五触发器、Signal / readout、统计排名和候选读出经验 | 不得继承旧 trigger schema、runner、回测结果或当前系统语义所有权 | 只作为 PAS / Signal / readout 的经验输入 |
| `G:\malf-history\EmotionQuant-gamma` | `reference_input` | T+1、A 股执行边界、risk sidecar 与风险提醒经验 | 不得迁移旧执行面、risk runtime、broker 或仓位逻辑 | 只作为 A 股边界与风险 sidecar 的参考 |
| `G:\malf-history\astock_lifespan-alpha` | `reference_input` | Alpha / PAS / Signal / Position 早期分解、producer / consumer 边界和 contract-first 经验 | 不得迁移旧代码、旧 data runner、旧 queue/checkpoint 表面或完成状态标签 | 只吸收分解方式、合同边界和恢复经验 |
| `G:\malf-history\lifespan-0.01` | `reference_input` | producer、runner、checkpoint、ledger、raw_market -> market_base 的工程经验 | 不得原样继承 schema、runner、DB 表面或历史 pipeline 行为 | 只作为 Data Foundation / Pipeline 未来设计参考 |

## 3. 明确不吸收的内容

| 内容 | 原因 |
|---|---|
| 旧 repo 代码整块迁移 | 会把历史语义债带入新系统 |
| 历史回测结果直接当新系统证据 | 不具备当前 repo lineage |
| 旧 schema 原样继承 | 会阻断重新公理化 PAS |
| 旧 runner / queue / checkpoint 表面原样继承 | 会把旧系统未完成状态伪装成当前系统合同 |
| 旧版本未完工状态被当成当前完成状态 | 会掩盖当时的取舍折衷和 retained gap |
| 书籍正文直接复制进 repo | 会把概念来源误当成交付内容 |
| 书籍交易管理动作直接进入 PAS 输出 | 会让 PAS 越界输出仓位、订单、成交或收益承诺 |
| 外部库默认字段定义 | 不等于本系统合同 |

## 4. 冻结结论

```text
predecessor_strength_map = frozen
collect strengths = yes
preserve book-origin brainstorming lineage = yes
preserve historical tradeoff rationale = yes
preserve retained gaps = yes
transplant legacy code / schema / runner = no
formal DB mutation = no
broker feasibility = deferred
next card = pas-axiomatic-state-machine-card
```
