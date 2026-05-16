# MALF+PAS Scenario Atlas v1

日期：2026-05-16

状态：frozen-by-malf-pas-scenario-atlas-card-20260516-01

## 1. 目标

本文件冻结 `MALF_PAS_Scenario_Atlas_v1_0` 在 `Malf-Pas` 当前治理阶段的 companion authority surface。

正式 validated atlas：

```text
H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0
```

它不是新的 MALF / PAS design set，而是一个只读的场景图谱 companion asset。

## 2. 系统定位

| 项 | 裁决 |
|---|---|
| MALF v1.4 | `current immutable authority_anchor` |
| MALF v1.5 | `current structural behavior fact package` |
| PAS v1.1 | `predecessor PAS authority reference` |
| PAS v1.2 | `current successor PAS authority definition` |
| Scenario Atlas v1.0 | `companion authority asset for sandbox explanation` |
| 当前 atlas | `H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0` |
| 下一卡 | `open-source-adapter-boundary-card` |
| 是否输出订单 / 仓位 / 成交 / broker 指令 / 收益承诺 | 否 |

## 3. 固定输入边界

atlas 只能消费：

```text
MALF WavePosition
WaveBehaviorSnapshot
PAS Context
PAS Directional Premise
PAS StrengthWeaknessMatrix
```

历史资料只允许进入：

```text
reference only / not proof
```

不得让历史资料变成当前语义 owner、formal proof 或收益证据。

## 4. 固定案例编排

atlas 首版固定五个标准案例：

| 顺序 | case_id | 主读法 |
|---:|---|---|
| 1 | `strength_continuation_case` | `strong` |
| 2 | `weakness_rejection_case` | `weak` |
| 3 | `boundary_test_case` | `mixed` |
| 4 | `transition_unresolved_case` | `ambiguous` |
| 5 | `no_actionable_premise_case` | `not_applicable` |

编排顺序固定按语义主读法，而不是按年份、收益结果或历史来源排序。

## 5. 图解发布面

正式发布面固定为：

```text
Markdown + SVG
```

其中：

- Markdown 承担案例说明、边界、输入摘要与禁止结论。
- SVG 承担语义图谱、状态线与 companion 图解。
- Browser 只可用于预览和版式讨论，不属于正式 authority artifact 本身。

## 6. companion 边界

atlas 只回答：

- 当前 frozen MALF+PAS 语义在标准场景里如何被读懂。
- 哪些证据支持 `strong / weak / mixed / ambiguous / not_applicable`。
- 哪些 setup posture 可以被解释为 `favored / allowed / deferred / blocked`。
- 哪些历史旁证只可作为阅读辅助。

atlas 不回答：

- `buy / sell / hold`
- broker feasibility
- live trading readiness
- formal backtest proof
- alpha 证明
- 仓位、订单、成交、收益

## 7. 不变量

1. atlas 只能解释已冻结语义，不得反向重写 MALF 或 PAS。
2. atlas 的历史旁证必须带 `reference only / not proof` 口径。
3. atlas 的正式图解资产固定为 `Markdown + SVG`。
4. atlas 不得伪装成 playbook、runtime contract、formal proof 或收益叙事。
5. 同一案例 id、同一上游 frozen 输入边界，应保持可重复阅读的一致表达。
6. atlas 关闭后，下一张授权卡推进为 `open-source-adapter-boundary-card`。

## 8. 当前闭环结论

第 15 卡已建立 `MALF_PAS_Scenario_Atlas_v1_0`，并把它冻结为：

```text
read-only companion atlas
standard cases + svg diagrams
reference-only historical side evidence
no profit proof
```

当前 live next 推进为：

```text
open-source-adapter-boundary-card
```
