# git-batch-commit 汉化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `git-batch-commit` skill 的主要语言从英文改为中文简体，包括 `SKILL.md`、参考文档、脚本输出和 `README.md` 中文部分，同时保留约定式提交类型与 gitmoji。

**Architecture：** 对所有用户可见的英文文本进行逐文件翻译替换；脚本内部命令与逻辑、Git 操作、文件路径、类型名与 gitmoji 保持不变。

**Tech Stack：** Markdown、Python 3、Git

---

## 文件结构

| 文件 | 操作 | 说明 |
|---|---|---|
| `git-batch-commit/SKILL.md` | 修改 | 核心 skill 文档，全部改为中文 |
| `git-batch-commit/references/commit-types.md` | 修改 | 提交类型映射表，描述与示例改为中文 |
| `git-batch-commit/references/grouping-rules.md` | 修改 | 分组策略文档改为中文 |
| `git-batch-commit/references/security.md` | 修改 | 安全规则文档改为中文 |
| `git-batch-commit/scripts/check-staged.py` | 修改 | 预检脚本输出改为中文 |
| `git-batch-commit/scripts/batch-commit.py` | 修改 | 批量提交脚本输出改为中文 |
| `git-batch-commit/scripts/batch-undo.py` | 修改 | 撤销脚本输出改为中文 |
| `git-batch-commit/README.md` | 修改 | 中文部分更新，英文部分保留 |

---

### Task 1: 更新 `SKILL.md` 前半部分（frontmatter、概述、反模式、模式表、预检）

**Files:**
- Modify: `git-batch-commit/SKILL.md:1-69`

- [ ] **Step 1: 将 `SKILL.md` 前 69 行替换为以下中文内容**

```markdown
---
name: git-batch-commit
description: 自动将暂存的 Git 变更按意图拆分为单元级、基于意图的提交，并生成 gitmoji 风格的中文提交信息。适用于单次 git add 混入了多种变更类型（ESLint / 依赖 / Swagger / DTO / 样式 / 业务逻辑）且希望按意图干净拆分的场景。按意图而非目录分组。支持 Windows / Linux / macOS 跨平台运行。
license: MIT
---

# Git-Batch-Commit

本 skill 会分析已暂存的 Git 变更，按意图分组，并生成清晰、可审查的提交计划与提交信息。它优先执行安全检查，并在任何提交操作前要求用户明确确认。


铁律：在置信度低或检测到敏感文件时，绝不提交 —— 先建议，再提交。

## 需要避免的反模式

**这是最重要的部分 —— 每次运行前请先阅读。**

- **不要** 在未展示分组计划的情况下盲目提交（除非用户说“立即提交”）
- **不要** 将无关意图混入同一个提交（例如：依赖 + 业务逻辑）
- **不要** 跳过敏感文件检查 —— 发现 `.env`、`*.pem`、`credentials*` 等文件必须立即停止
- **不要** 使用 `--no-verify` 或 `git commit --amend`，除非用户明确要求
- **不要** 使用 `push --force`
- **不要** 提交二进制产物、构建输出或日志文件
- **不要** 仅按目录分组 —— 按意图分组（同一目录下的配置变更与业务逻辑变更不属于同一个提交）
- **不要** 跳过未暂存文件检查 —— 如果同一文件同时处于暂存和未暂存状态，必须先警告用户
- **不要** 在未阅读 diff 的情况下猜测意图 —— 在标注分组前先查看 `git diff --cached` 的补丁内容

## 工作流

### 第 0 步：确定模式（必需）

先问：用户请求的是哪种模式？

| 用户输入 | 模式 |
|---|---|
| "整理/拆分/批量处理我暂存的变更"（不含“立即提交”） | **建议模式**（默认） |
| "立即拆分并提交" / "无需确认" | **执行模式** |
| "仅分组" / "起草提交信息" | **仅建议模式** |
| "预览" / "空运行" / "看看会怎样" | **空运行模式** |

在模式明确之前，不要继续后续步骤。

### 第 1 步：预检（阻塞式）

警告 —— 在分析任何内容前先运行：

```bash
python3 scripts/check-staged.py
```

该脚本会检查：
- 是否存在已暂存文件
- 是否包含敏感文件（`.env`、`*.pem`、`credentials*` 等）
- 是否包含二进制产物或构建输出
- 是否存在同一文件同时处于暂存和未暂存状态
- 分支状态（未推送提交、上游跟踪情况）

**如果发现敏感文件 -> 立即停止。告知用户具体文件，并建议手动处理。**

**如果没有已暂存变更 -> 立即停止。告知用户暂存区为空。**

**如果同一文件同时处于暂存和未暂存状态 -> 默认仅进入建议模式，并警告用户。**

**如果当前分支存在未推送提交：**
- 警告："当前分支有 N 个未推送提交。重置操作将改写历史。是否继续？"
- 不要自动继续 —— 必须得到用户确认后才能进入第 5 步。

**跨平台：** 脚本支持 Windows / Linux / macOS（需要 Python 3）。
```

