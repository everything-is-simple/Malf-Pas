# Malf-Pas Root Directory Policy v1

日期：2026-05-15

状态：active / root-directory-policy

## 1. 目标

本文件冻结 `Malf-Pas` 重构系统的六根目录规则。

上一版 `Asteria` 同时把历史经验、validated delivery、备份包、report 和 temp 产物混在多个旧目录里。
`Malf-Pas` 从本阶段开始必须把这些职责拆开，避免当前系统数据根、历史经验、备份包和运行产物互相污染。

## 2. Malf-Pas 六根目录

| root_key | 路径 | 职责 | 当前阶段规则 |
|---|---|---|---|
| `repo_root` | `H:\Malf-Pas` | 新系统代码、文档、治理入口 | repo 根目录不得落缓存、临时 DB、report artifacts 或 scratch |
| `data_root` | `H:\Malf-Pas-data` | 当前系统本地数据库根目录；后续历史大账本与子库落点 | 当前 `formal DB mutation = no`，不得正式写入 |
| `backup_root` | `H:\Malf-Pas-backup` | 备份包、交付 zip、可恢复快照 | 不承载历史经验定义，不作 scratch |
| `validated_root` | `H:\Malf-Pas-Validated` | 本系统沉淀后的历史经验、权威材料、经验索引 | 不承载备份包，不承载运行产物 |
| `report_root` | `H:\Malf-Pas-reprot` | report、audit readout、运行报告输出根 | 目录名按当前环境固定为 `reprot`；不得写入 repo 根 |
| `temp_root` | `H:\Malf-Pas-temp` | 临时产物、cache、smoke-run scratch | 不得 promote 为正式事实，不得进入 repo |

## 3. 上一版目录边界

上一版目录只能作为只读参考或历史来源，不得成为 `Malf-Pas` 当前系统根目录。

| previous_root | 当前角色 |
|---|---|
| `H:\Asteria` | 上一版代码与治理范式参考 |
| `H:\Asteria-data` | 上一版数据根；只读参考与 lineage 经验输入 |
| `H:\Asteria-Validated` | 上一版混合 validated / 历史经验 / 备份包输入；只读参考 |
| `H:\Asteria-report` | 上一版报告根；只读参考 |
| `H:\Asteria-temp` | 上一版临时根；只读参考，不复用 |

## 4. 硬规则

1. `H:\Malf-Pas-data` 是当前系统唯一数据根，但当前阶段不得正式写入。
2. `H:\Malf-Pas-backup` 只放备份包和可恢复快照。
3. `H:\Malf-Pas-Validated` 只放本系统沉淀后的历史经验与权威材料。
4. `H:\Malf-Pas-reprot` 只放报告与 audit readout。
5. `H:\Malf-Pas-temp` 只放临时产物和 cache。
6. 上一版 `H:\Asteria-*` 目录只能只读参考，不得作为当前系统 output root 或 scratch。
7. 任何新脚本、hook、registry 或 card 如需要根目录，必须引用本文件与
   `governance/root_directory_registry.toml`。

## 5. 外部参考根

以下 `G:` 路径不是 `Malf-Pas` 六根目录的一部分，也不得作为 output root 或 scratch。
它们只提供思想来源、历史版本经验与实现取舍参考。

| reference_root | 当前角色 | 禁止解释 |
|---|---|---|
| `G:\《股市浮沉二十载》` | 书籍参考与思路风暴来源根 | 不得作为 runtime、正式数据根、broker 指令或收益承诺来源 |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | PAS context、trigger、strength、lifecycle 与业务边界概念锚点 | 不得复制正文或把交易管理动作直接变成 PAS 输出动作 |
| `G:\malf-history` | 曾经做过但未完成的历史版本根；用于理解各模块实现理由、权衡折衷、样本和失败教训 | 不得迁移旧 schema、runner、DuckDB 表面或旧代码 |
