<div align="center">
  <img src="./assets/banner.svg" alt="git-batch-commit banner" width="100%" />
</div>

<p align="center">
  <a href="#chinese">中文</a> | <a href="#english">English</a>
</p>

---
<a name="chinese"></a>

# git-batch-commit

自动将暂存的 Git 变更按意图拆分为单元级提交，并生成英文 gitmoji 风格的提交信息。

非常适合当 `git add .` 混入了多种类型的变更（如 ESLint / 依赖 / Swagger / DTO / 样式 / 业务逻辑）时，你想将它们拆分隔离为多个独立提交的场景。

---

## 核心特性

- **敏感文件拦截** - 检测到 `.env` / `*.pem` / `credentials*` 等敏感文件在暂存区时，将立即停止执行
- **按意图而非目录分组** - 基于变更意图进行独立的逻辑分组提交，而非机械地按照目录进行拆分
- **中等置信度确认机制** - 当 AI 无法确定分组是否合理时，需用户明确确认/调整后方可继续
- **空运行预览 (Dry-Run)** - 在实际提交前支持预览基于 glob 展开的文件列表
- **撤销机制** - 支持软重置（soft reset），以便在意外提交后能快速恢复此前的暂存状态
- **分支状态感知** - 自动检测未推送的提交、缺失的上游分支，并给出适当的警告
- **Hook 失败处理** - 自动识别 lint / commit-msg / pre-commit 等钩子的执行失败情况并建议修复方案
- **PR 摘要生成** - 在提交完成后，可进一步生成 PR 标题、描述以及 CHANGELOG 条目
- **跨平台兼容** - 基于 Python 3 编写，完美支持 Windows / Linux / macOS

---

## 兼容性

兼容任何允许加载自定义 skill 目录结构并支持读取 `SKILL.md` 的 AI 代理终端或编辑器。

---

## 安装说明

### 选项 1：使用npx安装
```bash
npx skills add Charry-039/skills --path git-batch-commit
```

### 选项 2：克隆至本地skills目录 (示例)
以在 Claude Code 中使用为例，可克隆至如下路径：

```bash
cd ~/.claude-code/skills/
git clone https://github.com/Charry-039/skills/git-batch-commit.git
```

---

## 使用指南

### 运行模式

- 建议模式 / Suggestion mode (默认)
- 执行模式 / Execution mode
- 空运行模式 / Dry-run mode
- 仅建议模式 / Suggestion-only mode

详细工作流、安全检查和确认机制请在此技能内部参阅 `SKILL.md`。

### 触发短语

| 输入短语 (Input) | 触发模式 (Mode) |
|-------|------|
| `/git-batch-commit` | 建议模式 (默认) |
| `整理我暂存的更改` | 建议模式 (默认) |
| `立即拆分并提交` | 执行模式 |
| `仅分组` | 仅建议模式 |
| `预览` / `空运行` | 空运行模式 |
| `撤销上一批` / `撤销` | 撤销模式 |

### 典型工作流

**1. 首先你执行了大范围的暂存操作：**

```bash
git add .
```

**2. 激活此技能：**

```
按意图拆分这些分阶段文档。
```

**3. 随后技能将自动分析暂存区差异，并为你呈现建议的分组计划：**

```
I identified 3 suggested commits:

1. :sparkles: feat(api): add response DTOs and Swagger docs
   - Files: src/dto/response.dto.ts, src/dto/pagination.dto.ts
   - Reason: Response models and API docs are the same unit of change
   - Confidence: high

2. :wrench: chore(eslint): update ESLint config and fix rule conflicts
   - Files: eslint.config.js, package.json
   - Reason: Toolchain configuration update
   - Confidence: high

3. :lipstick: style(styles): refine the style system
   - Files: src/styles/theme.css
   - Reason: Style system changes
   - Confidence: medium

   About group 3 (confidence: medium):
   Choose: A. keep separate  B. merge with another group  C. split  D. cancel

Confirm and I will commit in this order.
```

**4. 确认后，你可以（可选）进行空运行预览：**

```bash
python3 scripts/batch-commit.py --dry-run
```

**5. 确认无误后执行正式提交：**

