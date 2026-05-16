# Open-Source Adapter Boundary Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `open-source-adapter-boundary-card-20260516-01` |
| card type | `governance terminal closeout` |

## 2. 本次目标

- 新建 `docs/01-architecture/08-open-source-adapter-boundary-v1.md`。
- 新建 `governance/open_source_adapter_boundary_registry.toml`。
- 逐项冻结 `DuckDB / Arrow / Polars`、`vectorbt / backtesting.py`、`Qlib`、`baostock`、`AKShare` 的 adapter 角色与禁止越界边界。
- 把首张治理 roadmap 收口到 `none / terminal`。
- 建立第 16 卡 execution 四件套并登记进结论索引。

## 3. 允许动作

- 新增 adapter boundary authority doc 与 machine-readable registry。
- 更新 README、docs README、AGENTS、roadmap、conclusion index、module gate、repo registry 与 repo-local governance check。
- 将首张治理 roadmap 的 live next 改为 `current_allowed_next_card = ""`。

## 4. 禁止动作

- 不回写历史 execution records。
- 不改写历史 frozen registries 的原始结论。
- 不打开 runtime、formal DB mutation、broker、order、position、fill 或 profit claim。
- 不迁移 legacy code、schema、runner 或旧 DuckDB 表面。
- 不新增 `*.duckdb`、`*.db`、`*.sqlite` 变更。

## 5. 通过标准

- `08-open-source-adapter-boundary-v1.md` 形成统一角色法、逐项项目表、禁止越界与 terminal closeout 口径。
- `governance/open_source_adapter_boundary_registry.toml` 建立并纳入 governance checks。
- `governance/module_gate_registry.toml` 与 `governance/repo_governance_registry.toml` 的 `current_allowed_next_card` 变为 `""`。
- roadmap 第 16 卡、结论索引和 live doc surface 已同步为 terminal 口径。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套。
- repo-local doctor、governance check 与 unittest 通过。
