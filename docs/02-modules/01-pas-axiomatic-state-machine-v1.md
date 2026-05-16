# PAS 公理化状态机 v1

日期：2026-05-15

状态：frozen-by-pas-axiomatic-state-machine-card-20260515-01

## 1. 目标

本文件冻结 PAS v1.1 在 `Malf-Pas` 当前治理阶段的权威设计面。

正式 validated 设计集：

```text
H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1
```

PAS v1.1 不是从 `PriceBar` 出发，而是从 MALF v1.4 `WavePosition` 出发。

```text
MALF WavePosition
-> PAS-Core
-> PAS-Lifecycle
-> PAS-Service
-> Signal
```

## 2. 系统定位

| 项 | 裁决 |
|---|---|
| PAS 角色 | `opportunity_interpreter` |
| 当前 PAS 设计集 | `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1` |
| 当前 MALF 锚点 | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4` |
| predecessor MALF reference | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` |
| 上游 | `MALF v1.4 WavePosition / Core trace / Lifespan stats / transition trace / birth descriptors` |
| 下游 | `Signal` |
| 是否输出订单 | 否 |
| 是否输出仓位 | 否 |
| 是否输出成交 | 否 |
| 是否输出收益承诺 | 否 |
| 是否输出 broker 指令 | 否 |

## 3. 三层结构

| layer | 作用 |
|---|---|
| `PAS-Core` | 从 MALF WavePosition 推导 context、premise、strength / weakness、opportunity zone 与 setup family |
| `PAS-Lifecycle` | 记录候选 observing、forming、waiting、triggered、cancelled、modified、invalidated、reentry 与 Signal handoff |
| `PAS-Service` | 只读发布 `PASCandidate`、`PASCandidateLatest`、`PASLifecycleTrace` |

铁律：

```text
MALF owns structure.
PAS owns opportunity interpretation.
Signal owns accept/reject.
Position and Trade own management/action.
```

## 4. PAS 宗旨

PAS v1.1 的宗旨是：

```text
identify strength / weakness
reject weakness
join strength
```

这句话只表示机会解释原则：

- 识别 MALF 波段事实中的强势 / 弱势。
- 拒绝弱势、失效、不被支持或 lineage 不完整的候选。
- 在 MALF 结构强势被证明且 PAS context 支持时，形成可交给 Signal 的机会候选。

它不表示买卖、仓位、成交或收益承诺。

## 5. Lifecycle 状态集合

```text
observing
forming
waiting
triggered
cancelled
modified
invalidated
reentry_candidate
submitted_to_signal
accepted_by_signal
rejected_by_signal
```

`triggered` 不等于交易信号，`accepted_by_signal` 不等于订单。

## 6. Setup Family

当前 PAS v1.1 固定五族 setup family：

```text
TST
BOF
BPB
PB
CPB
```

五族只表示 opportunity setup family，不自动等于交易信号。

## 7. 来源边界

| 来源 | PAS 吸收方式 | 禁止解释 |
|---|---|---|
| `MALF v1.4` | 结构事实锚点，提供 WavePosition | 不得被 PAS 重写 |
| YTC 卷 2 | context、S/R、trend、strength / weakness、future path | 不复制正文，不变成 runtime |
| YTC 卷 3 | setup family、trigger、cancel、modify、reentry | 不变成订单或仓位 |
| YTC 卷 4 | 业务流程边界提醒 | T1/T2、止损、仓位、执行不进入 PAS |

## 8. 明确 handoff 边界

PAS 只输出候选、状态、理由和 MALF lineage。

以下内容属于后续 `Position / Trade / Portfolio Plan`，不属于 PAS 输出：

- T1 / T2 分批。
- 保本处理。
- 跟踪止损。
- 撤单与真实执行。
- 仓位大小。
- 组合目标暴露。
- 收益统计与账户状态。

## 9. 机器可读入口

```text
governance/pas_axiomatic_state_machine_registry.toml
```

## 10. 不变量

1. PAS 只能消费 MALF 已确认或当时可见的事实。
2. PAS 不得重写 wave、break、transition、candidate guard、confirmation 或 lifespan rank。
3. PAS 输出的是候选和理由，不是交易承诺。
4. 没有 MALF lineage，不得形成 formal PAS candidate。
5. 同输入、同 MALF rule version、同 PAS rule version 必须可重放一致。

## 11. 后续修订路线

第 12 卡先裁决了修订路线，第 13 卡又进一步完成了 MALF v1.5 successor 设计集。
因此当前下一步已经固定为：PAS v1.2 只能消费 MALF 输出，不得回头读 `PriceBar`。

```text
MALF v1.5 frozen output = WavePosition + wave_behavior_snapshot
PAS v1.2 frozen input boundary = MALF outputs only
PAS v1.2 planned rule = strength_weakness_matrix
PAS still does not read PriceBar or rewrite MALF
```
