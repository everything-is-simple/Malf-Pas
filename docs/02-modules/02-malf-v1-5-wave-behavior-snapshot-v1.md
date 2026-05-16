# MALF v1.5 Wave Behavior Snapshot v1

日期：2026-05-16

状态：frozen-by-malf-v1-5-wave-behavior-snapshot-card-20260516-01

## 1. 目标

本文件冻结 MALF v1.5 在 `Malf-Pas` 当前治理阶段的 successor authority design surface。

正式 validated 设计集：

```text
H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5
```

MALF v1.5 不重写 `MALF v1.4`，而是在 v1.4 已有 `WavePosition / Core trace / Lifespan stats /
transition trace / birth descriptors` 之上，新增只读的 `wave_behavior_snapshot`。

```text
MALF v1.4 facts
-> wave_behavior_snapshot
-> PAS v1.2 strength_weakness_matrix
-> Signal
```

## 2. 系统定位

| 项 | 裁决 |
|---|---|
| MALF v1.4 | `current immutable authority_anchor` |
| MALF v1.5 | `successor authority definition` |
| 当前设计集 | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5` |
| predecessor/original reference | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4` |
| 上游 | `MALF v1.4 WavePosition / Core trace / Lifespan stats / transition trace / birth descriptors / lineage` |
| 下游 | `PAS v1.2` |
| 是否输出 PriceBar 重解释 | 否 |
| 是否输出 strength score | 否 |
| 是否输出 setup family | 否 |
| 是否输出 accept / reject | 否 |
| 是否输出订单 / 仓位 / 成交 / broker 指令 / 收益承诺 | 否 |

## 3. `wave_behavior_snapshot` 只回答什么

`wave_behavior_snapshot` 只回答可审计的结构行为事实，不回答机会解释或交易动作。

当前固定六个行为面：

| facet | 作用 | 只读来源 |
|---|---|---|
| `continuation_regime` | 当前 wave 是延续、减速还是停滞 | `new_count / no_new_span / update_rank / stagnation_rank` |
| `stagnation_regime` | 波段停滞压力是否抬升 | `no_new_span / stagnation_rank / life_state` |
| `transition_regime` | transition 是平稳切换、反复摇摆还是未决拖长 | `transition_span / candidate_replacement_count / open_transition_id` |
| `birth_quality_regime` | 当前 wave 的出生质量是紧凑、中性还是代价较大 | `candidate_wait_span / candidate_replacement_count / confirmation_distance_*` |
| `boundary_pressure_regime` | 当前结构更靠近延续边界、守护边界还是中性区 | `current_effective_guard / transition boundary / confirmation lineage` |
| `directional_continuity_regime` | 当前结构更像顺势延续、反向新生或 transition 未定 | `direction / old_direction / birth_type / system_state` |

这些 facet 只能是结构行为 bucket 与审计理由，不得直接变成强弱结论、setup 结论或交易意图。

## 4. `wave_behavior_snapshot` 不回答什么

- 不回答 `buy / sell / hold / reduce / add`
- 不回答 `strong / weak` 的最终业务语义
- 不回答 `TST / BOF / BPB / PB / CPB`
- 不回答接受 / 拒绝
- 不回答仓位、分批、止损、成交、账户或收益
- 不回答 runtime 是否 ready
- 不授权正式 DB mutation、broker、paper-live 或实盘

## 5. 来源边界

| 来源 | MALF v1.5 吸收方式 | 禁止解释 |
|---|---|---|
| `MALF v1.4` | 唯一结构事实输入；提供 WavePosition 与 lineage | 不得被 v1.5 覆盖或伪装替换 |
| `MALF-system-history` | 只读回收“哪些结构行为事实曾经缺失”的经验 | 不迁移旧 schema、旧 runner、旧语义表面 |
| `MALF-reference` | 只读桥接表达、图示和边界提醒 | 不变成当前语义 owner |
| `PAS v1.1` | 只作为下游需求方参考，不反向定义 MALF | 不得让 PAS 倒逼 MALF 输出机会解释 |

## 6. Service 只读发布面

当前 v1.5 固定新增两层服务面：

```text
WaveBehaviorSnapshot
WaveBehaviorSnapshotLatest
```

其中：

- `WaveBehaviorSnapshot` 绑定单条结构行为快照与来源 lineage。
- `WaveBehaviorSnapshotLatest` 是每个 `symbol / timeframe` 的最新快照。

二者都只能由 MALF-Service 从 MALF 事实派生，不得由 PAS、Signal 或下游写回。

## 7. 机器可读入口

```text
governance/malf_v1_5_wave_behavior_snapshot_registry.toml
```

## 8. 不变量

1. `wave_behavior_snapshot` 只能消费 MALF 已确认或当时可见的结构事实。
2. MALF v1.5 不得重算 `PriceBar -> HH/HL/LL/LH` 以外的新语义入口给 PAS。
3. MALF v1.5 只能发布行为事实 bucket 与 audit reason，不得替 PAS 生成强弱结论。
4. 没有 MALF lineage，不得形成 formal `wave_behavior_snapshot`。
5. 同输入、同 MALF v1.4 rule version、同 v1.5 rule version 必须可重放一致。
6. v1.5 是 successor design set，不得回写、覆盖或伪装成 v1.4 原锚点。

## 9. 当前闭环结论

第 13 卡已建立 MALF v1.5 successor design set，并把 `wave_behavior_snapshot` 冻结为
MALF-owned structure behavior facts。

第 14 卡已经完成：

```text
pas-v1-2-strength-weakness-matrix-card
```

首张治理 roadmap 当前口径为：

```text
none / terminal
```

PAS v1.2 已固定只消费：

```text
WavePosition + wave_behavior_snapshot
```

仍不得回头读取 `PriceBar` 或重写 MALF。
