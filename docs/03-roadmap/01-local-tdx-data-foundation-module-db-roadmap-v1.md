# Malf-Pas 系统第二张路线图：local-tdx-data-foundation-module-db-roadmap-v1

日期：2026-05-16

状态：frozen-by-card-018 / post-terminal separate roadmap

## 1. 定位

本路线图是 `Malf-Pas` 系统的第二张 roadmap。

它接力第一张治理路线图：

```text
docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md
```

第一张 roadmap 已经收口为：

```text
none / terminal
```

因此本路线图不是继续占用第一张治理路线图，也不是重开治理初始化路线；它是第一张路线图之后的新独立
post-terminal roadmap。

本路线图只对应一个模块数据库边界：

```text
Data Foundation
```

## 2. 一句话目标

本路线图不是去“分析市场”，而是先把 `Malf-Pas` 的正式本地数据粮道和第一个正式模块库建好。

更具体地说：冻结本地通达信正式 truth source，并把 Data Foundation 做成一个同时满足
`development_usable = true` 与 `daily_usable = true` 的历史大账本分账本。

## 3. 系统接力关系

| 系统路线 | 文档 | 状态 | 作用 |
|---:|---|---|---|
| Roadmap 1 | `00-malf-pas-governance-roadmap-v1.md` | `terminal / governance-only completed` | 立法、锚点、模块所有权、历史大账本协议、日更协议、adapter 边界 |
| Roadmap 2 | `01-local-tdx-data-foundation-module-db-roadmap-v1.md` | `frozen-by-card-018` | 建设 Data Foundation 模块库与日常维护闭环 |
| Roadmap 3 | 待 Data closeout passed 后新开 | `not opened` | `MALF v1.5` 模块数据库路线 |

Roadmap 2 完成前，不得开启 Roadmap 3。

## 4. 共通边界

本路线图共享以下边界：

```text
doc-first
one-roadmap-one-module-db
read-only-to-previous-assets
no-legacy-code-migration
no-broker
no-profit-claim
no-downstream-semantic-db
development-usable-required
daily-usable-required
```

本路线图允许后续卡申请和冻结的写入授权只能是：

```text
Data Foundation only
H:\Malf-Pas-data only
```

该授权不得外溢到：

```text
MALF
PAS
Signal
Position
Portfolio Plan
Trade
System Readout
Pipeline runtime
broker
paper-live
backtest
profit proof
```

## 5. 正式 truth source

本路线图冻结 Data Foundation 的正式本地 truth source 优先根为：

```text
H:\tdx_offline_Data
H:\new_tdx64
```

本路线图必须先通过只读盘点证明这两个根的可读性、目录族、文件族、时间覆盖、资产覆盖和 fingerprint 策略。

`TuShare / baostock / AKShare` 不得成为正式 truth owner。后续若保留 provider，也只能是 adapter、参考或实验输入，
不得替代本地 TDX truth source。

mock 只能用于：

```text
unit test
contract test
proof harness
```

mock 不得冒充正式 truth。

## 6. 只读参考边界

以下路径只允许只读吸收经验，不得迁移旧 schema、runner、DuckDB 表面或旧代码：

```text
H:\Asteria-data
G:\malf-history\Asteria
G:\malf-history\Asteria-report
G:\malf-history\Asteria-Validated
G:\malf-history\astock_lifespan-alpha
G:\malf-history\EmotionQuant-alpha
G:\malf-history\EmotionQuant-beta
G:\malf-history\EmotionQuant-gamma
G:\malf-history\lifespan-0.01
G:\malf-history\MarketLifespan-Quant
```

允许吸收的经验包括：

1. `raw_market` 文件级 registry、source manifest、run audit、reject audit。
2. `market_base_day/week/month` 物化规则、latest pointer、dirty scope、自然键唯一性。
3. `market_meta` 的 symbol master、calendar、tradability、industry/block relation。
4. daily incremental、manifest diff、checkpoint/resume、fingerprint mismatch 拒绝。
5. release audit、DB readiness、read-only open、row count、required table、closeout 证据组织。

禁止吸收为当前事实的内容包括：

