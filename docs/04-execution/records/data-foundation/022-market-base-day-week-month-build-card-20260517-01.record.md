# Market Base Day Week Month Build Record

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `market-base-day-week-month-build-card-20260517-01` |
| result | `passed` |

## 2. 执行顺序

1. 读取 live authority docs、Roadmap 2、conclusion index、repo governance registry、Data contract registry 与 raw-market closeout。
2. 先写第 22 卡红灯测试，要求 market-base runtime、build/validator CLI、closeout registry 与四件套必须存在。
3. 新增 `src/malf_pas/data_foundation/market_base.py`，实现 day 账本构建、week/month day-derived 聚合、validator 与 report 输出。
4. 新增 `scripts/data_foundation/build_market_base_day_week_month.py` 与 `scripts/data_foundation/validate_market_base_day_week_month.py`。
5. 先跑 bounded smoke build 到 `H:\Malf-Pas-temp`，确认 SQL 路径、聚合逻辑、validator 和 report 输出正常。
6. 对正式 `raw_market.duckdb` 跑 full build，创建 `H:\Malf-Pas-data\market_base_day.duckdb`、`market_base_week.duckdb`、`market_base_month.duckdb`。
7. 立刻对同一输入再跑第二次 full build，验证 `delete+rebuild` 路径幂等且不膨胀业务事实。
8. 同步 `governance/market_base_day_week_month_registry.toml`、README、docs README、AGENTS、Roadmap 2、conclusion index 与第 22 卡四件套。
9. 复跑 governance / unittest / validator，确认 live next 已切到 `market-meta-tradability-calendar-card`。

## 3. 关键验证

| 验证项 | 结果 |
|---|---|
| bounded smoke build | `passed / 5 symbols / day 4720 / week 998 / month 237` |
| full build | `passed / day 28649022 / week 6071205 / month 1454045` |
| full rerun idempotence | `passed / same-input rerun did not inflate row counts` |
| day analysis line | `analysis_price_line = backward` |
| week/month lineage | `derived_from_timeframe = day`，`source_run_id = market-base-day-week-month-build-card-20260517-01:day` |
| day/week/month natural key | `unique` |
| day/week/month latest pointer | `unique` |
| source manifest binding | `complete` |
| current live write scope | `H:\Malf-Pas-data\market_base_day.duckdb / market_base_week.duckdb / market_base_month.duckdb only` |
| downstream runtime scope | `not opened` |

## 4. 重要说明

- week/month 当前仍是 `day-derived`。这张卡没有打开 direct week/month source，也没有把该结论包装成“以后永远如此”；它只是忠实执行当前 live 治理状态。
- `base_run`、`dirty_scope`、`source_manifest`、`schema_version` 已在三库中形成最小闭环，但第 24-26 卡要负责把 `data_control.run_ledger`、checkpoint/resume、freshness/readout 的系统级闭环补全。
- 第 22 卡完成后，只能说明 `market_base_day/week/month` 已经 development-usable 的基础面成形；Data Foundation 的 `daily_usable` 总体 ready 仍未宣告。

## 5. 后续要求

- 下一张 Data Foundation 卡为 `market-meta-tradability-calendar-card`。
- 第 23 卡只允许建立 `market_meta` 基础事实账本，不得回头改写第 22 卡对 `market_base_day/week/month` 的自然键、lineage 或 live 写入边界。
- 第 24-26 卡继续承担 `data_control`、daily incremental、checkpoint/resume、freshness/audit 的系统闭环，不得被第 22 卡“提前完成”的表述替代。

## 6. 文档更新

- `src/malf_pas/data_foundation/market_base.py`
- `scripts/data_foundation/build_market_base_day_week_month.py`
- `scripts/data_foundation/validate_market_base_day_week_month.py`
- `tests/data_foundation/test_market_base_ledger.py`
- `tests/data_foundation/test_market_base_cli.py`
- `src/malf_pas/governance/checks.py`
- `tests/governance/test_governance_checks.py`
- `pyproject.toml`
- `governance/repo_governance_registry.toml`
- `governance/module_gate_registry.toml`
- `governance/data_foundation_roadmap_registry.toml`
- `governance/market_base_day_week_month_registry.toml`
- `README.md`
- `docs/README.md`
- `AGENTS.md`
- `docs/00-governance/04-root-directory-policy-v1.md`
- `governance/README.md`
- `governance/module_api_contracts/README.md`
- `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
