# Malf-Pas Post-Terminal Roadmap And Module-DB Discipline v1

日期：2026-05-16

状态：adopted-after-first-governance-roadmap-terminal

## 1. 目的

本文件冻结首张治理 roadmap 收口之后的新纪律。

它回答 4 个问题：

1. 后续 roadmap 该怎么开。
2. 每张 roadmap 和模块数据库之间是什么关系。
3. 数据真值、mock、上一版数据库和检查放行该如何约束。
4. 每张 roadmap 什么时候才算同时开发可用、日常可用。

## 2. 本次新增纪律总数

本次一共新增 `12` 条系统纪律。

## 3. 十二条纪律

| order | rule_id | discipline |
|---:|---|---|
| 1 | `POST-TERMINAL-SEPARATE-ROADMAP-ONLY` | 首张治理 roadmap 收口后，后续工作必须新开独立 roadmap，不得继续占用已 terminal 的治理路线图。 |
| 2 | `ONE-ROADMAP-ONE-MODULE-DB` | 每一张新 roadmap 必须对应一个模块数据库或一个模块账本边界，不得一张 roadmap 同时跨多个核心模块数据库。 |
| 3 | `CURRENT-MODULE-DB-READY-BEFORE-NEXT-ROADMAP` | 当前 roadmap 对应的模块数据库未建好、未通过检查、未形成闭环前，不得开启下一张 roadmap。 |
| 4 | `ROADMAP-READY-REQUIRES-DEVELOPMENT-USABLE` | 模块 roadmap 要宣告 ready，必须先做到开发可用：下游能稳定消费 contract、schema、manifest、lineage 和最小接口。 |
| 5 | `ROADMAP-READY-REQUIRES-DAILY-USABLE` | 模块 roadmap 要宣告 ready，必须先做到日常可用：具备 ledger、daily incremental 或明确等价机制、dirty scope、checkpoint/resume、freshness/audit 闭环。 |
| 6 | `POST-DATA-CORE-PRIORITY-MALF-PAS-SIGNAL` | Data 之后的核心兵力优先投入 `MALF -> PAS -> Signal`，因为这三层是本系统不可替代的主权层。 |
| 7 | `LOCAL-TDX-FORMAL-TRUTH-SOURCE` | 正式行情/基础事实真值优先来自 `H:\tdx_offline_Data` 与 `H:\new_tdx64` 的本地通达信资产。 |
| 8 | `NO-NETWORK-PROVIDER-FORMAL-TRUTH` | `TuShare / baostock / AKShare` 等网络 provider 不得成为正式 truth owner；最多只可保留 adapter、参考或实验地位。 |
| 9 | `MOCK-ONLY-FOR-TESTS-AND-PROOF` | mock 只能用于 unit test、contract test、proof harness，不得冒充正式输入真值。 |
| 10 | `ASTERIA-DATA-READ-ONLY-BOOTSTRAP-REFERENCE` | `H:\Asteria-data` 只能作为 Data Foundation 早期 bootstrap 参考和历史大账本经验输入，只读，不得成为当前系统正式 output root。 |
| 11 | `MODULE-DBS-ARE-GOVERNED-SUB-LEDGERS` | 后续各模块数据库都属于同一个历史大账本的受治理分账本，不得被理解成互不相干的散库。 |
| 12 | `ADVANCE-ONLY-AFTER-CHECKS-PASS` | 任何模块 roadmap 都必须先完成本模块数据库、文档、registry、检查闭环，通过后才能推进下一环。 |

## 4. 路线图开启纪律

首张治理 roadmap 已经是：

```text
none / terminal
```

因此后续推进必须遵守：

1. 先新开独立 roadmap。
2. 每张 roadmap 只对应一个模块数据库。
3. 当前模块数据库未 ready 前，不得开下一张 roadmap。
4. 当前模块数据库 ready 的判定，必须同时满足：
   - authority doc 已冻结
   - machine-readable registry 已落地
   - 模块数据库边界已命名
   - development usable 已成立
   - daily usable 已成立
   - repo-local 检查已通过
   - execution 闭环已成立

## 4.1 Ready 双重定义

后续任何模块 roadmap 都不得只用“能支撑下一层开发”来冒充 ready。

`development_usable = true` 必须同时满足：

