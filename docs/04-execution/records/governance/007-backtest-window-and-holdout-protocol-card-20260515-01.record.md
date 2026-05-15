# Backtest Window And Holdout Protocol Record

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `backtest-window-and-holdout-protocol-card-20260515-01` |
| result | `passed` |

## 2. 执行顺序

1. 复核 `README.md`、`AGENTS.md`、重构总纲、来源裁决、主线权威图、MALF 锚点、模块所有权、存储裁决、历史大账本协议、每日增量协议、roadmap、结论索引和 repo registry。
2. 确认当前 live next 为 `backtest-window-and-holdout-protocol-card`。
3. 新增 backtest window and holdout protocol 文档，冻结 `2012..2021`、三年滚动段、reserved holdout 和 `2021` 用途隔离规则。
4. 新增 machine-readable backtest window holdout registry。
5. 更新 roadmap、docs entry、governance README、pyproject、repo registry、gate registry 和结论索引。
6. 建立第七卡 execution 四件套，并将下一卡推进到 `source-authority-and-non-migration-rule-card`。
7. 运行 repo-local doctor、governance check、unittest 和 exact authority search。

## 3. 关键验证

| 验证 | 结果 |
|---|---|
| authority docs reviewed before edit | `passed` |
| historical_coverage_window frozen | `passed` |
| selection_window frozen | `passed` |
| reserved_holdout_segments frozen | `passed` |
| year_2021_boundary purpose-isolated | `passed` |
| no_holdout_leakage protocol frozen | `passed` |
| live next advanced to source-authority-and-non-migration-rule-card | `passed` |
| dev doctor | `passed` |
| project governance check | `passed` |
| governance tests | `passed` |
| formal DB artifact created | `no` |
| runtime implementation created | `no` |
| backtest executed | `no` |
| profit proof created | `no` |

## 4. 外部证据资产

| 资产 | 路径 |
|---|---|
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |

## 5. 文档更新

- `README.md`
- `AGENTS.md`
- `docs/README.md`
- `docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md`
- `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
- `docs/04-execution/records/governance/007-backtest-window-and-holdout-protocol-card-20260515-01.*`
- `governance/README.md`
- `governance/backtest_window_holdout_registry.toml`
- `governance/module_gate_registry.toml`
- `governance/repo_governance_registry.toml`
- `pyproject.toml`
