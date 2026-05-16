# MALF v1.4 Immutability Anchor Record

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-v1-4-immutability-anchor-card-20260515-01` |
| result | `passed` |

## 2. 执行顺序

1. 复核 `README.md`、`AGENTS.md`、重构总纲、来源裁决、主线权威图、MALF 锚点、模块所有权、存储裁决、历史大账本协议、每日增量协议、回测窗口协议、root directory policy、roadmap、结论索引和 repo registry。
2. 确认当前 live next 为 `malf-v1-4-immutability-anchor-card`。
3. 将 MALF anchor 文档状态冻结为 `frozen-by-malf-v1-4-immutability-anchor-card-20260515-01`。
4. 明确 MALF v1.4 目录、zip 与 `MANIFEST.json` 的角色边界。
5. 新增 `governance/malf_v1_4_immutability_registry.toml` 并增强 repo-local registry 校验。
6. 更新 roadmap、结论索引、gate registry、repo governance registry 与 AGENTS 当前状态。
7. 建立第九卡 execution 四件套，并将下一卡推进到 `predecessor-strength-map-card`。
8. 运行 repo-local doctor、governance check、unittest 和 exact authority search。

## 3. 关键验证

| 验证 | 结果 |
|---|---|
| authority docs reviewed before edit | `passed` |
| MALF v1.4 anchor document frozen | `passed` |
| anchor directory registered | `passed` |
| anchor zip registered | `passed` |
| anchor MANIFEST registered | `passed` |
| downstream MALF rewrite forbidden | `passed` |
| adapter MALF semantic ownership forbidden | `passed` |
| runtime authorization remains false | `passed` |
| formal DB mutation remains no | `passed` |
| live next advanced to predecessor-strength-map-card | `passed` |
| dev doctor | `passed` |
| project governance check | `passed` |
| governance tests | `passed` |
| formal DB artifact created | `no` |
| runtime implementation created | `no` |
| legacy code migrated | `no` |
| broker or profit proof created | `no` |

## 4. 外部证据资产

| 资产 | 路径 |
|---|---|
| anchor_directory | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4 (current authority anchor)` |
| anchor_manifest | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4\MANIFEST.json (package boundary evidence, not runtime proof)` |
| current_anchor_zip | `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4.zip (authority zip copy; SHA256 05B0C99170AAE5C1ECA36FC5981829CE397E721F93A5095E32586672D23BBFC7)` |
| predecessor_anchor_directory | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4 (read-only predecessor/original reference)` |
| predecessor_anchor_zip | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip (read-only predecessor/original archive)` |
| predecessor_anchor_manifest | `H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4\MANIFEST.json (read-only predecessor/original reference)` |
| backup_snapshot_manifest | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_4-snapshot-20260516-192716.manifest.json` |
| backup_snapshot_zip | `H:\Malf-Pas-backup\MALF_Three_Part_Design_Set_v1_4-snapshot-20260516-192716.zip (SHA256 95C2613FCAA29AB81BD2C5C30A8E7323D22D098357CE210324325BA31F84209B)` |
| report_dir | `not applicable` |
| manifest | `not applicable` |
| validated_asset | `not applicable` |
| formal_db | `not applicable` |
| current_data_root | `H:\Malf-Pas-data (not accessed)` |
| previous_data_root_reference | `H:\Asteria-data (not accessed)` |

## 5. 文档更新

- `AGENTS.md`
- `docs/01-architecture/01-malf-v1-4-anchor-position-v1.md`
- `docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md`
- `docs/04-execution/00-conclusion-index-v1.md`
- `docs/04-execution/records/governance/009-malf-v1-4-immutability-anchor-card-20260515-01.*`
- `governance/README.md`
- `governance/malf_v1_4_immutability_registry.toml`
- `governance/module_gate_registry.toml`
- `governance/repo_governance_registry.toml`
- `pyproject.toml`
- `src/malf_pas/governance/checks.py`
