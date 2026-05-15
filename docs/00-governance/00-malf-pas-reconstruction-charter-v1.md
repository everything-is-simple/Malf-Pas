# Malf-Pas 重构总纲 v1

日期：2026-05-15

## 1. 系统命名

| 项 | 名称 |
|---|---|
| 英文名 | `Malf-Pas` |
| 中文名 | `Malf-Pas 重构系统` |
| 主落点 | `H:\Malf-Pas` |
| 本地数据库根目录 | `H:\Malf-Pas-data` |
| 远端 | `https://github.com/everything-is-simple/Malf-Pas` |
| 结构锚点 | `MALF v1.4` |
| 当前重点 | `PAS axiomatic redesign` |

一句话定义：

> Malf-Pas 是一个以 MALF v1.4 为结构真值、以 PAS 为机会解释层、以 Signal 为候选裁决层的治理先行研究系统。

## 2. 重构裁决

本次不是在旧系统上继续拼接代码，而是建立一个目标定义先行的新主线。

| 问题 | 裁决 |
|---|---|
| 是否再次重构 | 是 |
| 是否推倒 MALF v1.4 | 否，MALF v1.4 固定为长期 authority anchor |
| 是否保留旧系统经验 | 是，保留经验、测试样本、失败教训，不直接继承旧语义 |
| 第一阶段是否写 runtime | 否 |
| 第一阶段是否写正式 DB | 否 |
| 第一阶段是否讨论 broker | 否 |
| 谁是当前真正要重做的核心 | `PAS` |

## 3. 第一阶段边界

当前阶段固定为：

```text
governance-only
doc-first
read-only-to-validated-assets
no-formal-db-mutation
no-legacy-code-migration
no-broker
no-profit-claim
```

本阶段不允许被解释成：

```text
runtime build
strategy proof
broker feasibility execution
paper-live preparation
historical code transplant
```

## 4. 权威资产链

| 资产 | 地位 | 用途 |
|---|---|---|
| `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` | 核心 authority anchor | 后续 PAS / Signal / Position / Trade / System 的结构输入基准 |
| `H:\Asteria-Validated\Asteria_System_Design_Set_v1_0` | 治理范式参考 | 提供文档结构、门禁与 execution discipline 参考 |
| `H:\Asteria-Validated\MALF-system-history` | 历史经验输入 | 提取 MALF/PAS 演化经验，不迁移旧语义 |
| `H:\Asteria-Validated\MALF-reference` | 参考输入 | 提供桥接与验证线索 |
| `G:\malf-history` | 历史系统输入池 | 梳理各代系统最出彩模块与 retained gap |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | PAS 概念锚点 | 提取 context、trigger、strength、lifecycle、业务边界 |

## 5. 主线裁决

```mermaid
flowchart LR
    A["MALF v1.4"] --> B["PAS"]
    B --> C["Signal"]
    C --> D["Position / Trade"]
    D --> E["System Readout"]
```

| 层 | 角色 |
|---|---|
| `MALF v1.4` | `structure_fact_owner` |
| `PAS` | `opportunity_interpreter` |
| `Signal` | `candidate_decision_ledger` |
| `Position / Trade` | `management_and_execution_layers` |

## 6. 不允许的重构方式

| 禁止项 | 原因 |
|---|---|
| 边 debug 边发明 PAS 主线定义 | 会重演旧系统语义漂移 |
| 下游模块反向修正 MALF | 会污染结构真值 |
| 把历史 repo 当成现成成品迁入 | 会把旧债直接带进新系统 |
| 用开源项目替代语义定义 | 会失去系统主权 |
| 第一阶段直接谈收益或实盘 | 当前没有证据支持 |

## 7. 第一阶段目标

第一张路线图必须完成：

1. 固定来源裁决与非迁移规则。
2. 固定 MALF v1.4 在系统中的锚点位置。
3. 梳理旧系统强项地图。
4. 冻结 PAS 公理化状态机最小集合。
5. 固定开源适配器边界。
6. 建立 execution 四件套模板和结论索引。
