# Local TDX Source Inventory Card

日期：2026-05-17

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `data-foundation` |
| run_id | `local-tdx-source-inventory-card-20260517-01` |
| roadmap_order | `019` |
| card type | `read-only source inventory / previous Data baseline reference` |

## 2. 本次目标

- 只读盘点 `H:\tdx_offline_Data` 与 `H:\new_tdx64`。
- 只读打开上一版 `H:\Asteria-data` 中 Data 五库作为对照基线。
- 冻结 source family、file family、fingerprint policy、week/month 来源结论与 tradability 来源结论。
- 明确 `H:\Asteria-data` 只能是 `reference_baseline_only`，不得成为当前 truth owner。

## 3. 允许动作

- 新增只读盘点工具和对应测试。
- 新增 `governance/local_tdx_source_inventory_registry.toml`。
- 同步 `governance/data_foundation_roadmap_registry.toml`、repo registry、pyproject registry 清单、Roadmap 2 与 conclusion index。
- 建立第 19 卡四件套。

## 4. 禁止动作

- 不写入 `H:\Malf-Pas-data`。
- 不修改 `H:\tdx_offline_Data`、`H:\new_tdx64` 或 `H:\Asteria-data`。
- 不把 `H:\Asteria-data` 升级为当前系统 truth owner、output root、scratch、schema migration source 或 runner migration source。
- 不用 `TuShare / baostock / AKShare` 补正式 truth。
- 不打开 MALF / PAS / Signal / Position / Trade / Pipeline runtime。

## 5. 通过标准

- `current_truth_roots = H:\tdx_offline_Data + H:\new_tdx64`。
- `previous_reference_root = H:\Asteria-data / reference_baseline_only`。
- week/month 结论写为 `day-derived`，并登记 direct parent 与 rule version。
- tradability 结论写为 `blocked`，并登记 gap。
- 上一版 Data 五库只读对照结果登记完成。
- repo-local doctor、governance check、unittest 与 Ruff 通过。