- [ ] **Step 2: 运行语法检查**

Run: `python3 -c "import markdown; markdown.markdown(open('git-batch-commit/SKILL.md').read())"` 或目视检查无错位。
Expected: 无报错，frontmatter 完整。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/SKILL.md
git commit -m ":memo: docs: translate SKILL.md introduction and pre-check to Chinese"
```

---

### Task 2: 更新 `SKILL.md` 中间部分（分析分组、生成提交信息、展示计划）

**Files:**
- Modify: `git-batch-commit/SKILL.md:70-137`

- [ ] **Step 1: 将 `SKILL.md` 第 70-137 行替换为以下中文内容**

```markdown
### 第 2 步：分析分组

必需 —— 在标注分组前请先阅读实际 diff 内容。

加载 `references/grouping-rules.md` 获取详细分组策略。

针对每个已暂存文件，问自己以下问题：

1. **变更意图是什么？**（新功能、bug 修复、配置、依赖、样式、文档）
2. **是否与其他文件相关？**（controller + service + dto = 同一意图）
3. **这是否是高置信度的独立分组？**（ESLint 配置、package.json、样式系统 = 几乎总是独立）
4. **应该与其他文件合并，还是单独成组？**

高置信度独立分组：
- `eslint.config.js`、`.eslintrc*`、`tsconfig*`、`nest-cli.json` -> `chore(eslint)`
- `package.json` + 锁文件（仅依赖变更） -> `build(deps)`
- `tailwind.config.*`、`*.theme.css`、`token*.css` -> `style(styles)`
- `swagger`、`openapi`、`*response.dto.ts`、`*pagination.dto.ts` -> `feat(api)` 或 `build(deps)`
- `*.spec.ts`、`test/**/*.ts` 与对应源码一起 -> 与源文件同一意图

分组范围优先级：`auth`、`tasks`、`votes`、`summaries`、`discussions`、`companions`、`users`、`api`、`eslint`、`deps`、`build`、`styles`

### 第 3 步：生成提交信息

加载 `references/commit-types.md` 获取类型/gitmoji 映射与格式规则。

每个分组生成一条提交信息，格式为：`:gitmoji: type(scope): 中文描述`

规则：
- 使用中文
- 描述意图，而非改动了哪些文件
- scope 来自上述优先级列表
- 如果不确定 scope，使用更宽泛的类别（`api`、`build`）

### 第 4 步：展示计划 + 门控（必需）

按以下格式展示计划：

```markdown
我识别出 N 个建议提交：

1. `<提交信息>`
   - 文件：...
   - 原因：...
   - 置信度：高/中

2. ...

确认后我将按此顺序执行提交。
```

#### 中等置信度分组 —— 在继续前必须解决

对每个中等置信度分组，明确询问用户：

> **关于第 X 组（置信度：中）：**
> 文件：...
> 原因：...
>
> 请选择：
> A. 保持为独立提交
> B. 合并到上一个/下一个分组
> C. 拆分为其他分组
> D. 取消该分组（暂不提交）

**在所有中等置信度分组都得到明确用户解决之前，不要进入第 5 步。**

整体门控问题：**是否按此计划继续（所有中等置信度分组已解决），还是需要调整？**
```

- [ ] **Step 2: 检查提交信息格式示例是否已改为中文**

Run: `grep -n "type(scope):" git-batch-commit/SKILL.md`
Expected: 显示 `:gitmoji: type(scope): 中文描述`，无 "English description" 字样。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/SKILL.md
git commit -m ":memo: docs: translate SKILL.md grouping and message generation to Chinese"
```

---

### Task 3: 更新 `SKILL.md` 后半部分（执行、摘要、撤销、输出模板）

**Files:**
- Modify: `git-batch-commit/SKILL.md:138-318`

- [ ] **Step 1: 将 `SKILL.md` 第 138 行至文件末尾替换为以下中文内容**

