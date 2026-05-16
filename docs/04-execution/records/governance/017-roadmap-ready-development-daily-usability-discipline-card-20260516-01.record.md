# Roadmap Ready Development Daily Usability Discipline Record

日期：2026-05-16

## 1. 执行摘要

本次执行把后续模块 roadmap 的 `ready` 标准从“能支撑后续开发”升级为
`development_usable + daily_usable` 双重门禁。该纪律适用于 Data Foundation 以及之后所有
MALF、PAS、Signal 等模块 roadmap，不是 Data 的临时规则。

## 2. 执行步骤

1. 复核 repo 当前 terminal 状态、post-terminal roadmap discipline 文档、历史大账本协议与每日增量协议。
2. 在 governance check 单测中先加入负向场景，确认缺少两条新纪律时应失败。
3. 增强 `src/malf_pas/governance/checks.py`，要求 registry 与 repo hard rules 同步包含两条新纪律。
4. 更新 post-terminal discipline registry，将纪律总数从 `10` 固定为 `12`。
5. 更新 AGENTS、README、docs README、governance README 与 reconstruction charter，使所有 agent 起草、执行、验收后续 roadmap 时必须检查两个 ready 维度。
6. 建立第 17 号 execution 四件套并登记进结论索引。

## 3. 关键验证

| 验证项 | 结果 |
|---|---|
| 缺少两条 ready 纪律的负向单测 | `passed` |
| post-terminal discipline registry 纪律总数 | `12` |
| repo hard_rules 含 development usable | `yes` |
| repo hard_rules 含 daily usable | `yes` |
| `python scripts\dev\doctor.py` | `exit 0` |
| `python scripts\governance\check_project_governance.py` | `passed` |
| `python -m unittest discover -s tests -p "test_*.py"` | `Ran 7 tests ... OK` |
| `python -m ruff check src tests scripts` | `All checks passed!` |
| formal DB mutation | `not changed / no` |
| live next | `not reopened / none / terminal` |

## 4. 后续要求

- 下一张 Data Foundation roadmap 必须同时写出 `development_usable` 与 `daily_usable` 通过标准。
- 任何后续模块如果声称天然不需要 daily incremental，必须在 roadmap 中写明理由与替代日常维护机制。
- 只满足 contract/schema/manifest/lineage 的模块，不得再被称为 `ready`。
