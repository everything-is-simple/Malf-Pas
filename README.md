# Malf-Pas

**Malf-Pas** 是一个以 `MALF v1.4` 为结构锚点、以 `PAS` 为机会解释层、以 `Signal` 为候选裁决层的新一代治理先行研究系统。

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
| `H:\Malf-Pas-data` | 本地数据库根目录；后续历史大账本与子库落点，但当前阶段不得正式写入 |
| `H:\Asteria-Validated` | 已验证设计、MALF v1.4 权威资产、历史 formal 归档 |
| `H:\Asteria` | 治理范式与文档结构参考，不是本仓库运行面 |
| `G:\malf-history` | 历史系统经验与模块强项参考输入 |
| `G:\《股市浮沉二十载》\2020.(Au)LanceBeggs` | PAS 概念、公理与状态机来源锚点 |

repo 根目录保持干净：不得新增临时 DB、缓存、report artifacts 或 scratch 目录。

## 当前原则

1. 先有权威设计，再有实现。
2. 第一张路线图只做治理卡，不做 runtime、正式 DB、回测实现或 broker 适配。
3. `MALF v1.4` 是长期 authority anchor，不因 PAS 重构而漂移。
4. `PAS` 只解释机会与候选生命周期，不输出仓位、订单、成交。
5. `Signal` 只聚合 PAS 候选并裁决接受或拒绝。
6. 历史系统与开源项目只提供参考、适配器能力或工程经验，不拥有本系统语义定义权。

## 当前权威资产

首轮治理阶段明确只读消费以下权威输入：

```text
H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4
H:\Asteria-Validated\MALF_Three_Part_Design_Set_v1_4.zip
H:\Asteria-Validated\Asteria_System_Design_Set_v1_0
H:\Asteria-Validated\MALF-system-history
H:\Asteria-Validated\MALF-reference
G:\malf-history
G:\《股市浮沉二十载》\2020.(Au)LanceBeggs
```

当前裁决：

```text
MALF v1.4 is immutable.
PAS must be re-axiomatized.
No formal DB mutation is authorized.
No broker or live-trading discussion is opened by this repo initialization.
```

## 阅读入口

1. [Agent 规则](AGENTS.md)
2. [文档入口](docs/README.md)
3. [重构总纲](docs/00-governance/00-malf-pas-reconstruction-charter-v1.md)
4. [来源裁决与非迁移规则](docs/00-governance/01-source-authority-and-non-migration-rule-v1.md)
5. [执行记录协议](docs/00-governance/02-execution-record-protocol-v1.md)
6. [repo 治理环境 bootstrap](docs/00-governance/03-repo-governance-environment-bootstrap-v1.md)
7. [主线权威图](docs/01-architecture/00-mainline-authoritative-map-v1.md)
8. [MALF v1.4 锚点位置](docs/01-architecture/01-malf-v1-4-anchor-position-v1.md)
9. [旧系统强项地图](docs/01-architecture/02-predecessor-strength-map-v1.md)
10. [模块设计文档标准](docs/02-modules/00-module-design-document-standard-v1.md)
11. [PAS 公理化状态机](docs/02-modules/01-pas-axiomatic-state-machine-v1.md)
12. [首张治理路线图](docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md)
13. [执行区入口](docs/04-execution/README.md)

## 开发检查

```powershell
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```