```markdown
### 第 5 步：执行提交（仅执行模式）

用户确认且所有中等置信度分组已解决后：

**5a. 重新验证暂存状态** —— 运行 `git diff --cached --name-only`，确认自第 1 步以来没有新增变更。

**5b. 生成清单文件** `.git-batch-manifest.json`：

```json
{
  "commits": [
    {
      "message": ":sparkles: feat(api): 添加 tasks 模块",
      "files": ["src/tasks/*.ts", "src/dto/task*.ts"]
    },
    {
      "message": ":wrench: chore(eslint): 更新 ESLint 配置",
      "files": ["eslint.config.js", "package.json"]
    }
  ]
}
```

将该文件写入仓库根目录的 `.git-batch-manifest.json`。

**5c. 提交前提供空运行预览：**

询问：**"执行前是否需要空运行预览？"**

如果需要：

```bash
python3 scripts/batch-commit.py --dry-run
```

空运行会展示：
- 每次提交展开 glob 后的具体文件列表
- 将要执行的 git 命令
- 清单文件会被保留，供后续执行或调整

**5d. 执行：**

```bash
# 默认：失败时停止，不自动回滚
python3 scripts/batch-commit.py

# 可选：失败时自动回滚所有已成功提交
python3 scripts/batch-commit.py --rollback-on-fail
```

**回滚行为：**
- 在任何提交前保存当前 HEAD
- 如果某次提交失败，询问是否回滚
- 使用 `--rollback-on-fail` 时自动回滚到保存的 HEAD
- 成功的提交不会自动回滚 —— 由用户决定是否回滚

**如果某次提交失败：**
- 停止后续提交
- 报告哪次提交失败及原因
- 报告失败前成功提交的次数
- 询问："是否回滚已成功提交？"

### Hook 失败处理策略

当 `git commit` 返回非零且 stderr 包含 hook 关键词时：

| stderr 关键词 | 可能原因 | 处理方式 |
|---|---|---|
| `pre-commit` | lint/format 检查失败 | 说明哪条规则失败及如何修复，然后重新运行 |
| `commit-msg` | 提交信息格式无效 | 展示所需格式，生成修正后的信息，重新提交 |
| `post-commit` | 非关键 hook 失败 | 警告用户：提交已成功，但 post-hook 失败 |
| `lint` / `eslint` / `prettier` | 代码检查失败 | 列出失败文件和规则，建议修复命令 |

**处理流程：**

1. 解析 stderr 并识别 hook 类型
2. 如果是 `commit-msg`：生成修正后的提交信息，询问用户确认后重新提交
3. 如果是 `pre-commit`（lint/format）：说明失败原因和修复命令，不自动回滚
4. 如果是 `post-commit`：提交已成功，仅警告用户
5. 如果无法识别：停止并报告错误文本，建议用户手动处理

**禁止：**
- 不要使用 `--no-verify` 绕过 hook
- 不要未分析原因就回滚

### 第 6 步：摘要

执行完成后（或在建议模式下展示计划后）：
- 创建了多少个提交
- 每条提交信息 + 短 hash
- 剩余的暂存/未暂存文件及未包含原因

**提供 PR 摘要生成：**

所有提交成功后，询问：**"是否需要生成 PR 标题、描述或 CHANGELOG 条目？"**

如果需要，基于提交信息生成：

```markdown
## PR 标题
feat(api): 添加响应 DTO 和 Swagger 文档

## PR 描述
### 变更摘要
- `:sparkles: feat(api): 添加响应 DTO 和 Swagger 文档`
- `:wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突`

### 变更详情
（根据提交信息简要说明每次提交的意图）

### 测试建议
（根据变更文件给出：DTO 更新 -> 验证 API 响应格式；ESLint 变更 -> 运行 lint）
```

**CHANGELOG 条目生成：**

如果用户要求 CHANGELOG：

```markdown
## Changelog

### [Unreleased]
#### Features
- 添加响应 DTO 和 Swagger 文档
#### Chores
- 更新 ESLint 配置并修复规则冲突
```

CHANGELOG 规则：
- 按约定式类型分组：`Features`、`Bug Fixes`、`Chores`、`Refactors`、`Docs`
- 为提高可读性，去掉提交信息中的 gitmoji 和 scope
- 使用 `### [Unreleased]` 小节，或追加当天日期
- 标题：使用最重要的提交信息（优先 `feat` > `fix` > 其他）
- 描述：按类型列出所有提交信息
- 根据变更文件添加 "测试建议"（而非泛泛而谈）

### 撤销上一批

如果用户在批量提交后说 "撤销上一批" / "撤销"：

询问：**"想要撤销多少个提交？"**（默认撤销上一批全部）

```bash
python3 scripts/batch-undo.py
```

