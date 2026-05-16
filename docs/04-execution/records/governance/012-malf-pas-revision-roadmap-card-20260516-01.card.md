# MALF+PAS Revision Roadmap Card

日期：2026-05-16

## 1. 卡信息

| 项 | 值 |
|---|---|
| route | `governance` |
| run_id | `malf-pas-revision-roadmap-card-20260516-01` |
| card type | `governance` |

## 2. 本次目标

- 把原 live next `open-source-adapter-boundary-card` 后移到第 16 卡。
- 新增第 13、14、15 卡：MALF v1.5、PAS v1.2、MALF+PAS scenario atlas。
- 固定修订路线：改 MALF 输出结构行为事实，不放松 PAS 只读 MALF 输出的边界。
- 将 live next 推进到 `malf-v1-5-wave-behavior-snapshot-card`。

## 3. 允许动作

- 修订 roadmap、README、docs README、AGENTS 和相关 authority docs。
- 新增 `governance/malf_pas_revision_roadmap_registry.toml`。
- 将该 registry 纳入 `pyproject.toml` required registries 和 repo-local governance check。
- 更新 repo registry、module gate registry 与 conclusion index。
- 建立第 12 卡 execution 四件套。

## 4. 禁止动作

- 不创建 MALF v1.5、PAS v1.2 或 scenario atlas 正文目录。
- 不修改 `H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4`。
- 不修改 `H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1`。
- 不读取或写入正式 DB。
- 不创建 runtime、schema、runner、broker、仓位、订单、成交或收益证明。

## 5. 通过标准

- roadmap 从 12 张卡修订为 16 张卡。
- 第 12 卡状态为 `passed`，第 13 卡为当前 live next。
- 第 13、14、15、16 卡目标和通过标准写入 roadmap。
- 新 registry 能被 repo-local governance check 校验。
- conclusion index 与 module gate / repo registry 同步。
- repo-local doctor、governance check、unittest 与 exact search 通过。