1. 下游模块能稳定消费本模块输出，不需要猜 schema。
2. contract、schema_version、manifest、lineage、最小消费接口已冻结。
3. 不需要临时 mock 冒充正式 truth。
4. 不需要绕过 source manifest、run lineage 或 schema/rule version。

`daily_usable = true` 必须同时满足：

1. 模块具备自己的 ledger 或受治理分账本。
2. daily incremental、dirty scope、checkpoint/resume、freshness/audit 已形成闭环。
3. 失败后状态可解释、可审计、可续跑或可明确 replan。
4. 若某模块天然不需要 daily incremental，roadmap 必须显式说明“不需要”的理由和替代日常维护机制，不能留空。

## 5. 模块库推进顺序

当前主张固定为：

```text
Data Foundation
-> MALF v1.5
-> PAS v1.2
-> Signal
```

解释如下：

1. `Data Foundation` 先解决正式输入真值和 source manifest 边界。
2. `MALF v1.5` 先把结构行为事实层真正做成开发可用、日常可用的模块数据库。
3. `PAS v1.2` 再把强弱识别和 lifecycle 读法做成开发可用、日常可用的模块数据库。
4. `Signal` 最后只接已成形的候选面，不反向发明 `MALF / PAS` 语义，也不能跳过自身日常可用闭环。

## 6. 数据真值纪律

当前正式输入真值口径固定为：

```text
formal local truth source roots
= H:\tdx_offline_Data
= H:\new_tdx64
```

约束如下：

1. 本地通达信资产是正式 truth source 优先候选。
2. `TuShare / baostock / AKShare` 不得成为正式 truth owner。
3. 网络 provider 就算被保留，也只能停留在 adapter、参考或实验输入层。
4. mock 数据只能用于测试、proof 和 contract harness。
5. 正式模块数据库不得把 mock 混进 source truth。

## 7. 上一版数据库纪律

`H:\Asteria-data` 当前只允许：

1. 作为 `Data Foundation` bootstrap 参考。
2. 作为历史大账本拓扑、formal DB 分层、lineage 经验输入。
3. 作为 `raw_market / market_base_day / market_base_week / market_base_month / market_meta` 这类上游事实层的只读参考。

`H:\Asteria-data` 当前不允许：

1. 作为当前系统正式 output root。
2. 作为当前系统 scratch。
3. 作为 `MALF / PAS / Signal / Position / Trade / System` 语义的直接迁移面。
4. 直接复用上一版下游语义库去跳过本版模块数据库建设。

## 8. 历史大账本纪律

后续所有模块数据库都必须服从：

```text
one logical historical ledger
with governed sub-ledgers
```

这意味着：

1. `Data / MALF / PAS / Signal` 不是四套互不相关的小库。
2. 每个模块库都必须有 lineage、source manifest、schema/rule version 和检查边界。
3. 每个模块库都要能说明自己在历史大账本中的 ledger role。
4. 后续路线图推进顺序，本质上就是按分账本逐个冻结、逐个放行。

## 9. 放行纪律

后续每张模块 roadmap 只有在以下条件满足后，才允许进入下一张：

1. 模块数据库结构边界已冻结。
2. 模块数据库 truth source 已冻结。
3. 模块数据库与上游/下游 handoff 已冻结。
4. `development_usable = true` 已被文档、registry 和检查证明。
5. `daily_usable = true` 已被文档、registry 和检查证明；若例外，必须写明替代日常维护机制。
6. doctor / governance / unittest 已通过。
7. 如有 execution 卡，则四件套与 conclusion index 已同步。

## 10. 人话版结论

这次新增纪律的核心，不是“多写几条规则”，而是把后续开发顺序真正钉死：
先把数据真值源和模块数据库一个个做扎实，再开下一张 roadmap。以后不能再一边开新路线，一边让上一个模块库半成品悬空。

更直白地说，后面的主战场是 `Data 之后的 MALF -> PAS -> Signal`，但它们也不能一口气并行乱冲。
每张 roadmap 只打一个模块库；库没建好、检查没通过，就不准翻到下一张。

现在进一步写死：库“能让下一层开发”还不够。它还必须能被日常维护、日常增量、断点续跑和 freshness/audit
检查接住。开发可用和日常可用缺任何一个，都不能叫 ready。