该脚本会：
- 展示上一批提交（来自清单）或询问数量
- 使用 `git reset --soft HEAD~N` 撤销（文件回到暂存状态，不会丢失）
- 清理清单文件
- 默认交互式确认；使用 `--all` 跳过确认

**不要使用 `git reset --hard` 撤销 —— 那会丢弃变更。**

## 输出模板

### 建议模式输出
```markdown
我识别出 N 个建议提交：

1. `<msg>`
   - 文件：...
   - 原因：...
   - 置信度：高/中

2. ...

确认后我将按此顺序执行提交。
```

### 执行模式输出
```markdown
已完成批量提交。创建了 N 个提交：

1. `<msg1>` (abc1234)
2. `<msg2>` (def5678)

如果需要，我可以：
- 检查剩余的暂存/未暂存变更
- 生成 PR 摘要 / 标题
```
```

- [ ] **Step 2: 验证无英文模板残留**

Run: `grep -n "Confirm and I will" git-batch-commit/SKILL.md || echo "OK"`
Expected: 输出 "OK"（无残留英文模板）。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/SKILL.md
git commit -m ":memo: docs: translate SKILL.md execution and summary sections to Chinese"
```

---

### Task 4: 翻译 `references/commit-types.md`

**Files:**
- Modify: `git-batch-commit/references/commit-types.md`

- [ ] **Step 1: 将文件完整替换为以下内容**

```markdown
# 提交类型与 Gitmoji 映射

优先级映射：

| 场景 | 约定式类型 | Gitmoji |
|----------|-------------------|---------|
| 新功能 | `feat` | `:sparkles:` |
| Bug 修复 | `fix` | `:bug:` |
| 文档 | `docs` | `:memo:` |
| 样式 / 视觉调整 | `style` | `:lipstick:` |
| 重构 | `refactor` | `:recycle:` |
| 性能 | `perf` | `:zap:` |
| 测试 | `test` | `:white_check_mark:` |
| 构建 / 依赖 | `build` | `:package:` |
| 配置 / 工具链 / 杂项 | `chore` | `:wrench:` |
| CI | `ci` | `:green_heart:` |
| 关键热修复 | `fix` | `:ambulance:` |
| 安全修复 | `fix` | `:lock:` |
| 破坏性变更 | `feat` | `:boom:` |
| 移除代码或文件 | `refactor` | `:fire:` |
| 移动/重命名资源 | `refactor` | `:truck:` |
| 依赖升级 | `build` | `:arrow_up:` |
| 依赖降级 | `build` | `:arrow_down:` |
| 固定依赖版本 | `build` | `:pushpin:` |
| 添加依赖 | `build` | `:heavy_plus_sign:` |
| 移除依赖 | `build` | `:heavy_minus_sign:` |
| 发布 / 版本标签 | `chore` | `:bookmark:` |
| 进行中 | `chore` | `:construction:` |
| 修复 linter 警告 | `chore` | `:rotating_light:` |
| 添加/更新开发脚本 | `chore` | `:hammer:` |
| 添加/更新 .gitignore | `chore` | `:see_no_evil:` |
| CI 构建系统 | `ci` | `:construction_worker:` |
| 开始一个项目 | `chore` | `:tada:` |

## 范围优先级列表

`auth`、`tasks`、`votes`、`summaries`、`discussions`、`companions`、`users`、`deps`、`eslint`、`build`、`styles`、`api`

## 好的示例

- `:wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突`
- `:package: build(deps): 添加 Swagger 依赖并对齐响应模型`
- `:sparkles: feat(tasks): 添加分页响应 schema`
- `:bug: fix(auth): 校验刷新 token 参数`
- `:recycle: refactor(api): 拆分共享分页 DTO`
- `:lipstick: style(styles): 更新样式方案并统一主题 token`

## 不好的示例

- `更新代码`
- `修复点东西`
- `提交`
- `改了很多`
- `:sparkles: feat: 更新代码`

## 格式

```
:gitmoji: <type>(<scope>): <中文描述>
```

要求：
- 描述使用中文
- 简洁具体，直接描述变更意图
- 优先使用上述优先级列表中的 scope
```

- [ ] **Step 2: 验证格式规则已改为中文**

Run: `grep -n "English" git-batch-commit/references/commit-types.md || echo "OK"`
Expected: 输出 "OK"。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/references/commit-types.md
git commit -m ":memo: docs: translate commit-types reference to Chinese"
```

---

### Task 5: 翻译 `references/grouping-rules.md`

**Files:**
- Modify: `git-batch-commit/references/grouping-rules.md`

- [ ] **Step 1: 将文件完整替换为以下内容**

```markdown
# 分组策略

