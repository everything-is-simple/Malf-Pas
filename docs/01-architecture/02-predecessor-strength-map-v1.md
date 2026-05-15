# 旧系统强项地图 v1

日期：2026-05-15

状态：active / reference-map

## 1. 目标

本文件只回答：旧系统和历史资料各自最值得吸收的强项是什么，以及哪些内容必须留在参考层。

## 2. 强项地图

| 来源 | 可吸收强项 | 处置 |
|---|---|---|
| `H:\Asteria-Validated\MALF-system-history` | MALF 历次沉淀、定义演进脉络 | `reference_input` |
| `H:\Asteria-Validated\MALF-reference` | 桥接材料、定义旁证 | `reference_input` |
| `G:\《股市浮沉二十载》` | 书籍参考、思路风暴、PAS 原始问题意识与交易语境 | `brainstorming_source` |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | context、trigger、strength、lifecycle、交易业务边界 | `concept_source` |
| `G:\malf-history` | 曾经做过但未完成的历史版本集合；各模块实现理由、权衡折衷、失败教训 | `historical_tradeoff_reference` |
| `G:\malf-history\MarketLifespan-Quant` | PAS 五触发器、Signal/readout、统计排名经验 | `reference_input` |
| `G:\malf-history\EmotionQuant-gamma` | T+1、A 股执行边界、risk sidecar 经验 | `reference_input` |
| `G:\malf-history\astock_lifespan-alpha` | Alpha/PAS/Signal/Position 早期分解经验 | `reference_input` |
| `G:\malf-history\lifespan-0.01` | producer、runner、checkpoint、ledger 思路 | `reference_input` |

## 3. 明确不吸收的内容

| 内容 | 原因 |
|---|---|
| 旧 repo 代码整块迁移 | 会把历史语义债带入新系统 |
| 历史回测结果直接当新系统证据 | 不具备当前 repo lineage |
| 旧 schema 原样继承 | 会阻断重新公理化 PAS |
| 旧版本未完工状态被当成当前完成状态 | 会掩盖当时的取舍折衷和 retained gap |
| 书籍正文直接复制进 repo | 会把概念来源误当成交付内容 |
| 外部库默认字段定义 | 不等于本系统合同 |

## 4. 当前结论

```text
collect strengths
preserve book-origin brainstorming lineage
preserve historical tradeoff rationale
preserve gaps
do not transplant semantics
```