1. 旧业务模块语义。
2. 旧下游 DB。
3. 旧 runner 原样迁移。
4. 历史收益、回测截图或 broker 结论。

## 7. Data 模块库范围

本路线图的 Data Foundation 模块库范围固定为：

| DB | ledger role | 职责 |
|---|---|---|
| `raw_market.duckdb` | `source_fact_raw_ledger` | 原始 TDX 文件登记、原始 bar、ingest run、reject audit、source manifest |
| `market_base_day.duckdb` | `source_fact_base_day_ledger` | day 基础行情事实、latest pointer、dirty scope、analysis price line |
| `market_base_week.duckdb` | `source_fact_base_week_ledger` | week 基础行情事实、latest pointer、dirty scope、direct source 或 day raw 派生 lineage |
| `market_base_month.duckdb` | `source_fact_base_month_ledger` | month 基础行情事实、latest pointer、dirty scope、direct source 或 day raw 派生 lineage |
| `market_meta.duckdb` | `source_fact_meta_ledger` | symbol master、calendar、tradability、industry/block relation、source manifest |
| `data_control.duckdb` | `data_orchestration_control_ledger` | Data run ledger、dirty queue、checkpoint、resume state、audit state；freshness audit/readout 必须以独立表族表达 |

这些库是同一个逻辑历史大账本的 Data 受治理分账本，不得被理解成散库集合。

`data_control.duckdb` 允许同时承载 orchestration control facts 与 Data freshness/readout surface，
但必须用独立表族表达，不得把 run ledger、checkpoint、resume state、freshness readout 混写进单一万能控制表。

## 8. 数据范围

本路线图首版 Data Foundation 覆盖范围固定为：

```text
asset_type = stock / index / block
timeframe = day / week / month
```

`day` 优先直接来自本地 TDX source。

`week / month` 的来源规则必须在 source manifest 和 lineage 中显式表达：

1. 若本地 TDX 存在可读 direct source，则优先登记 direct source。
2. 若 direct source 不完整或不可用，可从 `day raw` 做确定性派生。
3. 无论 direct source 还是 day-derived，都必须保留 `source_manifest_hash`、`source_run_id`、`schema_version` 与派生规则版本。

## 9. 共同治理键

Data Foundation 后续表、manifest、checkpoint 和 readout 必须预留并使用以下共同治理键：

```text
symbol
asset_type
timeframe
bar_dt
trade_dt
run_id
source_run_id
schema_version
rule_version
source_manifest_hash
checkpoint_key
```

业务事实自然键不得依赖 `run_id`。`run_id` 只作为运行审计、lineage 和断点续传线索。

## 10. Ready 双重标准

本路线图不得用“能支撑后续开发”冒充 ready。

`development_usable = true` 必须证明：

1. 下游 `MALF v1.5` 可以稳定消费 Data 输出，不需要猜 schema。
2. Data contract、schema_version、source manifest、lineage 和最小消费接口已冻结。
3. 不需要 mock 冒充正式 truth。
4. 不需要绕过 manifest、run lineage 或 schema/rule version。

`daily_usable = true` 必须证明：

1. Data 具备自己的 run ledger 和受治理分账本。
2. daily incremental、dirty scope、checkpoint/resume、freshness/audit 已形成闭环。
3. 失败后状态可解释、可审计、可续跑或可明确 replan。
4. 同一输入重复运行不产生业务事实重复，自然键唯一，latest pointer 唯一。
5. checkpoint fingerprint mismatch 时必须拒绝错误 resume，并要求 replan 或 reset。

## 11. 路线图卡序

本路线图的 execution card 编号继续接当前 conclusion index，从 `018` 开始。

