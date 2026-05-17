# Data Module DB Contract Record

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `data-module-db-contract-card-20260517-01` |
| result | `passed` |

## 2. 执行顺序

1. 读取 repo authority docs、Roadmap 2、execution protocol、conclusion index 与相关 registry。
2. 先写红灯测试，要求第 20 卡必须具备 Data contract module、contract registry、governance registry check 与四件套。
3. 新增 `governance/data_module_db_contract_registry.toml`，冻结六库、表族、自然键、治理键、lineage 与 validator 边界。
4. 新增 `src/malf_pas/data_foundation/contract.py` 与 validator CLI，默认只读 registry，不写正式 DB。
5. 接入 `src/malf_pas/governance/checks.py`、`pyproject.toml` 与 `governance/repo_governance_registry.toml`。
6. 同步 `governance/data_foundation_roadmap_registry.toml`，将下一卡推进到 `raw-market-full-build-ledger-card`。
7. 同步 README、docs README、AGENTS、governance README、Roadmap 2 与 conclusion index。
8. 建立第 20 卡四件套。

## 3. 关键验证

| 验证项 | 结果 |
|---|---|
| 第 20 卡红灯测试 | `failed as expected before implementation` |
| Data contract validator | `passed / 6 databases / 38 table families` |
| run_id natural key guard | `bar 类业务事实自然键禁止 run_id` |
| data_control family boundary | `orchestration 与 freshness/readout 分离` |
| forbidden downstream semantics guard | `MALF / PAS / Signal / broker / order / profit 字段禁止进入 Data contract` |
| current card creates DB | `false` |
| current card writes data root | `false` |

## 4. 后续要求

- 下一张 Data Foundation 卡为 `raw-market-full-build-ledger-card`。
- 第 21 卡只能在 Data Foundation 范围内建立 `raw_market` 文件级历史账本，不得打开下游 MALF / PAS / Signal runtime。
- 第 20 卡不宣告 Data Foundation ready；ready 仍必须等第 27 卡同时证明 `development_usable = true` 与 `daily_usable = true`。

## 5. 文档更新

- `governance/data_module_db_contract_registry.toml`
- `src/malf_pas/data_foundation/contract.py`
- `scripts/data_foundation/validate_data_contract.py`
- `tests/data_foundation/test_data_contract.py`
- `tests/governance/test_governance_checks.py`
- `src/malf_pas/governance/checks.py`
- `pyproject.toml`
- `governance/repo_governance_registry.toml`
- `governance/data_foundation_roadmap_registry.toml`
- `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
- `README.md`
- `docs/README.md`
- `AGENTS.md`
- `governance/README.md`
