# Malf-Pas Post-Terminal Roadmap And Module-DB Discipline v1

日期：2026-05-16

状态：adopted-after-first-governance-roadmap-terminal

## 1. 目的

本文件冻结首张治理 roadmap 收口之后的新纪律。

它回答 3 个问题：

1. 后续 roadmap 该怎么开。
2. 每张 roadmap 和模块数据库之间是什么关系。
3. 数据真值、mock、上一版数据库和检查放行该如何约束。

## 2. 本次新增纪律总数

本次一共新增 `10` 条系统纪律。

## 3. 十条纪律

| order | rule_id | discipline |
|---:|---|---|
| 1 | `POST-TERMINAL-SEPARATE-ROADMAP-ONLY` | 首张治理 roadmap 收口后，后续工作必须新开独立 roadmap，不得继续占用已 terminal 的治理路线图。 |
| 2 | `ONE-ROADMAP-ONE-MODULE-DB` | 每一张新 roadmap 必须对应一个模块数据库或一个模块账本边界，不得一张 roadmap 同时跨多个核心模块数据库。 |
| 3 | `CURRENT-MODULE-DB-READY-BEFORE-NEXT-ROADMAP` | 当前 roadmap 对应的模块数据库未建好、未通过检查、未形成闭环前，不得开启下一张 roadmap。 |
| 4 | `POST-DATA-CORE-PRIORITY-MALF-PAS-SIGNAL` | Data 之后的核心兵力优先投入 `MALF -> PAS -> Signal`，因为这三层是本系统不可替代的主权层。 |
| 5 | `LOCAL-TDX-FORMAL-TRUTH-SOURCE` | 正式行情/基础事实真值优先来自 `H:\tdx_offline_Data` 与 `H:\new_tdx64` 的本地通达信资产。 |
| 6 | `NO-NETWORK-PROVIDER-FORMAL-TRUTH` | `TuShare / baostock / AKShare` 等网络 provider 不得成为正式 truth owner；最多只可保留 adapter、参考或实验地位。 |
| 7 | `MOCK-ONLY-FOR-TESTS-AND-PROOF` | mock 只能用于 unit test、contract test、proof harness，不得冒充正式输入真值。 |
| 8 | `ASTERIA-DATA-READ-ONLY-BOOTSTRAP-REFERENCE` | `H:\Asteria-data` 只能作为 Data Foundation 早期 bootstrap 参考和历史大账本经验输入，只读，不得成为当前系统正式 output root。 |
| 9 | `MODULE-DBS-ARE-GOVERNED-SUB-LEDGERS` | 后续各模块数据库都属于同一个历史大账本的受治理分账本，不得被理解成互不相干的散库。 |
| 10 | `ADVANCE-ONLY-AFTER-CHECKS-PASS` | 任何模块 roadmap 都必须先完成本模块数据库、文档、registry、检查闭环，通过后才能推进下一环。 |

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
   - repo-local 检查已通过
   - execution 闭环已成立

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
2. `MALF v1.5` 先把结构行为事实层真正做成模块数据库。
3. `PAS v1.2` 再把强弱识别和 lifecycle 读法做成模块数据库。
4. `Signal` 最后只接已成形的候选面，不反向发明 `MALF / PAS` 语义。

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
4. doctor / governance / unittest 已通过。
5. 如有 execution 卡，则四件套与 conclusion index 已同步。

## 10. 人话版结论

这次新增纪律的核心，不是“多写几条规则”，而是把后续开发顺序真正钉死：
先把数据真值源和模块数据库一个个做扎实，再开下一张 roadmap。以后不能再一边开新路线、一边让上一个模块库半成品悬空。

更直白地说，后面的主战场是 `Data 之后的 MALF -> PAS -> Signal`，但它们也不能一口气并行乱冲。
每张 roadmap 只打一个模块库；库没建好、检查没通过，就不准翻到下一张。