## 优先作为独立批次的变更

以下类型默认各自作为独立提交：

1. **依赖/锁文件变更**：`package.json`、`package-lock.json`、`pnpm-lock.yaml`、`yarn.lock`
2. **工具链/配置变更**：`eslint.config.js`、`.eslintrc*`、`tsconfig*`、`nest-cli.json`、构建配置
3. **样式系统变更**：tailwind、theme token、全局样式、UI 样式方案迁移
4. **单一功能域变更**：例如 auth、tasks、votes、summaries 各自独立
5. **纯文档变更**：README、`docs/`

## 可以合并的情况

- 依赖变更仅支持某个具体功能变更，且关系非常明确
- controller/service/dto/entity/test 围绕同一功能一起变更
- 配置变更仅支持该功能运行，不是独立的工具链升级

## 应该拆分的情况

即使文件在同一目录下，也要拆分：

- 同时包含“安装依赖”和“新功能”
- 同时包含“lint 修复”和“功能逻辑调整”
- 同时包含“样式调整”和“API 响应结构变更”

## 冲突解决

当同一文件可能属于多个分组时：

1. **高置信度的语义关联**优先于目录位置
2. **独立的工具链变更**保持独立，不要与业务逻辑混合
3. **独立的依赖变更**保持独立，除非能明确证明它只服务于某一个功能
4. 覆盖多个模块的 **Swagger/DTO 新增**应单独成批
5. 独立的 **README/docs** 修订应单独提交

如果仍无法决定：选择更保守的拆分方案，并标记为“低置信度”。

## 识别信号

### A. 文件角色
源码、DTO/schema/类型定义、测试、配置文件、锁文件、样式文件、文档、迁移文件

### B. 变更意图信号
- `package.json` / 锁文件变更 -> 依赖或构建提交
- `eslint`、`prettier`、`tsconfig`、`nest-cli`、`vite`、`webpack`、`babel`、`jest`、`vitest` -> 工具链/配置提交
- `swagger`、`openapi`、`@ApiProperty`、response DTO、pagination DTO -> API 建模/文档提交
- `*.css`、`*.scss`、`tailwind`、`theme`、`token`、`design system` -> 样式提交
- controller/service/dto/entity 一起变更 -> 功能或 bug 修复提交
- `*.spec.*`、`test/`、`__tests__/` -> 测试提交
- `README`、`docs/` -> 文档提交

### C. Diff 语义
根据补丁内容判断：新能力、bug 修复、重命名/清理/重构、样式转换、依赖安装或配置升级、Swagger/响应模型完善、校验规则增强

### D. 关联性
满足以下任一条件的多文件应归为一组：
- Service、controller、DTO 围绕同一 API 变更
- 配置文件变更明显与对应修复文件相关
- 依赖变更与对应代码使用强相关
- pagination DTO、response DTO、Swagger 注解围绕同一 API 文档
```

- [ ] **Step 2: 验证无英文残留**

Run: `grep -nE "Changes That|Cases That|Conflict Resolution|Recognition Signals|File Roles|Change Intent|Diff Semantics|Correlation" git-batch-commit/references/grouping-rules.md || echo "OK"`
Expected: 输出 "OK"。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/references/grouping-rules.md
git commit -m ":memo: docs: translate grouping-rules reference to Chinese"
```

---

### Task 6: 翻译 `references/security.md`

**Files:**
- Modify: `git-batch-commit/references/security.md`

- [ ] **Step 1: 将文件完整替换为以下内容**

```markdown
# 安全与边界

## 敏感文件列表

已暂存变更中出现以下文件时，必须**立即停止**并提示用户手动处理：

- `.env`（及变体 `.env.local`、`.env.production` 等）
- `*.pem`、`*.key`（私钥文件）
- `credentials*.json`
- `id_rsa*`
- `.npmrc`（可能包含 token）
- `secrets.*`
- `*.p12`、*.pfx`（证书）
- `aws_*.json`（AWS 凭证）
- `gcp-*.json`（GCP 凭证）
- `azure-*.json`
- 文件名中包含 `secret`、`private`、`credential` 的任何文件

## 强制规则（绝不）

- **绝不**提交敏感文件
- **绝不**使用 `--no-verify`
- **绝不**使用 `git commit --amend`，除非用户明确要求
- **绝不**使用 `push --force`
- 如果 hook 失败，先分析失败原因，然后修复并创建**新提交**

## 预检项

执行前必须验证：
1. 存在已暂存变更
2. 不存在敏感文件
3. 不存在二进制产物、构建输出、日志文件、缓存文件
4. 不存在同一文件同时处于暂存和未暂存状态（避免工作流意外影响工作树状态）

