# Raw Market Full Build Ledger Record

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `raw-market-full-build-ledger-card-20260517-01` |
| result | `passed` |

## 2. 执行顺序

1. 读取 live authority docs、Roadmap 2、conclusion index、repo governance registry 与 Data contract registry。
2. 先写第 21 卡红灯测试，要求 raw-market runtime、build/validator CLI、closeout registry 与四件套必须存在。
3. 新增 `src/malf_pas/data_foundation/raw_market.py`，实现 source discovery、TDX `*.day` parser、DuckDB schema writer、canonical root selection、reject/skipped 审计与 resume guard。
4. 新增 `scripts/data_foundation/build_raw_market_full_ledger.py` 与 `scripts/data_foundation/validate_raw_market_ledger.py`，并补 `duckdb` 依赖。
5. 先跑 bounded smoke build，确认正式 roots、schema、validator 和 report 输出路径正常。
6. 对 `H:\tdx_offline_Data` 与 `H:\new_tdx64` 跑 full build，创建 `H:\Malf-Pas-data\raw_market.duckdb`。
7. 立刻对同一输入再跑 `daily_incremental`，验证 `skipped_unchanged`、幂等重跑与 no-op audited closeout。
8. 同步 `governance/raw_market_full_build_registry.toml`、README、docs README、AGENTS、Roadmap 2、conclusion index 与第 21 卡四件套。
9. 跑 `doctor / governance / unittest / validator` 完成 repo-local closeout。

## 3. 关键验证

| 验证项 | 结果 |
|---|---|
| bounded smoke build | `passed / 5 canonical files / 4720 raw bars` |
| full build | `passed / 30556 discovered source files / 28649022 raw bars / 144743 dual_root_divergence audits` |
| daily incremental rerun | `passed / skipped_unchanged = 12196 / no duplicate business facts` |
| raw_bar natural key | `unique` |
| source manifest binding | `complete` |
| ingest_run audit boundary | `source ingest local audit only; not data_control.run_ledger` |
| current live write scope | `H:\Malf-Pas-data\raw_market.duckdb only` |
| downstream runtime scope | `not opened` |

## 4. 重要说明

- `source_file` 当前 ledger row count 是 `30558`，而 full build summary 的 discovered file count 是 `30556`。差异来自 secondary root 中有 `2` 个文件在 full build 和 daily incremental 之间发生了 revision rollover，因此以新 revision 追加进 `source_file` ledger，但没有造成 `raw_bar` 业务事实重复。
- 当前 `ingest_run` 表保留最新一轮 `daily_incremental` 审计状态；full build 的 manifest/hash 和 summary 已通过 report 文件与 closeout registry 留痕。
- 本卡只建立 `raw_market` 文件级历史账本，不宣告 `market_base_*`、`market_meta`、`data_control` 或整个 Data Foundation 已 ready。

## 5. 后续要求

- 下一张 Data Foundation 卡为 `market-base-day-week-month-build-card`。
- 第 22 卡只允许建立 `market_base_day/week/month` 物化账本，不得把 `tradability` 或 `data_control` 提前并入。
- `development_usable = true` 与 `daily_usable = true` 的整体 ready 结论仍要等第 27 卡统一关闭。

## 6. 文档更新

- `src/malf_pas/data_foundation/raw_market.py`
- `src/malf_pas/data_foundation/__init__.py`
- `scripts/data_foundation/build_raw_market_full_ledger.py`
- `scripts/data_foundation/validate_raw_market_ledger.py`
- `tests/data_foundation/test_raw_market_ledger.py`
- `tests/data_foundation/test_raw_market_cli.py`
- `src/malf_pas/governance/checks.py`
- `tests/governance/test_governance_checks.py`
- `scripts/dev/doctor.py`
- `pyproject.toml`
- `governance/repo_governance_registry.toml`
- `governance/module_gate_registry.toml`
- `governance/data_foundation_roadmap_registry.toml`
- `governance/raw_market_full_build_registry.toml`
- `README.md`
- `docs/README.md`
- `AGENTS.md`
- `docs/00-governance/04-root-directory-policy-v1.md`
- `governance/README.md`
- `governance/module_api_contracts/README.md`
- `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
