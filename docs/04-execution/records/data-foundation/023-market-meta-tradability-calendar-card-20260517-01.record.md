# Market Meta Tradability Calendar Record

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-meta-tradability-calendar-card-20260517-01` |
| result | `passed` |

## 2. 执行顺序

1. 读取 live authority docs、Roadmap 2、conclusion index、repo governance registry、market-base closeout 与 Data contract registry。
2. 先写第 23 卡红灯测试，要求 market-meta runtime、TDX 静态 parser、build/validator CLI、closeout registry 与四件套必须存在。
3. 新增 `src/malf_pas/data_foundation/tdx_meta.py`，实现 `base.dbf / *.tnf / tdxhy.cfg / tdxzs.cfg / blocknew/*` 的最小解析层。
4. 新增 `src/malf_pas/data_foundation/market_meta.py`，实现 symbol master、trade calendar、tradability、industry/block relation、validator 与 report 输出。
5. 先跑本地 fixture 单测，确认 direct-proven tradability、current-snapshot relation 与空 TNF 兼容成立。
6. 对真实数据先跑 bounded smoke，确认 scope 过滤真的只约束当前 symbol 集，而不是把整库 tradability 误写进 bounded 结果。
7. 对正式 `raw_market.duckdb` 与 `market_base_day.duckdb` 跑 full build，创建 `H:\Malf-Pas-data\market_meta.duckdb`。
8. 复跑 validator，抓取 row count、自然键唯一、lineage 与 unresolved gap 指标。
9. 同步 `governance/market_meta_tradability_calendar_registry.toml`、README、docs README、AGENTS、root policy、module gate、Roadmap 2、conclusion index 与第 23 卡四件套。

## 3. 关键验证

| 验证项 | 结果 |
|---|---|
| fixture ledger tests | `passed / direct tradability only / current snapshot relation only` |
| CLI tests | `passed / build + validate JSON summary available` |
| bounded smoke build | `passed / 5 symbols / tradability 2777 / unresolved_gap_count 4178` |
| full build | `passed / instrument 7669 / calendar 18676 / tradability 19212175 / relation 7898` |
| relation breakdown | `industry 5508 / block 2390` |
| natural keys | `instrument_master / trade_calendar / tradability_fact / industry_block_relation all unique` |
| lineage | `complete` |
| tradability policy | `tdx_direct_only / no_inferred_negative_facts` |
| current live write scope | `H:\Malf-Pas-data\market_base_day.duckdb / market_base_week.duckdb / market_base_month.duckdb / market_meta.duckdb` |
| downstream runtime scope | `not opened` |

## 4. 重要说明

- 本卡把 `tradability` 收口为“正向可证事实优先”。也就是说，只有 `trade_calendar` 为 open 且 `market_base_day` 存在 bar 的 `(symbol, trade_dt)` 才会写成 `tradable`。
- open day 缺 bar 目前不被伪装成停牌、ST、退市整理或任何负向业务事实，因此 full build 仍保留 `7669` 个 unresolved symbol 和 `44854914` 个 unresolved gap。这是当前 truth boundary 的真实结果，不是 bug 修饰。
- `industry_block_relation` 只落当前快照，不做历史区间反推；`effective_to` 固定为空。
- 第 23 卡完成后，只能说明 `market_meta` 的基础事实层已成形；Data Foundation 的 `daily_usable` 总体 ready 仍未宣告。

## 5. 后续要求

- 下一张 Data Foundation 卡为 `data-control-run-ledger-checkpoint-card`。
- 第 24 卡只允许建立 `data_control` 控制账本，不得回头重定义第 23 卡对 `tradability`、`negative_fact_policy` 或 `industry_block_snapshot_mode` 的边界。
- 第 25-26 卡继续承担 daily incremental、checkpoint/resume、freshness/readout 的系统闭环，不得被第 23 卡“已建库”的表述替代。

## 6. 文档更新

- `src/malf_pas/data_foundation/tdx_meta.py`
- `src/malf_pas/data_foundation/market_meta.py`
- `scripts/data_foundation/build_market_meta_tradability_calendar.py`
- `scripts/data_foundation/validate_market_meta_tradability_calendar.py`
- `tests/data_foundation/support_tdx_meta_fixtures.py`
- `tests/data_foundation/test_market_meta_ledger.py`
- `tests/data_foundation/test_market_meta_cli.py`
- `src/malf_pas/governance/checks.py`
- `tests/governance/test_governance_checks.py`
- `pyproject.toml`
- `governance/repo_governance_registry.toml`
- `governance/module_gate_registry.toml`
- `governance/data_foundation_roadmap_registry.toml`
- `governance/root_directory_registry.toml`
- `governance/market_meta_tradability_calendar_registry.toml`
- `README.md`
- `AGENTS.md`
- `docs/README.md`
- `docs/00-governance/04-root-directory-policy-v1.md`
- `governance/README.md`
- `governance/module_api_contracts/README.md`
- `docs/04-execution/00-conclusion-index-v1.md`