## 低置信度分组

如果无法 100% 确定分组：先向用户展示计划，**不要直接提交**。
```

- [ ] **Step 2: 验证敏感文件列表完整且为中文**

Run: `grep -n "Sensitive File" git-batch-commit/references/security.md || echo "OK"`
Expected: 输出 "OK"。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/references/security.md
git commit -m ":memo: docs: translate security reference to Chinese"
```

---

### Task 7: 翻译 `scripts/check-staged.py`

**Files:**
- Modify: `git-batch-commit/scripts/check-staged.py`

- [ ] **Step 1: 将所有中文用户可见输出替换为中文（仅修改 print 字符串，不动逻辑）**

具体替换映射：
- `"=== Git Status ==="` -> `"=== Git 状态 ==="`
- `"(no changes)"` -> `"（无变更）"`
- `"=== Staged Files ==="` -> `"=== 已暂存文件 ==="`
- `"(none)"` -> `"（无）"`
- `"=== Staged Diff Stats ==="` -> `"=== 暂存区 diff 统计 ==="`
- `"=== Sensitive File Scan ==="` -> `"=== 敏感文件扫描 ==="`
- `"WARNING: sensitive files found:"` -> `"警告：发现敏感文件："`
- `"Please handle manually before continuing."` -> `"请在继续前手动处理。"`
- `"No sensitive files found."` -> `"未发现敏感文件。"`
- `"=== Binary / Build Artifact Scan ==="` -> `"=== 二进制 / 构建产物扫描 ==="`
- `"WARNING: possible files that should not be committed:"` -> `"警告：以下文件可能不应提交："`
- `"No obvious build artifacts or log files found."` -> `"未发现明显的构建产物或日志文件。"`
- `"=== Staged + Unstaged Same-File Check ==="` -> `"=== 暂存与未暂存同文件检查 ==="`
- `"WARNING: the following files are both staged and unstaged:"` -> `"警告：以下文件同时处于暂存和未暂存状态："`
- `"This workflow may affect working tree state."` -> `"该工作流可能会影响工作树状态。"`
- `"No files are both staged and unstaged."` -> `"没有文件同时处于暂存和未暂存状态。"`
- `"=== Branch Status ==="` -> `"=== 分支状态 ==="`
- `"Current branch: {branch}"` -> `"当前分支：{branch}"`
- `"WARNING: unpushed commits found:"` -> `"警告：发现未推送提交："`
- `"No unpushed commits (or no upstream)."` -> `"无未推送提交（或无上游分支）。"`
- `"=== Check complete ==="` -> `"=== 检查完成 ==="`
- `"  Command failed: {cmd} -> {e}"` -> `"  命令失败：{cmd} -> {e}"`

- [ ] **Step 2: 运行脚本验证输出为中文且功能正常**

