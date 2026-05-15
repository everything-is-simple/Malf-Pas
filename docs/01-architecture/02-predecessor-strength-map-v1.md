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
| `G:\malf-history\MarketLifespan-Quant` | PAS 五触发器、Signal/readout、统计排名经验 | `reference_input` |
| `G:\malf-history\EmotionQuant-gamma` | T+1、A 股执行边界、risk sidecar 经验 | `reference_input` |
| `G:\malf-history\astock_lifespan-alpha` | Alpha/PAS/Signal/Position 早期分解经验 | `reference_input` |
| `G:\malf-history\lifespan-0.01` | producer、runner、checkpoint、ledger 思路 | `reference_input` |
| `YTC 卷 2/3/4` | PAS 公理、状态变化、交易业务边界 | `concept_source` |

## 3. 明确不吸收的内容

| 内容 | 原因 |
|---|---|
| 旧 repo 代码整块迁移 | 会把历史语义债带入新系统 |
| 历史回测结果直接当新系统证据 | 不具备当前 repo lineage |
| 旧 schema 原样继承 | 会阻断重新公理化 PAS |
| 外部库默认字段定义 | 不等于本系统合同 |

## 4. 当前结论

```text
collect strengths
preserve gaps
do not transplant semantics
```

