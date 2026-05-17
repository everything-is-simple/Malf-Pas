# Market Meta Tradability Calendar Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-meta-tradability-calendar-card-20260517-01` |
| roadmap_order | `023` |
| card type | `Data Foundation market_meta foundational fact ledger build` |

## 2. 本次目标

- 建立 `market_meta.duckdb` 正式基础事实账本。
- 落成 `instrument_master / trade_calendar / tradability_fact / industry_block_relation / source_manifest / schema_version`。
- 固定 `tradability` 只写本地 TDX 直接可证的 `tradable` 正向事实，不推断停牌、ST、退市整理等负向事实。
- 固定 `industry/block relation` 只做当前快照，不做历史区间反推。
- 交付 `build_market_meta_tradability_calendar.py` 与 `validate_market_meta_tradability_calendar.py` 两个 CLI。
- 建立第 23 卡四件套、closeout registry 与 conclusion index 入口。

## 3. 允许动作

- 新增 `src/malf_pas/data_foundation/tdx_meta.py`，实现最小 TDX 静态元数据解析。
- 新增 `src/malf_pas/data_foundation/market_meta.py`，实现 `market_meta` 构建、validator 与 report 输出。
- 新增 `scripts/data_foundation/build_market_meta_tradability_calendar.py` 与 `scripts/data_foundation/validate_market_meta_tradability_calendar.py`。
- 新增 market-meta 单测、CLI 测试与治理检查测试。
- 写入 `H:\Malf-Pas-data\market_meta.duckdb`。
- 输出 report 到 `H:\Malf-Pas-reprot\data-foundation\market-meta-tradability-calendar-card-20260517-01\`。
- 同步 `governance/market_meta_tradability_calendar_registry.toml`、README、docs README、AGENTS、Roadmap 2、conclusion index 与第 23 卡四件套。

## 4. 禁止动作

- 不创建或写入 `data_control.duckdb`，也不提前打开 checkpoint/resume orchestration 或 freshness/readout。
- 不把 open day 缺 bar 解释成停牌、ST、退市整理或任何负向业务事实。
- 不引入 `baostock / AKShare / TuShare` 作为本卡正式 truth owner。
- 不迁移上一版 Asteria schema、runner、DuckDB 表面或旧数据。
- 不进入 MALF / PAS / Signal runtime、broker、paper-live、backtest、收益证明或 live trading。

## 5. 通过标准

- `market_meta.duckdb` 已创建，且六个必需表族全部存在。
- `instrument_master / trade_calendar / tradability_fact / industry_block_relation` 自然键唯一，lineage 完整。
- `tradability_fact` 只包含 `tdx_direct` 正向可证行，不包含伪造负向事实。
- `source_manifest` 已显式登记 `hq_cache / blocknew` 根路径、hash 和 tradability gap 边界。
- `industry/block relation` 已以当前快照闭环，不夸大为历史补齐。
- 本卡不夸大为 Data Foundation ready，也不替代后续 `data_control` / daily incremental / freshness 的模块级闭环。
