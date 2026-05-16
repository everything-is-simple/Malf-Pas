# Roadmap Ready Development Daily Usability Discipline Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `roadmap-ready-development-daily-usability-discipline-card-20260516-01` |
| card type | `post-terminal governance discipline update` |

## 2. 本次目标

- 将后续模块 roadmap 的 `ready` 标准升级为 `development_usable + daily_usable` 双重门禁。
- 把 `ROADMAP-READY-REQUIRES-DEVELOPMENT-USABLE` 与 `ROADMAP-READY-REQUIRES-DAILY-USABLE` 写入文档、registry、AGENTS 和 repo-local governance check。
- 确认缺少这两条纪律时，`python scripts\governance\check_project_governance.py` 必须失败。
- 建立本次治理纪律修正的 repo-local execution 四件套。

## 3. 允许动作

- 修改 post-terminal roadmap discipline 文档与机器可读 registry。
- 修改 repo governance registry、AGENTS、README、docs README 与 governance README。
- 增强 `src/malf_pas/governance/checks.py` 与对应单测。
- 更新结论索引并新增第 17 号 execution 四件套。

## 4. 禁止动作

- 不重开首张治理 roadmap 的 `none / terminal` 状态。
- 不启动 Data Foundation、MALF、PAS、Signal 或任何业务模块施工。
- 不写入正式 DB、cache、report、scratch 或 runtime 产物。
- 不引入 broker、paper-live、实盘、订单、仓位、成交、alpha 或收益证明口径。
- 不迁移历史 repo schema、runner 或 legacy code。

## 5. 通过标准

- post-terminal roadmap discipline 的纪律总数从 `10` 固定为 `12`。
- registry 同时要求 `development_usable_required_before_next_roadmap = true` 与 `daily_usable_required_before_next_roadmap = true`。
- repo governance `hard_rules` 包含两条 roadmap-ready usability 纪律。
- governance check 对缺失两条纪律的 registry 会产生 finding。
- repo-local doctor、governance check 与 unittest 通过。
