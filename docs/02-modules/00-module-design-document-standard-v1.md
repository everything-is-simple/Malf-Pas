# Malf-Pas 模块设计文档标准 v1

日期：2026-05-15

## 1. 目的

任何模块进入 `src/` 或正式 DB 设计之前，必须先拥有可审阅、可冻结、可测试的权威设计文档。

## 2. 每个模块必须有的文档

| 顺序 | 文档 | 作用 |
|---:|---|---|
| 1 | Authority Design | 模块定义、职责边界、依赖方向、状态机 |
| 2 | Semantic Contract | 输入输出语义、字段含义、禁止表达 |
| 3 | Database Schema Spec | DB 名称、表族、自然键、版本字段 |
| 4 | Runner Contract | CLI/API、build mode、checkpoint、幂等 |
| 5 | Audit Spec | 硬规则、软观察、失败裁决 |
| 6 | Build Card | 本轮只动什么、不动什么、验收口径 |
| 7 | Evidence / Record / Conclusion | 执行闭环 |

## 3. Authority Design 最小结构

```text
1. 模块定义
2. 模块只回答什么
3. 模块不回答什么
4. 输入
5. 输出
6. 状态机或数据流图
7. 核心表族
8. 自然键
9. 版本字段
10. 上游依赖
11. 下游消费者
12. 不变量检查
13. 上线门禁
```

## 4. 首轮特殊规则

当前阶段只有 PAS 允许进入“公理化定义文档”层，不允许进入 schema、runner 或 runtime。

## 5. 画图要求

| 内容 | 图类型 |
|---|---|
| 模块上下游 | `flowchart` |
| 状态转换 | `stateDiagram` |
| 构建顺序 | `flowchart` |

## 6. 当前禁止项

- 未冻结 Authority Design 就写实现
- 用 runtime 结果倒推定义
- 用 Position / Trade 语义污染 PAS
- 在没有正式合同前定义正式 DB

