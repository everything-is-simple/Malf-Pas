# Malf-Pas 首张治理路线图 v1

日期：2026-05-15

状态：active / governance-only roadmap

## 1. 定位

本路线图是新系统的第一张路线图，只负责立法，不负责施工实现。

## 2. 共通边界

所有卡共享以下属性：

```text
governance-only
doc-first
read-only-to-validated-assets
no-formal-db-mutation
no-broker
no-profit-claim
no-legacy-code-migration
```

## 3. 六张治理卡

| 顺序 | 卡 | 状态 | 目标 |
|---:|---|---|---|
| 1 | `governance-roadmap-freeze-card` | active | 固定第一张路线图边界与命名口径 |
| 2 | `source-authority-and-non-migration-rule-card` | planned | 冻结来源分类与非迁移规则 |
| 3 | `malf-v1-4-immutability-anchor-card` | planned | 锚定 MALF v1.4 的系统位置与不变量 |
| 4 | `predecessor-strength-map-card` | planned | 盘点旧系统与历史资料的最出彩强项 |
| 5 | `pas-axiomatic-state-machine-card` | planned | 冻结 PAS 最小状态机与七层语义 |
| 6 | `open-source-adapter-boundary-card` | planned | 固定开源项目的 adapter 边界 |

## 4. 通过标准

| 卡 | 通过标准 |
|---|---|
| `governance-roadmap-freeze-card` | 主落点、远端、阶段边界写死 |
| `source-authority-and-non-migration-rule-card` | 分类枚举与非迁移规则冻结 |
| `malf-v1-4-immutability-anchor-card` | MALF 锚点与不变量列明 |
| `predecessor-strength-map-card` | 每个主要来源都有可吸收强项与禁止迁移说明 |
| `pas-axiomatic-state-machine-card` | lifecycle、七层语义、handoff 边界冻结 |
| `open-source-adapter-boundary-card` | 每个主要开源项目都有允许角色与禁止越界说明 |

## 5. 当前结论

```text
This roadmap is legislation-first.
It does not authorize runtime, DB, broker, or strategy claims.
```

