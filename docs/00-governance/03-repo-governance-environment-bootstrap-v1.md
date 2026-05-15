# Malf-Pas repo 治理环境 bootstrap v1

日期：2026-05-15

状态：passed / governance-environment-bootstrap

## 1. 目标

本文件冻结 `repo-governance-environment-bootstrap-card` 的边界：本仓库可以从
`H:\Asteria` 吸收治理环境经验，但只能形成 Malf-Pas 自己的 repo-local 治理骨架。

## 2. 迁入裁决

| 面 | 裁决 | repo-local 落点 |
|---|---|---|
| workflow plugin 形态 | 允许改造成 Malf-Pas workflow skeleton | `plugins/malf-pas-workflow` |
| governance check script | 允许改造成本仓库治理检查 | `scripts/governance/check_project_governance.py` |
| dev doctor | 允许改成本仓库环境读出 | `scripts/dev/doctor.py` |
| package / lint / test 配置 | 允许建立最小 Python 工具层 | `pyproject.toml` |
| conda fallback | 允许建立可重建环境说明 | `environment.yml` |
| ignore rules | 必须补齐缓存、DB、report、temp 忽略 | `.gitignore` |
| agent rules | 允许继承治理纪律写法，但必须重写权威集与阶段真值 | `AGENTS.md` |
| repo entry | 允许继承入口结构、关键路径、阅读入口写法，但不得复制 Asteria release state | `README.md` |
| Codex repo-local 规则 | 允许文档化技能边界；不得迁入秘密 | `.codex/` |
| machine-readable governance | 允许建立 registry / topology / bootstrap placeholders | `governance/*.toml` |

本卡对你点名的四个治理面，当前已落地为：

| Asteria 来源 | Malf-Pas 当前落点 |
|---|---|
| `H:\Asteria\.codex` | `.codex/README.md` 与 `.codex/skills/malf-pas-governance/SKILL.md` |
| `H:\Asteria\.gitignore` | `.gitignore` |
| `H:\Asteria\AGENTS.md` | `AGENTS.md` |
| `H:\Asteria\README.md` | `README.md` |

`.venv` 的处理口径单独固定如下：

```text
copy H:\Asteria\.venv -> forbidden
reference H:\Asteria\.venv package feasibility -> allowed
create H:\Malf-Pas\.venv from local Python 3.11 -> allowed and preferred
install -e .[dev] into H:\Malf-Pas\.venv -> allowed
commit .venv into repo -> forbidden
```

## 3. 明确不迁入

| 来源 | 裁决 |
|---|---|
| `H:\Asteria\.venv` | 不复制；只作为依赖可行性参考 |
| `H:\Asteria\scripts\malf` 等业务 runner | 不迁入；第一张 roadmap 不授权 runtime |
| Asteria released state | 不复制；Malf-Pas 当前仍是治理初始化 |
| Asteria formal DB / report / temp outputs | 不迁入；本仓库不得落运行产物 |
| 旧系统 schema / DuckDB 表面 | 不迁入；后续必须先冻结目标设计 |

## 4. 当前机器可读骨架

| 文件 | 作用 |
|---|---|
| `governance/repo_governance_registry.toml` | repo 根、阶段、硬规则、下一卡 |
| `governance/module_gate_registry.toml` | 治理卡状态与下一张允许卡 |
| `governance/database_topology_registry.toml` | formal root 与 DB mutation 禁令 |
| `governance/environment_bootstrap_registry.toml` | 继承 / 不继承 surface 的机器可读裁决 |
| `governance/module_api_contracts/README.md` | 后续模块合同目录占位；当前不冻结业务合同 |

## 5. 验证命令

```powershell
python -m venv H:\Malf-Pas\.venv
H:\Malf-Pas\.venv\Scripts\python.exe -m pip install --upgrade pip
H:\Malf-Pas\.venv\Scripts\python.exe -m pip install -e ".[dev]"
python scripts\dev\doctor.py
python scripts\governance\check_project_governance.py
python -m unittest discover -s tests -p "test_*.py"
```

## 6. 门禁影响

```text
repo-local workflow hooks = present
repo-local governance checks = present
reproducible environment config = present
machine-readable governance skeleton = present
clean ignore rules = present
copied virtualenv = no
copied business runtime = no
formal DB mutation = no
broker feasibility = deferred
next card = system-mainline-module-ownership-card
```