```bash
python3 scripts/batch-commit.py
```

**6. 执行完成：**

```
完成。已创建 3 个提交：

1. :sparkles: feat(api): 添加响应 DTO 和 Swagger 文档   (a1b2c3d)
2. :wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突   (e4f5g6h)
3. :lipstick: style(styles): 统一主题 token     (i7j8k9l)

你需要生成 PR 标题、描述或 CHANGELOG 条目吗？
```

---

## 脚本清单

| 脚本文件 | 用途 |
|--------|---------|
| `check-staged.py` | 预检暂存区：预防敏感文件、构建产物或同时处于暂存/未暂存状态的文件导致的执行冲突 |
| `batch-commit.py` | 基于自动生成的 manifest.json 按批次提交，支持 `--dry-run` 与 `--rollback-on-fail` |
| `batch-undo.py` | 撤销技能上一批次操作所产生的提交（软重置，文件退回暂存状态） |

---

## 目录结构

```
git-batch-commit/
├── SKILL.md
├── README.md
├── references/
│   ├── commit-types.md
│   ├── grouping-rules.md
│   └── security.md
└── scripts/
   ├── batch-commit.py
   ├── batch-undo.py
   └── check-staged.py
```

## 参考文献

- commit-types.md: gitmoji 与约定式提交类型的映射规则
- grouping-rules.md: 基于意图的变更分组策略规范
- security.md: 敏感文件判定与安全边界规定

---

## 策略：如何分组

工具在处理时优先将下列变更各自作为独立批次提取：

| 变更类型 | 示例文件 |
|------|---------------|
| ESLint / 工具链 | `eslint.config.js`, `tsconfig*.json`, `nest-cli.json` |
| 依赖更新 | `package.json`, `package-lock.json`, `pnpm-lock.yaml` |
| Swagger / DTO | `*response.dto.ts`, `*pagination.dto.ts`, 以及对应的 Swagger 注解 |
| 样式系统 | `tailwind.config.*`, `*.theme.css`, `token*.css` |
| 业务逻辑 | 按不同的业务领域（如 auth / tasks / votes 等）独立分组 |
| 文档 | `README.md`, `docs/` |

---

## 安全规则

**绝对禁止执行以下操作：**

- 在评估置信度为 `low` 或是存在未确认的 `medium` 置信度组时直接执行提交
- 使用 `--no-verify` 参数尝试绕过或跳过任何 Git Hooks
- 尝试执行 `push --force` (强制推送)
- 执行 `git commit --amend`（除非得到了用户的明确指令）
- 提交任何敏感文件（如 `.env`, `*.pem`, `credentials*` 等）
- 提交二进制工件资源、构建输出结果或运行日志文件

---

## 环境要求

- Python 3.6+
- 正常可用的 Git 环境

---

## 许可证

MIT

<a name="english"></a>

# git-batch-commit

Automatically organize staged Git changes into unit-level, intent-based commits with gitmoji-style messages in English.

Ideal when `git add .` mixes multiple types of changes (ESLint / deps / Swagger / DTO / styles / business logic) and you want to split them into separate commits.

---

## Features

- **Sensitive File Blocking** - `.env` / `*.pem` / `credentials*` and similar files in staging area immediately stop execution
- **Group by Intent, Not Directory** - identifies independent commits based on change intent, not mechanical directory splitting
- **Medium-Confidence Confirmation Gate** - when AI is uncertain, requires explicit user resolution before proceeding
- **Dry-Run Preview** - preview glob-expanded file lists before actual commits
- **Undo Mechanism** - soft reset to recover staged state after accidental commits
- **Branch Awareness** - detects unpushed commits, missing upstream, and warns appropriately
- **Hook Failure Handling** - auto-identifies lint / commit-msg / pre-commit failures and suggests fixes
- **PR Summary Generation** - generates PR title, description, and CHANGELOG entries after commits
- **Cross-Platform** - Python 3, works on Windows / Linux / macOS

---

## Compatibility

Compatible with any AI agent terminal or editor that can load a skill folder and read `SKILL.md`.

---

## Installation

### Option 1: Using npx
```bash
npx skills add Charry-039/skills --path git-batch-commit
```