| 顺序 | 卡 | 目标 | 通过口径 |
|---:|---|---|---|
| 18 | `data-foundation-roadmap-freeze-card` | 冻结系统第 2 张 roadmap、Data-only mutation 授权、与第 1 张 terminal roadmap 的接力关系 | roadmap 文档、Data-only scope、禁止下游范围同步、registry 与四件套闭环 |
| 19 | `local-tdx-source-inventory-card` | 只读盘点两个本地 TDX truth roots | source family、file family、fingerprint、week/month direct source 可用性结论、tradability 来源可用性结论、manifest 规则冻结 |
| 20 | `data-module-db-contract-card` | 冻结 Data 六库 contract、表族、自然键、共同治理键、lineage | schema/manifest/lineage/minimal consumer contract、Data validator 最小骨架、`raw_market.ingest_run` 与 `data_control.run_ledger` 的关系冻结 |
| 21 | `raw-market-full-build-ledger-card` | 建立 `raw_market` 文件级历史账本 | source file、raw bar、ingest run、reject audit、skipped/failed 记录通过 |
| 22 | `market-base-day-week-month-build-card` | 建立 day/week/month base 物化账本 | bar/latest/run/dirty_scope、自然键唯一、lineage 完整 |
| 23 | `market-meta-tradability-calendar-card` | 建立 `market_meta` 基础事实账本 | symbol master、calendar、tradability、industry/block relation、tradability 来源边界通过 |
| 24 | `data-control-run-ledger-checkpoint-card` | 建立 `data_control` 控制账本 | run ledger、dirty queue、checkpoint、resume state、audit state、orchestration/readout 表族边界通过 |
| 25 | `data-daily-incremental-resume-card` | 建立 Data daily runner 和续跑闭环 | manifest diff、dirty scope、resume_strict、idempotence 通过 |
| 26 | `data-freshness-audit-readout-card` | 建立 freshness audit/readout | source/base 最新日、lag、missing、stale、blocked reason 可读 |
| 27 | `data-foundation-release-audit-closeout-card` | 对 Data 六库做 release audit 并收口 | repo-local checks、Data validator、四件套、conclusion index 全部通过 |

## 12. 各卡详细边界

### 12.1 `018-data-foundation-roadmap-freeze-card`

目标：

1. 把本文件登记为系统第二张 roadmap。
2. 证明它接力第一张 `none / terminal` roadmap。
3. 冻结本路线图只对应 `Data Foundation` 一个模块数据库边界。
4. 将 `formal DB mutation = no` 收窄为后续 Data 卡可申请的 `Data Foundation only` 授权。

禁止：

1. 创建 Data DB。
2. 打开 MALF / PAS / Signal runtime。
3. 宣告 Data ready。

闭环结果：

```text
run_id = data-foundation-roadmap-freeze-card-20260517-01
status = passed
registry = governance/data_foundation_roadmap_registry.toml
next_data_foundation_card = local-tdx-source-inventory-card
```

本卡通过后，只表示 Roadmap 2 和 Data-only 授权边界已冻结；不表示 `H:\Malf-Pas-data`
已经写入，也不表示 Data Foundation 已经 development usable 或 daily usable。

### 12.2 `019-local-tdx-source-inventory-card`

目标：

1. 只读盘点 `H:\tdx_offline_Data`。
2. 只读盘点 `H:\new_tdx64`。
3. 冻结 stock/index/block 与 day/week/month 的 source family。
4. 冻结 file fingerprint 策略：path、size、mtime、content hash、source root、source revision。
5. 产出 week/month direct source 可用性结论。
6. 产出 tradability 来源可用性结论。
7. 产出 source inventory readout。

禁止：

1. 写入 `H:\Malf-Pas-data`。
2. 修改 TDX 源目录。
3. 用网络 provider 补正式 truth。

通过标准：

1. source family、file family 与 fingerprint 规则可读、可审计。
2. week/month direct source 可用性结论必须明确写成 `direct / day-derived / blocked` 之一，不得保持隐含假设。
3. 若 week/month direct source 不完整或不可用，必须登记 day-derived 所需的 direct parent、manifest 与 rule version 输入边界。
4. tradability 来源可用性结论必须明确写出 `TDX direct / authorized source_adapter / blocked`。
5. 若 tradability 需要 adapter 补充，必须同时登记 gap 范围，不得把 adapter 默认升级为 formal truth owner。

### 12.3 `020-data-module-db-contract-card`

目标：

