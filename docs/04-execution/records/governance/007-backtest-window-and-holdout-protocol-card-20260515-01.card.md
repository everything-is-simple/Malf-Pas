# Backtest Window And Holdout Protocol Card

日期：2026-05-15

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `backtest-window-and-holdout-protocol-card-20260515-01` |
| card type | `governance` |

## 2. 本次目标

- 冻结 `Malf-Pas` 第一阶段回测窗口与留出样本协议。
- 冻结 `2012..2021` 历史覆盖口径、三年滚动段、`2021..2023` 与 `2024..2026` reserved holdout 边界。
- 明确 `2021` 用途隔离：可作为历史覆盖口径末年，但不得参与选择、调参或策略筛选。

## 3. 允许动作

- 修改治理文档、architecture 文档、roadmap、结论索引与 execution 四件套。
- 新增 machine-readable backtest window and holdout registry。
- 更新 gate registry 的当前卡与下一卡状态。
- 保持 `H:\Malf-Pas-data` 为当前系统未来数据根，但当前不写入。

## 4. 禁止动作

- 写入任何 `*.duckdb`、`*.db`、`*.sqlite` 或正式数据根目录。
- 读取或改写 `H:\Malf-Pas-data`、`H:\Asteria-data` 中的正式数据资产。
- 运行回测、生成收益 proof、输出 broker readiness 或 paper-live 结论。
- 新增 runtime、runner、schema migration、业务模块实现或 legacy code migration。
- 把 2021 同时用于选择窗口和 reserved holdout。

## 5. 通过标准

- 回测窗口、三年滚动段、reserved holdout 与 `2021` 用途隔离裁决冻结。
- 第 7 卡 protocol 文档与 machine-readable registry 建立。
- roadmap、docs entry、governance README、pyproject、repo registry、gate registry 与结论索引同步。
- repo 内形成 `card / evidence-index / record / conclusion` 四件套并登记进结论索引。
- repo-local 治理检查与 unittest 通过。
