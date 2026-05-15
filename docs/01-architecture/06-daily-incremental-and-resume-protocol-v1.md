# Daily Incremental And Resume Protocol v1

日期：2026-05-15

状态：frozen-by-daily-incremental-and-resume-protocol-card-20260515-01

## 1. 目标

本文件冻结 `Malf-Pas` 第一阶段的每日增量、dirty scope、checkpoint、resume 与 staging
promote 协议。

本卡只定义治理协议，不创建正式数据库，不执行 schema migration，不实现 runner，不授权 runtime build。

## 2. Daily Incremental Principle

每日增量不是“只算今天一行”，而是从 `source_manifest` 和 dirty scope 推导需要重算的最小可证明影响面。

| 原则 | 裁决 |
|---|---|
| input authority | `source_manifest` 是输入集合证明 |
| impact unit | dirty scope 必须绑定 `symbol / timeframe / date range / ledger_role` |
| replay boundary | 从最早受影响日期开始重放到目标 as-of 日期 |
| downstream propagation | 上游 dirty scope 必须沿主线向下游传播 |
| proof boundary | 没有 manifest、lineage、checkpoint 和 audit 的输出不得 promote |
| formal DB mutation | `no` |

## 3. Dirty Scope Protocol

dirty scope 是每日增量的影响面账册。每个 dirty item 必须至少包含：

| field | 说明 |
|---|---|
| `dirty_scope_id` | dirty scope 自身稳定标识 |
| `ledger_role` | 受影响账本角色，如 `source_fact`、`structure_fact`、`semantic_ledger` |
| `symbol` | 标的；组合级或全局项可用治理约定的 aggregate key |
| `timeframe` | `day / week / month` 等周期 |
| `dirty_start_dt` | 最早受影响日期 |
| `dirty_end_dt` | 本次目标重算截止日期 |
| `dirty_reason` | `source_changed / source_added / source_removed / rule_changed / schema_changed / lineage_gap / audit_failed / manual_review` |
| `source_manifest_hash` | 输入集合指纹 |
| `source_run_id` | 直接上游 run |
| `schema_version` | schema 合同版本 |
| `rule_version` | 业务规则版本 |
| `status` | `pending / planned / replaying / audited / blocked / promoted` |

dirty scope 推导规则：

1. source manifest 变化必须生成 `source_fact` dirty scope。
2. schema 或 rule 变化必须从该规则覆盖的最早日期开始重放。
3. lineage gap 或 audit failed 必须从缺口或失败点开始重放，不得只重跑当天。
4. 上游 dirty scope 通过 `source_run_id` 与 `source_manifest_hash` 传播给下游账本。
5. dirty scope 为空时，只能形成 `no-op audited` 结论，不能伪造 promote。

## 4. Checkpoint Protocol

checkpoint 是断点续传与批次审计的定位锚点，不是业务事实。

每个 checkpoint 必须至少包含：

| field | 说明 |
|---|---|
| `checkpoint_key` | 稳定 checkpoint key |
| `run_id` | 当前 run |
| `batch_id` | 当前 batch |
| `ledger_role` | 账本角色 |
| `symbol` | 标的或 aggregate key |
| `timeframe` | 周期 |
| `dirty_scope_id` | 对应 dirty scope |
| `processed_start_dt` | 已处理范围起点 |
| `processed_end_dt` | 已处理范围终点 |
| `source_manifest_hash` | 输入集合指纹 |
| `source_run_id` | 直接上游 run |
| `schema_version` | schema 合同版本 |
| `rule_version` | 业务规则版本 |
| `status` | `pending / running / passed / blocked / failed` |
| `audit_status` | `pending / passed / blocked / failed` |

checkpoint 规则：

1. checkpoint 必须绑定 dirty scope，不得独立漂移。
2. checkpoint 只能证明批次进度，不能替代 audit。
3. checkpoint 缺失或状态不一致时，不得宣告 resume passed。
4. checkpoint 所绑定的 manifest、schema、rule 任一变化，都必须触发 replan 或 restart。

## 5. Resume Mode Protocol

resume mode 固定为以下治理枚举：

| resume_mode | 允许行为 | 禁止行为 |
|---|---|---|
| `resume_strict` | 在 manifest、schema、rule 全部一致时从最后 passed checkpoint 继续 | 跳过 failed / blocked batch |
| `resume_replan` | manifest、schema、rule 变化后重算 dirty scope 并废弃不兼容 checkpoint | 复用旧 checkpoint 伪装连续执行 |
| `restart_from_manifest` | 从 source manifest 和 dirty scope 起点完整重放 | 保留旧 working facts 当成正式输出 |
| `audit_only` | 只审计现有 working facts、checkpoint 与 lineage | 写入正式 DB 或 promote |
| `no_op_audited` | dirty scope 为空时记录无变更结论 | 生成新的业务事实 |

默认 resume mode 是 `resume_strict`。任何越过 upstream blocked、audit failed 或 lineage gap 的 resume
都必须判定为 blocked。

## 6. Staging Promote Protocol

staging promote 是从 working facts 到正式账本的治理门，不是简单文件覆盖。

promote 必须满足：

1. dirty scope 全部 `audited`。
2. checkpoint 全部 `passed`。
3. source manifest、schema_version、rule_version、run lineage 完整。
4. batch audit 与 ledger audit 均为 `passed`。
5. promote record 写入 execution 四件套或后续正式 promote ledger。

promote 禁止：

1. 半成品 working facts 污染正式账本。
2. 在 audit failed、lineage gap、manifest mismatch 时 promote。
3. 假设跨库事务原子性。
4. 把 `H:\Asteria-data` 当作 `Malf-Pas` 当前系统数据落点或 scratch。

当前阶段仍不授权写入 `H:\Malf-Pas-data`，因此本协议只冻结未来 promote 的门禁条件。
备份包、历史经验、报告和临时产物必须分别落在 `H:\Malf-Pas-backup`、
`H:\Malf-Pas-Validated`、`H:\Malf-Pas-reprot`、`H:\Malf-Pas-temp`；
上一版 `H:\Asteria-*` 目录只读参考，不得参与 staging promote。

## 7. Mainline Propagation

dirty scope 的下游传播顺序固定为：

```text
source_fact
-> structure_fact
-> semantic_ledger
-> decision_ledger
-> management_ledger
-> portfolio_plan_ledger
-> execution_ledger
-> readout_ledger
```

`Pipeline` 只记录 run、manifest、checkpoint、resume trace、batch audit 和 promote trace；
它不得改变任一业务账本的语义。

## 8. Invariants

| invariant_id | invariant |
|---|---|
| `DAILY-INCREMENTAL-MANIFEST-FIRST` | 每日增量必须先从 source manifest 与 dirty scope 推导影响面 |
| `DIRTY-SCOPE-REPLAYS-FROM-EARLIEST-AFFECTED-DATE` | dirty scope 必须从最早受影响日期重放，不得只算当天 |
| `CHECKPOINT-BINDS-DIRTY-SCOPE` | checkpoint 必须绑定 dirty scope、manifest、schema、rule 与 lineage |
| `RESUME-CANNOT-SKIP-BLOCKED-UPSTREAM` | resume 不得跳过 blocked upstream、audit failed 或 lineage gap |
| `STAGING-PROMOTE-REQUIRES-AUDIT-PASSED` | working facts 只有 audit passed 且 lineage 完整后才能 promote |
| `NO-FORMAL-DB-MUTATION` | 当前阶段不得写入正式 DB 或正式数据根目录 |
