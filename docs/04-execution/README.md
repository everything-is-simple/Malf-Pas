# Malf-Pas 执行区入口

本目录负责 repo 内 execution discipline、模板和结论索引。

## 1. 四件套

| 文档 | 作用 |
|---|---|
| `card` | 本次执行目标、输入范围、允许动作、禁止动作 |
| `evidence-index` | 外部证据路径、关键指标、关键审计值 |
| `record` | 执行经过、关键步骤、关键验证 |
| `conclusion` | 最终裁决与门禁影响 |

没有这四件套，就不算 repo 内闭环完成。

四件套文件名必须带三位路线图顺序号前缀：

```text
<NNN>-<run_id>.card.md
<NNN>-<run_id>.evidence-index.md
<NNN>-<run_id>.record.md
<NNN>-<run_id>.conclusion.md
```

示例：`003-system-mainline-module-ownership-card-20260515-01.conclusion.md`。

## 2. 目录结构

```text
docs/04-execution/
  README.md
  00-conclusion-index-v1.md
  templates/
  records/
```

## 3. 第一阶段说明

第一阶段治理卡允许 `report_dir / manifest / validated_asset / formal_db` 为 `not applicable`，
但不允许缺失 `conclusion index registration`。
