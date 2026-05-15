# Repo Governance Environment Bootstrap Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `repo-governance-environment-bootstrap-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 从 Asteria 吸收治理环境经验，冻结 Malf-Pas 自己的最小可重建 repo-local 边界。
- 建立 workflow hooks、governance checks、environment config、machine-readable governance skeleton。
- 明确 `.venv`、业务 runner、正式 DB、report/temp artifacts、legacy code 不迁入。

## 3. 允许动作

- 修改治理文档、roadmap、README、AGENTS、结论索引与 execution 四件套。
- 新增 repo-local Python 工具骨架、治理检查脚本、workflow plugin skeleton、`.codex` 说明。
- 新增 `governance/*.toml` 作为机器可读治理占位与检查输入。

## 4. 禁止动作

- 写入任何正式数据库或 scratch DB。
- 迁入 Asteria 或历史 repo 的业务模块 runner、schema、runtime 代码。
- 复制 `.venv`、report、artifact、temp、个人 secret 或旧绝对执行路径。
- 打开 broker、paper-live、回测收益证明或模块 runtime 实现。

## 5. 通过标准

- `plugins`、`scripts`、`environment`、`.codex`、`.gitignore`、`governance` 的迁入 / 不迁入边界冻结。
- repo-local governance check 可运行并通过。
- 第二卡四件套登记进 `docs/04-execution/00-conclusion-index-v1.md`。
