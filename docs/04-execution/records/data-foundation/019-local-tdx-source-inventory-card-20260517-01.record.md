# Local TDX Source Inventory Record

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `local-tdx-source-inventory-card-20260517-01` |
| result | `passed` |

## 2. 执行顺序

1. 读取 repo authority docs、Roadmap 2、execution protocol、conclusion index 与相关 registry。
2. 先写红灯测试，要求第 19 卡必须登记上一版 `H:\Asteria-data` 只读参考、五个上一版 Data DB、week/month 与 tradability 结论。
3. 新增只读盘点模块与 CLI，默认 JSON 输出到 stdout，不写 `H:\Malf-Pas-data`。
4. 使用 `read_only=True` 打开上一版 Asteria Data 五库并登记表族与 row count。
5. 新增 `governance/local_tdx_source_inventory_registry.toml` 并接入 repo-local governance checks。
6. 同步 Roadmap 2、Data Foundation roadmap registry、repo registry、pyproject registry 清单和 conclusion index。
7. 建立第 19 卡四件套。

## 3. 关键验证

| 验证 | 结果 |
|---|---|
| 当前 truth roots | `H:\tdx_offline_Data` + `H:\new_tdx64` |
| 上一版参考根 | `H:\Asteria-data / reference_baseline_only` |
| 上一版 Data 五库 | `present` |
| week/month direct source | `not proven / day-derived` |
| tradability source | `blocked` |
| current card creates DB | `false` |
| current card writes data root | `false` |

## 4. 外部证据资产

| 资产 | 路径 |
|---|---|
| report_dir | `not applicable` |
| manifest | `governance/local_tdx_source_inventory_registry.toml` |
| validated_asset | `not applicable` |

## 5. 文档更新

- `docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
- `docs/04-execution/records/data-foundation/019-local-tdx-source-inventory-card-20260517-01.*.md`