Run: `cd git-batch-commit && python3 scripts/check-staged.py`
Expected: 标题显示 "=== Git 状态 ==="、"=== 敏感文件扫描 ===" 等中文，脚本正常结束。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/scripts/check-staged.py
git commit -m ":globe_with_meridians: i18n: translate check-staged.py output to Chinese"
```

---

### Task 8: 翻译 `scripts/batch-commit.py`

**Files:**
- Modify: `git-batch-commit/scripts/batch-commit.py`

- [ ] **Step 1: 将用户可见输出字符串替换为中文（不动逻辑）**

具体替换映射：
- `"Error: manifest file not found: {manifest_file}"` -> `"错误：未找到清单文件：{manifest_file}"`
- `"Please generate a grouping plan first (run the git-batch-commit skill)."` -> `"请先生成分组计划（运行 git-batch-commit skill）。"`
- `">>> Read manifest: {manifest_file}"` -> `">>> 读取清单：{manifest_file}"`
- `">>> Mode: DRY-RUN (preview only, no commits)"` -> `">>> 模式：空运行（仅预览，不提交）"`
- `">>> Current HEAD: {original_head}"` -> `">>> 当前 HEAD：{original_head}"`
- `"Warning: commit {idx} missing message or files, skipping"` -> `"警告：第 {idx} 次提交缺少信息或文件，跳过"`
- `">>> [{idx}/{total}] {msg}"` -> `">>> [{idx}/{total}] {msg}"`（保持不变，msg 本身由 skill 生成）
- `"    File patterns: {', '.join(files)}"` -> `"    文件模式：{', '.join(files)}"`
- `"    Expanded:      {', '.join(expanded)}"` -> `"    展开结果：      {', '.join(expanded)}"`
- `"    [DRY-RUN] git add {' '.join(expanded)}"` -> `"    [空运行] git add {' '.join(expanded)}"`
- `"    [DRY-RUN] git commit -m \"{msg}\""` -> `"    [空运行] git commit -m \"{msg}\""`
- `"    >>> Dry-run: this commit would succeed"` -> `"    >>> 空运行：此次提交可以成功"`
- `"    Staged: {staged or '(none)'}"` -> `"    已暂存：{staged or '（无）'}"`
- `"    >>> Commit succeeded ({commit_hash})"` -> `"    >>> 提交成功 ({commit_hash})"`
- `"    >>> Commit failed: {result.stderr.strip()}"` -> `"    >>> 提交失败：{result.stderr.strip()}"`
- `"\n!!! Rollback mode enabled, resetting to: {original_head}"` -> `"\n!!! 回滚模式已启用，重置到：{original_head}"`
- `"Rolled back {len(successful)} commits"` -> `"已回滚 {len(successful)} 个提交"`
- `"\n!!! Failed on commit {idx}. {len(successful)} commits succeeded and remain on the branch."` -> `"\n!!! 第 {idx} 次提交失败。此前 {len(successful)} 个提交已成功并保留在分支上。"`
- `"  - {m} ({h})"` -> `"  - {m} ({h})"`（保持不变）
- `"\nTo rollback, run: git reset --hard <desired-head>"` -> `"\n如需回滚，请运行：git reset --hard <desired-head>"`
- `"=== Dry-run complete ==="` -> `"=== 空运行完成 ==="`
- `"These are the operations the script would run. No commits were created."` -> `"以下是脚本将要执行的操作。未创建任何提交。"`
- `"Manifest file retained at: {manifest_file}"` -> `"清单文件保留在：{manifest_file}"`
- `"When ready, run: python scripts/batch-commit.py"` -> `"准备好后，请运行：python scripts/batch-commit.py"`
- `"=== Execution complete ==="` -> `"=== 执行完成 ==="`
- `"Success: {len(successful)} commits"` -> `"成功：{len(successful)} 个提交"`
- `"Commit list:"` -> `"提交列表："`
- `"\nManifest file cleaned up."` -> `"\n清单文件已清理。"`

- [ ] **Step 2: 验证脚本仍可正常解析**

Run: `cd git-batch-commit && python3 -m py_compile scripts/batch-commit.py`
Expected: 无报错。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/scripts/batch-commit.py
git commit -m ":globe_with_meridians: i18n: translate batch-commit.py output to Chinese"
```

---

### Task 9: 翻译 `scripts/batch-undo.py`

**Files:**
- Modify: `git-batch-commit/scripts/batch-undo.py`

- [ ] **Step 1: 将用户可见输出字符串替换为中文（不动逻辑）**

具体替换映射：
- `">>> Found manifest file: {manifest_file}"` -> `">>> 找到清单文件：{manifest_file}"`
- `">>> Last batch commit records are available."` -> `">>> 上一批提交记录可用。"`
- `">>> Manifest file not found, attempting to infer from recent commits."` -> `">>> 未找到清单文件，尝试从最近提交推断。"`
- `"\n=== Last 10 commits ==="` -> `"\n=== 最近 10 个提交 ==="`
- `"(no commits)"` -> `"（无提交）"`
- `">>> Enter the number of commits to undo (default 1):"` -> `">>> 请输入要撤销的提交数量（默认 1）："`
- `"Count: "` -> `"数量："`
- `"Invalid input, using default 1"` -> `"输入无效，使用默认值 1"`
- `"\n>>> Will undo {len(commits)} commits (--all mode)"` -> `"\n>>> 将撤销 {len(commits)} 个提交（--all 模式）"`
- `"\n>>> Will undo {len(commits)} commits (interactive mode)"` -> `"\n>>> 将撤销 {len(commits)} 个提交（交互模式）"`
- `"Confirm undo? Type 'yes' to continue: "` -> `"确认撤销？输入 yes 继续："`
- `"Undo canceled."` -> `"撤销已取消。"`
- `">>> Undo [{i}/{len(commits)}]: {msg}"` -> `">>> 撤销 [{i}/{len(commits)}]: {msg}"`
- `"    >>> Undid one commit (soft reset)"` -> `"    >>> 已撤销 1 个提交（软重置）"`
- `"    Files restored to staged state."` -> `"    文件已恢复到暂存状态。"`
- `"\n=== Undo complete ==="` -> `"\n=== 撤销完成 ==="`
- `"Undid {len(commits)} commits. All changes are staged."` -> `"已撤销 {len(commits)} 个提交。所有变更已回到暂存状态。"`
- `"To discard changes completely, run: git reset --hard HEAD~N"` -> `"如需彻底丢弃变更，请运行：git reset --hard HEAD~N"`
- `"Manifest file cleaned up."` -> `"清单文件已清理。"`

