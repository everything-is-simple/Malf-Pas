# PAS v1.2 Strength Weakness Matrix v1

日期：2026-05-16

状态：frozen-by-pas-v1-2-strength-weakness-matrix-card-20260516-01

## 1. 目标

本文件冻结 PAS v1.2 在 `Malf-Pas` 当前治理阶段的 successor authority design surface。

正式 validated 设计集：

```text
H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2
```

PAS v1.2 不改写 `PAS v1.1` 原目录，而是在 `PAS-Core` 与 `PAS-Lifecycle` 之间新增一个离散的
`strength_weakness_matrix` 层。

```text
MALF WavePosition
+ WaveBehaviorSnapshot
-> PAS-Core
-> strength_weakness_matrix
-> PAS-Lifecycle
-> PAS-Service
-> Signal
```

## 2. 系统定位

| 项 | 裁决 |
|---|---|
| MALF v1.4 | `current immutable authority_anchor` |
| MALF v1.5 | `current structural behavior fact package` |
| PAS v1.1 | `predecessor PAS authority reference` |
| PAS v1.2 | `successor PAS authority definition` |
| 当前设计集 | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2` |
| 下游 | `Signal` |
| 是否读 `PriceBar` | 否 |
| 是否输出订单 / 仓位 / 成交 / broker 指令 / 收益承诺 | 否 |

## 3. 固定输入边界

`strength_weakness_matrix` 只能消费：

```text
MALF WavePosition
MALF Core trace
MALF transition trace
MALF Lifespan stats
MALF birth descriptors
MALF source lineage
WaveBehaviorSnapshot
PAS Context
PAS Directional Premise
```

其中 `WaveBehaviorSnapshot` 六个行为面固定沿用第 13 卡：

```text
continuation_regime
stagnation_regime
transition_regime
birth_quality_regime
boundary_pressure_regime
directional_continuity_regime
```

## 4. 固定输出边界

`strength_weakness_matrix` 输出固定为：

| 输出 | 说明 |
|---|---|
| `read_status` | `strong / weak / mixed / ambiguous / not_applicable` |
| `strength_evidence[]` | 支持“偏强”的离散证据 |
| `weakness_evidence[]` | 支持“偏弱”的离散证据 |
| `ambiguity_evidence[]` | 导致混合或不确定的证据 |
| `setup_posture_by_family` | 每个 `TST / BOF / BPB / PB / CPB` 的 `favored / allowed / deferred / blocked` |

这是机会解释层，不是数值评分层，也不是 MALF 结构事实层。

## 5. 默认离散矩阵

第 14 卡固定的默认 posture 规则如下：

| directional premise | dominant read | TST | BOF | BPB | PB | CPB |
|---|---|---|---|---|---|---|
| `expect_strength_continuation` | `strong` | `allowed` | `blocked` | `favored` | `favored` | `deferred` |
| `expect_weakness_rejection` | `weak` | `allowed` | `favored` | `blocked` | `blocked` | `deferred` |
| `expect_boundary_test` | `mixed` | `favored` | `allowed` | `deferred` | `deferred` | `deferred` |
| `expect_transition_resolution` | `ambiguous` | `deferred` | `deferred` | `blocked` | `blocked` | `blocked` |
| `no_actionable_premise` | `not_applicable` | `blocked` | `blocked` | `blocked` | `blocked` | `blocked` |

若 `read_status` 与 `directional premise` 不匹配，setup posture 必须整体降一档：

```text
favored -> allowed -> deferred -> blocked
```

若存在 `lineage_gap`、`transition_bound` 或 evidence 不足，则 posture 上限固定为 `deferred`。

## 6. Service 只读发布面

PAS v1.2 固定新增独立服务面：

```text
PASStrengthWeaknessMatrix
PASStrengthWeaknessMatrixLatest
```

同时保留并升级已有服务面：

```text
PASCandidate
PASCandidateLatest
PASLifecycleTrace
```

`PASCandidate` / `PASCandidateLatest` 只保留矩阵摘要，不再承担矩阵主存储。至少要保留：

```text
matrix_id
read_status
setup_family
candidate_reason
```

## 7. 不变量

1. PAS v1.2 只能消费 MALF 输出，不得回头读 `PriceBar`。
2. `strength_weakness_matrix` 必须保持离散矩阵，不得升级为分数或排名体系。
3. `strength_weakness_matrix` 是 PAS 机会解释，不得伪装成 MALF 结构事实。
4. 没有 MALF lineage，不得形成 formal matrix。
5. 同输入、同 MALF 规则版本、同 PAS 规则版本，必须可重放一致。
6. PAS v1.2 不输出 accept / reject，不输出订单、仓位、成交或收益承诺。

## 8. 当前闭环结论

第 14 卡已建立 PAS v1.2 successor design set，并把 `strength_weakness_matrix` 冻结为
基于 MALF 输出的离散强弱识别层。

首张治理 roadmap 现已收口为：

```text
none / terminal
```
