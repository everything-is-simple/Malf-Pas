# Backtest Window And Holdout Protocol Conclusion

日期：2026-05-15

## 1. 结论

| 项 | 值 |
|---|---|
| run_id | `backtest-window-and-holdout-protocol-card-20260515-01` |
| result | `passed` |
| next action | `进入 source-authority-and-non-migration-rule-card，继续冻结来源分类与非迁移规则。` |

## 2. 人话版结论

这张卡现在把“以后回测不能混样本”先钉住了：`2012..2021` 可以作为十年历史覆盖口径，
但真正用于选择、调参和策略筛选的窗口只到 `2020`。`2021` 开始归入 `2021..2023` 预留段，
`2024..2026` 是第二个预留段，后续没有独立 proof 前都不能拿来反向挑规则。

它没有跑回测，没有证明收益，没有写 `H:\Malf-Pas-data`，也没有读取或改写上一版 `H:\Asteria-data`。
下一步进入第 8 卡，继续冻结来源分类和非迁移规则。

## 3. 门禁影响

| 项 | 影响 |
|---|---|
| live next | `source-authority-and-non-migration-rule-card` |
| formal DB mutation | `no` |
| broker feasibility | `deferred` |
| legacy code migration | `not authorized` |
| runtime implementation | `not authorized` |
| backtest execution | `not authorized in this card` |
| profit proof | `not authorized` |
| current data root | `H:\Malf-Pas-data (not accessed)` |
| previous data root reference | `H:\Asteria-data (read-only reference, not accessed)` |

## 4. 关闭条件

- `docs/01-architecture/07-backtest-window-and-holdout-protocol-v1.md` 已建立。
- `governance/backtest_window_holdout_registry.toml` 已建立。
- roadmap、结论索引、gate registry 与 repo registry 已同步。
- 第 7 卡 execution 四件套已建立。
- repo-local 验证通过。