### Option 2: Clone to a Local Skills Directory (Example)

Example path for Claude Code:

```bash
cd ~/.claude-code/skills/
git clone https://github.com/Charry-039/skills/git-batch-commit.git
```

---

## Usage

### Modes

- Suggestion mode (default)
- Execution mode
- Dry-run mode
- Suggestion-only mode

See `SKILL.md` for the full workflow, safety checks, and confirmation gates.

### Trigger Phrases

| Input | Mode |
|-------|------|
| `/git-batch-commit` | Suggestion Mode (default) |
| `organize my staged changes` | Suggestion Mode (default) |
| `split and commit now` | Execution Mode |
| `group only` | Suggestion Only Mode |
| `preview` / `dry run` | Dry-run Mode |
| `undo last batch` / `undo` | Undo Mode |

### Typical Workflow

**1. You run a large `git add`:**

```bash
git add .
```

**2. Activate the skill:**

```
Split these staged files by intent.
```

**3. Skill analyzes staged diff and presents grouping plan:**

```
I identified 3 suggested commits:

1. :sparkles: feat(api): add response DTOs and Swagger docs
   - Files: src/dto/response.dto.ts, src/dto/pagination.dto.ts
   - Reason: Response models and API docs are the same unit of change
   - Confidence: high

2. :wrench: chore(eslint): update ESLint config and fix rule conflicts
   - Files: eslint.config.js, package.json
   - Reason: Toolchain configuration update
   - Confidence: high

3. :lipstick: style(styles): refine the style system
   - Files: src/styles/theme.css
   - Reason: Style system changes
   - Confidence: medium

   About group 3 (confidence: medium):
   Choose: A. keep separate  B. merge with another group  C. split  D. cancel

Confirm and I will commit in this order.
```

**4. After confirmation, optional dry-run preview:**

```bash
python3 scripts/batch-commit.py --dry-run
```

**5. Execute:**

```bash
python3 scripts/batch-commit.py
```

**6. Done:**

```
Done. Created 3 commits:

1. :sparkles: feat(api): add response DTOs and Swagger docs   (a1b2c3d)
2. :wrench: chore(eslint): update ESLint config and fix rule conflicts   (e4f5g6h)
3. :lipstick: style(styles): unify theme tokens     (i7j8k9l)

Do you want a PR title, description, or CHANGELOG entry?
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `check-staged.py` | Pre-check staged files: sensitive files, build artifacts, staged/unstaged conflicts |
| `batch-commit.py` | Execute commits batch-by-batch from manifest.json, supports --dry-run / --rollback-on-fail |
| `batch-undo.py` | Undo the last batch of commits (soft reset, files return to staged) |

---

## Structure

```
git-batch-commit/
├── SKILL.md
├── README.md
├── references/
│   ├── commit-types.md
│   ├── grouping-rules.md
│   └── security.md
└── scripts/
   ├── batch-commit.py
   ├── batch-undo.py
   └── check-staged.py
```

## References

- commit-types.md: gitmoji + conventional types mapping
- grouping-rules.md: intent-based grouping strategy
- security.md: sensitive file and safety boundaries

---

## Grouping Strategy

Change types that are prioritized as independent batches:

| Type | Example Files |
|------|---------------|
| ESLint / Toolchain | `eslint.config.js`, `tsconfig*.json`, `nest-cli.json` |
| Dependencies | `package.json`, `package-lock.json`, `pnpm-lock.yaml` |
| Swagger / DTO | `*response.dto.ts`, `*pagination.dto.ts`, Swagger annotations |
| Style System | `tailwind.config.*`, `*.theme.css`, `token*.css` |
| Business Logic | Grouped by domain (auth / tasks / votes, etc.) |
| Documentation | `README.md`, `docs/` |

---

## Safety Rules

**NEVER perform:**

- Committing when confidence is low or medium-confidence groups are unresolved
- Using `--no-verify` to skip Git hooks
- Using `push --force`
- Using `git commit --amend` unless explicitly asked
- Committing sensitive files (`.env`, `*.pem`, `credentials*`, etc.)
- Committing binary artifacts, build outputs, or log files

---

## Requirements

- Python 3.6+
- Git

---

## License

MIT