- [ ] **Step 2: 验证脚本仍可正常解析**

Run: `cd git-batch-commit && python3 -m py_compile scripts/batch-undo.py`
Expected: 无报错。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/scripts/batch-undo.py
git commit -m ":globe_with_meridians: i18n: translate batch-undo.py output to Chinese"
```

---

### Task 10: 更新 `README.md` 中文部分

**Files:**
- Modify: `git-batch-commit/README.md`

- [ ] **Step 1: 更新中文小节的关键描述与示例**

需要修改的中文部分：

1. 第 14 行：
   - 旧：`自动将暂存的 Git 变更按意图拆分为单元级提交，并生成英文 gitmoji 风格的提交信息。`
   - 新：`自动将暂存的 Git 变更按意图拆分为单元级提交，并生成 gitmoji 风格的中文提交信息。`

2. 第 87-108 行建议计划示例：将提交信息描述改为中文。例如：
   - `:sparkles: feat(api): add response DTOs and Swagger docs` -> `:sparkles: feat(api): 添加响应 DTO 和 Swagger 文档`
   - `:wrench: chore(eslint): update ESLint config and fix rule conflicts` -> `:wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突`
   - `:lipstick: style(styles): refine the style system` -> `:lipstick: style(styles): 细化样式系统`
   - `Choose: A. keep separate  B. merge with another group  C. split  D. cancel` -> `请选择：A. 保持独立  B. 合并到其它分组  C. 拆分  D. 取消`

3. 第 128-130 行执行完成示例：将提交信息描述改为中文：
   - `:sparkles: feat(api): 添加响应 DTO 和 Swagger 文档`
   - `:wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突`
   - `:lipstick: style(styles): 统一主题 token`

- [ ] **Step 2: 验证 README.md 中文部分无“英文”残留**

Run: `grep -n "英文" git-batch-commit/README.md || echo "OK"`
Expected: 输出 "OK"（英文小节本身可能包含 "English"，不影响；此检查针对中文小节）。

- [ ] **Step 3: 提交**

```bash
git add git-batch-commit/README.md
git commit -m ":memo: docs: update README Chinese section for Chinese commit messages"
```

---

### Task 11: 最终验证

**Files:**
- All modified files

- [ ] **Step 1: 全局检查是否还有英文用户提示残留在 SKILL.md 与 references 中**

Run:
```bash
cd git-batch-commit
grep -nE "(I identified|Confirm and I will|Proceed with this plan|Do you want|Completed batch|Undo complete|Current branch|No sensitive|WARNING)" SKILL.md references/*.md || echo "SKILL/ref OK"
```
Expected: 输出 "SKILL/ref OK"。

- [ ] **Step 2: 检查脚本输出字符串**

Run:
```bash
cd git-batch-commit
grep -nE "(Error:|Warning:|Mode:|Current HEAD|Commit succeeded|Commit failed|Dry-run complete|Execution complete|Undo complete|Check complete)" scripts/*.py || echo "scripts OK"
```
Expected: 输出 "scripts OK"（不再包含这些英文输出关键字）。

- [ ] **Step 3: 语法检查所有 Python 脚本**

Run:
```bash
cd git-batch-commit
python3 -m py_compile scripts/*.py
```
Expected: 无报错。

- [ ] **Step 4: 运行 check-staged.py 确认中文输出**

Run: `cd git-batch-commit && python3 scripts/check-staged.py | head -20`
Expected: 输出包含 "Git 状态"、"已暂存文件"、"敏感文件扫描" 等中文标题。

- [ ] **Step 5: 最终提交（如尚未提交）**

如果还有未提交变更：
```bash
git add git-batch-commit/
git commit -m ":globe_with_meridians: i18n: complete Simplified Chinese localization"
```

---

## 自检

- [x] 设计文档 `docs/superpowers/specs/2026-06-13-git-batch-commit-chinese-design.md` 已存在并获用户确认。
- [x] 每个任务对应一个可独立提交的小变更。
- [x] 未改动脚本内部 Git 命令与逻辑。
- [x] 未改动约定式提交类型名与 gitmoji。
- [x] 每个任务包含具体文件路径、修改内容与验证命令。
- [x] 最终验证任务覆盖全文英文残留检查与脚本语法检查。
