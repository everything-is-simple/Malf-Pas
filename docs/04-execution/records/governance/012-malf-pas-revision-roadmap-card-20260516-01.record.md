# MALF+PAS Revision Roadmap Record

日期：2026-05-16

## 1. 执行摘要

第 12 卡只执行路线修订，不执行 MALF/PAS 正文改版。

## 2. 执行动作

1. 复核 repo authority set、roadmap、conclusion index、registries 与第 11 卡四件套。
2. 将 roadmap 从 12 张卡扩展为 16 张卡。
3. 将原 `open-source-adapter-boundary-card` 从第 12 卡后移到第 16 卡。
4. 新增第 13 卡 `malf-v1-5-wave-behavior-snapshot-card`。
5. 新增第 14 卡 `pas-v1-2-strength-weakness-matrix-card`。
6. 新增第 15 卡 `malf-pas-scenario-atlas-card`。
7. 新增 `governance/malf_pas_revision_roadmap_registry.toml` 并纳入 governance check。
8. 同步 README、docs README、AGENTS、source authority、MALF anchor、PAS authority、module gate、repo registry 与 conclusion index。
9. 建立第 12 卡 execution 四件套。

## 3. 关键裁决

| 项 | 裁决 |
|---|---|
| 修订方式 | 改 MALF successor design set，不放松 PAS 只读 MALF 输出边界 |
| MALF v1.4 | 保留为 predecessor authority，不改写原目录 |
| PAS v1.1 | 保留为 predecessor authority，不改写原目录 |
| MALF v1.5 | 计划新建，发布 `wave_behavior_snapshot` |
| PAS v1.2 | 计划新建，发布 `strength_weakness_matrix` |
| scenario atlas | 计划新建，用于沙盘模拟与图解 |
| alpha | 只登记为后续可验证假设，不在本卡证明 |
| live next | `malf-v1-5-wave-behavior-snapshot-card` |

## 4. 验证

本卡收口已通过：

| command | result |
|---|---|
| `python scripts\dev\doctor.py` | `passed` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `passed` |
| `python -m ruff check src scripts tests` | `passed` |
| exact authority search | `passed` |

并追加 exact search 覆盖新版本目录名、`wave_behavior_snapshot`、`strength_weakness_matrix`、
`malf-pas-scenario-atlas-card` 和 `open-source-adapter-boundary-card`。
