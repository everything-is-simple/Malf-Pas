# Malf-Pas

**Malf-Pas** 是一个以 `MALF v1.4` 为当前结构锚点、以 `PAS` 为机会解释层、以 `Signal` 为候选裁决层的新一代治理先行研究系统。

内部核心分工：

```text
MALF = structure fact owner
PAS = opportunity interpreter
Signal = candidate decision ledger
```

远端仓库：

```text
https://github.com/everything-is-simple/Malf-Pas
```

## 关键路径

| 路径 | 职责 |
|---|---|
| `H:\Malf-Pas` | 新系统代码、文档、治理入口 |
| `H:\Malf-Pas-data` | Malf-Pas 重构后当前系统本地数据库根目录；后续历史大账本与子库落点，但当前阶段不得正式写入 |
| `H:\Malf-Pas-backup` | 当前系统备份包、交付 zip、可恢复快照落点；不放历史经验或 scratch |
| `H:\Malf-Pas-Validated` | 当前系统沉淀后的历史经验、权威材料与经验索引；不放备份包或运行产物 |
| `H:\Malf-Pas-reprot` | 当前系统 report、audit readout、运行报告输出根；目录名按当前环境固定为 `reprot` |
| `H:\Malf-Pas-temp` | 当前系统临时产物、cache、smoke-run scratch；不得 promote 为正式事实 |
| `H:\Asteria` | 上一版代码与治理范式参考；只读，不是本仓库运行面 |
| `H:\Asteria-data` | 上一版 Asteria 数据根；只读参考与 lineage 经验输入，不是 Malf-Pas 当前系统数据落点，也不得作为 scratch |
| `H:\Asteria-Validated` | 上一版混合 validated / 历史经验 / 备份包输入；只读参考，不是当前备份根 |
| `H:\Asteria-report` | 上一版报告根；只读参考，不复用为当前 report 根 |
| `H:\Asteria-temp` | 上一版临时根；只读参考，不复用为当前 scratch |
| `G:\malf-history` | 曾经做过但未完成的历史版本根；只读参考各版本、各模块为何这样实现，以及当时的权衡折衷 |
| `G:\《股市浮沉二十载》` | 书籍参考与思路风暴来源根；只读概念来源，不是 runtime、数据根或交易指令来源 |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | PAS 概念、公理与状态机来源锚点，尤其用于 context、trigger、strength、lifecycle 与业务边界 |

repo 根目录保持干净：不得新增临时 DB、缓存、report artifacts 或 scratch 目录。

## 当前原则

1. 先有权威设计，再有实现。
2. 第一张路线图只做治理卡，不做 runtime、正式 DB、回测实现或 broker 适配。
3. `MALF v1.4` 是长期 authority anchor，不因 PAS 重构而漂移。
4. `PAS` 只解释机会与候选生命周期，不输出仓位、订单、成交。
5. `Signal` 只聚合 PAS 候选并裁决接受或拒绝。
6. `G:\《股市浮沉二十载》` 是 PAS 思路风暴与概念来源，`G:\malf-history` 是旧版本工程取舍来源；二者都只读参考，不拥有本系统语义定义权。

## 当前权威资产

首轮治理阶段明确只读消费以下权威输入：

```text
H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_4
H:\Malf-Pas-Validated\MALF_Three_Part_Design_Set_v1_5
H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_1
H:\Malf-Pas-Validated\PAS__Three_Part_Design_Set_v1_2
H:\Malf-Pas-Validated\MALF_PAS_Scenario_Atlas_v1_0
H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4 (predecessor/original reference)
H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip (predecessor/original archive)
H:\Asteria-Validated\Asteria_System_Design_Set_v1_0
H:\Asteria-Validated\MALF-system-history
H:\Asteria-Validated\MALF-reference
G:\malf-history
G:\《股市浮沉二十载》
G:\《股市浮沉二十载》\2020.(Au)LanceBeggs
```

当前裁决：

```text
MALF v1.4 is the current predecessor authority anchor.
PAS v1.1 design set is the current predecessor PAS authority.
MALF v1.5 design set is frozen as successor authority for wave_behavior_snapshot.
PAS v1.2 is frozen as successor authority for strength_weakness_matrix.
MALF_PAS_Scenario_Atlas_v1_0 is frozen as a companion atlas for sandbox charts and case analysis.
No formal DB mutation is authorized.
No broker or live-trading discussion is opened by this repo initialization.
Current live next is open-source-adapter-boundary-card.
```

## 阅读入口

1. [Agent 规则](AGENTS.md)
2. [文档入口](docs/README.md)
3. [重构总纲](docs/00-governance/00-malf-pas-reconstruction-charter-v1.md)
4. [来源裁决与非迁移规则](docs/00-governance/01-source-authority-and-non-migration-rule-v1.md)
5. [执行记录协议](docs/00-governance/02-execution-record-protocol-v1.md)
6. [repo 治理环境 bootstrap](docs/00-governance/03-repo-governance-environment-bootstrap-v1.md)
7. [根目录钢铁规则](docs/00-governance/04-root-directory-policy-v1.md)
8. [主线权威图](docs/01-architecture/00-mainline-authoritative-map-v1.md)
9. [MALF v1.4 锚点位置](docs/01-architecture/01-malf-v1-4-anchor-position-v1.md)
10. [旧系统强项地图](docs/01-architecture/02-predecessor-strength-map-v1.md)
11. [系统主线模块所有权](docs/01-architecture/03-system-mainline-module-ownership-v1.md)
12. [存储引擎与便携性裁决](docs/01-architecture/04-storage-engine-and-portability-decision-v1.md)
13. [历史大账本拓扑协议](docs/01-architecture/05-historical-ledger-topology-protocol-v1.md)
14. [每日增量与断点续传协议](docs/01-architecture/06-daily-incremental-and-resume-protocol-v1.md)
15. [回测窗口与留出样本协议](docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md)
16. [模块设计文档标准](docs/02-modules/00-module-design-document-standard-v1.md)
17. [PAS 公理化状态机](docs/02-modules/01-pas-axiomatic-state-machine-v1.md)
18. [MALF v1.5 wave behavior snapshot](docs/02-modules/02-malf-v1-5-wave-behavior-snapshot-v1.md)
19. [PAS v1.2 strength weakness matrix](docs/02-modules/03-pas-v1-2-strength-weakness-matrix-v1.md)
20. [MALF+PAS scenario atlas](docs/02-modules/04-malf-pas-scenario-atlas-v1.md)
21. [首张治理路线图](docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md)
22. [执行区入口](docs/04-execution/README.md)

## Python 环境

首选 repo-local virtualenv：

```powershell
python -m venv H:\Malf-Pas\.venv
H:\Malf-Pas\.venv\Scripts\python.exe -m pip install --upgrade pip
H:\Malf-Pas\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

可选 conda fallback：

```powershell
conda env create -f environment.yml
```

说明：

```text
H:\Asteria\.venv is reference-only
H:\Malf-Pas\.venv must be recreated locally
.venv itself must stay out of git
```

## 开发检查

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```
