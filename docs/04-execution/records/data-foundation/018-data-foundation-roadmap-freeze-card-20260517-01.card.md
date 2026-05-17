# Data Foundation Roadmap Freeze Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `data-foundation-roadmap-freeze-card-20260517-01` |
| roadmap_order | `018` |
| card type | `post-terminal roadmap freeze / Data Foundation boundary authorization` |

## 2. 本次目标

- 把 `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md` 冻结为系统第二张 roadmap。
- 证明 Roadmap 2 接力第一张 `none / terminal` governance roadmap，而不是重开首张路线。
- 冻结 Roadmap 2 只对应 `Data Foundation` 一个模块数据库边界。
- 将当前 `formal DB mutation = no` 收窄为后续 Data 卡可申请的 `Data Foundation only` 授权口径。
- 建立第 18 卡 repo-local execution 四件套与 conclusion index 入口。

## 3. 允许动作

- 更新 Roadmap 2 文档状态和第 18 卡闭环入口。
- 新增 `governance/data_foundation_roadmap_registry.toml`。
- 同步 repo registry、governance README、README、docs README、AGENTS 与治理检查。
- 新增第 18 卡四件套并登记进结论索引。

## 4. 禁止动作

- 不创建 `raw_market.duckdb`、`market_base_day.duckdb`、`market_base_week.duckdb`、`market_base_month.duckdb`、`market_meta.duckdb` 或 `data_control.duckdb`。
- 不写入 `H:\Malf-Pas-data`。
- 不打开 MALF / PAS / Signal / Position / Trade / Pipeline runtime。
- 不进入 broker、paper-live、backtest、收益证明或 live trading。
- 不迁移历史 repo schema、runner、DuckDB 表面或 legacy code。

## 5. 通过标准

- Roadmap 2 状态为 `frozen-by-card-018`。
- 机器可读 registry 明确 `module_db_boundary = Data Foundation`。
- registry 明确本卡不建库、不写数据根，后续授权只限 `Data Foundation only`。
- conclusion index 登记第 18 卡。
- repo-local doctor、governance check 与 unittest 通过。