1. 冻结 Data 六库表族与最小字段。
2. 冻结业务自然键与治理键。
3. 冻结 source manifest、schema_version、rule_version、lineage 字段。
4. 冻结下游最小消费接口，第一消费者为 `MALF v1.5`。
5. 冻结 `raw_market.ingest_run` 与 `data_control.run_ledger` 的关系：前者是 source ingest 局部审计，后者是 module-level orchestration 审计。
6. 冻结 `data_control` 内 orchestration table families 与 freshness/readout table families 分离边界。
7. 冻结 tradability 来源登记 contract；若需 adapter 补充，必须以 authorized `source_adapter` 角色显式登记。
8. 交付 Data validator 最小骨架：entrypoint、contract assertions、fixture boundary。

禁止：

1. 让 Data 输出 MALF/PAS/Signal 语义。
2. 让 run_id 成为业务事实自然键。
3. 迁移历史 repo schema。

通过标准：

1. 六库 contract、自然键、治理键、schema_version、rule_version、source manifest 与 lineage 字段全部冻结。
2. `raw_market.ingest_run` 与 `data_control.run_ledger` 的关系写实，不允许后续以“迁移 audit 语义”掩盖边界不清。
3. `data_control` 的 orchestration table families 与 freshness/readout table families 分离边界写实。
4. tradability 来源登记 contract 明确到字段与 source role，不允许留空或默认为本地 truth。
5. Data validator 最小骨架在本卡冻结，并可被后续卡直接接入 contract / validator / fixture tests。

### 12.4 `021-raw-market-full-build-ledger-card`

目标：

1. 建立 raw file registry。
2. 建立 raw bar 历史账本。
3. 建立 raw ingest run audit。
4. 支持 full、bounded、audit-only、resume、daily_incremental 模式边界。
5. 证明 unchanged source 可被 `skipped_unchanged` 审计。

通过标准：

1. raw source trace 完整。
2. raw natural key 唯一。
3. failed/rejected source 有审计记录。
4. 同输入重跑不重复写业务事实。
5. raw ingest run audit 只证明 source ingest 局部审计，不替代 `data_control.run_ledger` 的 module-level orchestration 审计。

### 12.5 `022-market-base-day-week-month-build-card`

目标：

1. 建立 `market_base_day.duckdb`。
2. 建立 `market_base_week.duckdb`。
3. 建立 `market_base_month.duckdb`。
4. 建立 `market_base_bar`、`market_base_latest`、`market_base_run`、`market_base_dirty_scope`。
5. 冻结 `analysis_price_line = backward` 的下游分析口径。

通过标准：

1. day/week/month 的 row count、symbol count、日期跨度可审计。
2. latest pointer 唯一。
3. 自然键唯一。
4. week/month 的 direct 或 derived lineage 可解释。

### 12.6 `023-market-meta-tradability-calendar-card`

目标：

1. 建立 symbol master。
2. 建立 trade calendar。
3. 建立 asset type、exchange、industry/block relation。
4. 建立 tradability fact。
5. 登记停牌、ST、退市整理等基础可交易事实的来源边界。

通过标准：

1. `market_meta` 可回答“这个标的是什么、哪天能不能交易、属于什么基础分类”。
2. 不输出交易动作、仓位、订单或收益语义。
3. tradability fact 的 source manifest 必须显式登记来源；若非本地 TDX direct 给出，必须指向已授权 `source_adapter`，不得留空。

### 12.7 `024-data-control-run-ledger-checkpoint-card`

目标：

1. 建立 Data run ledger。
2. 建立 dirty queue / dirty scope。
3. 建立 checkpoint。
4. 建立 resume state。
5. 建立 audit state。
6. 建立 orchestration table families 与 freshness/readout table families 的分离边界。

通过标准：

1. checkpoint 必须绑定 dirty scope、manifest、schema、rule 与 lineage。
2. checkpoint 只能证明批次进度，不能替代 audit。
3. failed/blocked batch 不得被 resume 跳过。
4. `data_control` 即使与 freshness/readout 同库，也必须保持 orchestration table families 与 freshness/readout table families 分离。

### 12.8 `025-data-daily-incremental-resume-card`

目标：

