# Malf-Pas 执行记录协议 v1

日期：2026-05-15

## 1. 目标

本协议规定：本仓库如何对每张卡形成 repo 内可追溯闭环。

## 2. 最小闭环

每张卡都必须具备四件套：

| 文档 | 作用 |
|---|---|
| `card` | 说明本次为什么开工、只动什么、不动什么 |
| `evidence-index` | 外部证据路径、关键指标、关键审计值 |
| `record` | 执行顺序、关键验证、关键决策 |
| `conclusion` | `passed / blocked / superseded / failed` 结论与门禁影响 |

## 2.1 人话版收口

每张卡完成后，`conclusion` 必须附带一段简短的人话版总结，用普通语言说明这张卡到底完成了什么、
没有做什么、以及下一步是什么。

要求：

1. 必须写在 `conclusion` 文档里，作为固定章节，而不是临时聊天说明。
2. 语气要短、直接、可读，优先解释“这张卡把什么边界钉住了”。
3. 不得夸大成 runtime 完成、正式 DB 完成或 broker 完成。
4. 若结果是 `blocked`，人话版总结也必须真实说明堵点。

## 3. 第一阶段特例

第一张路线图属于 `governance-only` 路线，因此：

| 项 | 裁决 |
|---|---|
| formal DB | `not applicable` |
| runtime evidence | `not applicable` |
| validated zip | `optional later` |
| report_dir | `optional later` |
| conclusion index registration | `required` |

## 4. 目录结构

```text
docs/04-execution/
  README.md
  00-conclusion-index-v1.md
  templates/
  records/
    <module_or_route>/
      <NNN>-<run_id>.card.md
      <NNN>-<run_id>.evidence-index.md
      <NNN>-<run_id>.record.md
      <NNN>-<run_id>.conclusion.md
```

`NNN` 必须使用三位路线图顺序号，例如 `001-`、`002-`、`003-`。文件名前缀只表达
roadmap 顺序，不进入 `run_id` 字段本身。

## 5. truthful 规则

- roadmap 不是 conclusion。
- 没有 evidence-index 的 passed，不算 passed。
- blocked 卡必须真实说明 blocked 原因，不得改写成 planned。
- governance-only 卡不得伪装成 runtime 卡。
