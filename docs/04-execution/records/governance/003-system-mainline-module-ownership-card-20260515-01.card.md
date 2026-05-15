# System Mainline Module Ownership Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `system-mainline-module-ownership-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `Data Foundation -> System Readout` 的主线模块顺序。
- 冻结每个模块的语义所有权、自建边界和外部 adapter / engine 边界。
- 明确 `Portfolio Plan` 作为独立轻量层保留，不被 `Position` 或 `Trade` 吞并。

## 3. 允许动作

- 修改治理文档、architecture 文档、roadmap、结论索引与 execution 四件套。
- 新增 machine-readable module ownership registry。
- 更新 gate registry 的当前卡与下一卡状态。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 新增 runtime、runner、schema migration、业务模块实现或 legacy code migration。
- 打开 broker、paper-live、实盘、收益证明或成交回路。
- 让外部 provider、开源项目或历史 repo 拥有本系统语义定义权。

## 5. 通过标准

- Data -> System 模块顺序冻结。
- 每个模块的语义 owner、自建边界、外部边界冻结。
- `Portfolio Plan` 保留 / 轻量化边界冻结。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