1. 从 source manifest diff 推导 dirty scope。
2. 从最早受影响日期重放到 target as-of date。
3. 默认使用 `resume_strict`。
4. 支持 `resume_replan`、`restart_from_manifest`、`audit_only`、`no_op_audited` 的治理边界。
5. 证明幂等重跑。

通过标准：

1. source changed / added / removed 能形成 dirty scope。
2. dirty scope 为空时只能形成 `no-op audited`。
3. fingerprint mismatch 必须拒绝错误 resume。
4. audit failed 或 lineage gap 必须 blocked。

### 12.9 `026-data-freshness-audit-readout-card`

目标：

1. 输出 source 最新日期。
2. 输出 raw/base/meta/control 最新状态。
3. 输出 lag、missing source、stale ledger、dirty backlog。
4. 输出 blocked reason 与建议补采窗口。

通过标准：

1. 人能读懂 Data 当前是否新鲜。
2. 机器能消费 freshness status。
3. 不把 stale / missing 伪装成 ready。

### 12.10 `027-data-foundation-release-audit-closeout-card`

目标：

1. 对 Data 六库做 release audit。
2. 跑 repo-local checks。
3. 跑 Data validator。
4. 落 execution 四件套。
5. 更新 conclusion index。
6. 明确是否允许开启 Roadmap 3。

通过标准：

```text
development_usable = true
daily_usable = true
doctor passed
governance check passed
unittest passed
Data validator passed
card / evidence-index / record / conclusion complete
conclusion index synced
```

## 13. Data validator 必须检查

Data validator 最小 entrypoint、contract assertions 与 fixture boundary 必须在 `020-data-module-db-contract-card`
冻结，并在后续 Data runtime 卡中持续可运行。

Data validator 至少必须证明：

1. Roadmap 2 明确接力 Roadmap 1，而不是重开治理路线。
2. Data DB 只写入 `H:\Malf-Pas-data`。
3. `H:\Asteria-data` 与 `G:\malf-history\*` 只读参考。
4. `stock / index / block` 与 `day / week / month` 已被 manifest/registry 覆盖。
5. `raw_market / market_base_day / market_base_week / market_base_month / market_meta / data_control` 均存在。
6. 必需表族存在且非空，冷启动例外必须明确写出。
7. source manifest 可重放。
8. natural key 唯一。
9. latest pointer 唯一。
10. schema_version 已登记。
11. run lineage 完整。
12. dirty scope 可追溯。
13. checkpoint 可恢复。
14. freshness audit 可读。
15. Data 不输出任何 MALF/PAS/Signal/Position/Trade/System 语义。

## 14. repo-local 检查

本路线图每张施工卡关闭前至少运行：

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

涉及 Data runtime 或 validator 的卡，还必须运行对应 Data contract / validator / fixture tests。

## 15. 出场条件

本路线图只有在 `027-data-foundation-release-audit-closeout-card` passed 后，才允许宣告 Data Foundation ready。

ready 结论必须拆开写：

```text
implementation complete = true / false
development_usable = true / false
daily_usable = true / false
validation_closeout_complete = true / false
next_roadmap_allowed = true / false
```

只有以下全部为 true，才允许开启下一张 roadmap：

```text
development_usable = true
daily_usable = true
validation_closeout_complete = true
next_roadmap_allowed = true
```

下一张 roadmap 固定为：

```text
MALF v1.5 module DB roadmap
```

## 16. 明确不做

本路线图不做：

1. MALF v1.5 模块库。
2. PAS v1.2 模块库。
3. Signal 模块库。
4. Position / Portfolio Plan / Trade / System Readout。
5. broker / live trading / paper-live。
6. backtest / 收益证明。
7. 历史 repo schema 或 runner 迁移。
8. 网络 provider 正式 truth owner。
9. repo 根目录临时 DB、报告、cache 或 scratch。

## 17. 人话版结论

这张路线图就是系统第二步：先把数据粮道修成正式道路。

它不负责判断市场强弱，也不负责给交易信号。它只负责把本地通达信数据变成一个可追溯、可日更、可断点续跑、
可审计、可被下游稳定消费的 Data Foundation 模块库。

这张路不走完，后面的 `MALF v1.5 -> PAS v1.2 -> Signal` 都不准开工。
