# Daily Incremental And Resume Protocol Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `daily-incremental-and-resume-protocol-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `Malf-Pas` 第一阶段每日增量协议。
- 冻结 dirty scope、checkpoint、resume mode 与 staging promote 的治理边界。
- 明确第 6 卡只定义协议，不执行正式 DB mutation、schema migration 或 runtime build。

## 3. 允许动作

- 修改治理文档、architecture 文档、roadmap、结论索引与 execution 四件套。
- 新增 machine-readable daily incremental protocol registry。
- 更新 gate registry 的当前卡与下一卡状态。
- 保持 `H:\Malf-Pas-data` 为当前系统未来数据根，但当前不写入。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 读取或改写 `H:\Malf-Pas-data`、`H:\Asteria-data` 中的正式数据资产。
- 新增 runtime、runner、schema migration、业务模块实现或 legacy code migration。
- 打开 broker、paper-live、实盘、收益证明或成交回路。
- 把 staging promote 写成当前可执行的正式 promote 权限。

## 5. 通过标准

- 每日增量、dirty scope、checkpoint、resume 与 staging promote 规则冻结。
- 第 6 卡 protocol 文档与 machine-readable registry 建立。
- roadmap、docs entry、governance README、pyproject、repo registry、gate registry 与结论索引同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local 治理检查与 unittest 通过。
