---
name: git-batch-commit
description: "自动将暂存的 Git 变更按意图拆分为单元级提交，并生成 gitmoji 风格的提交信息。适用于一次 git add 混入了多种变更类型（eslint/依赖/swagger/dto/样式/业务逻辑）时，希望按意图生成干净、可审查的提交。按意图而非目录分组。跨平台支持 Windows/Linux/macOS。"
license: MIT
---

# Git-Batch-Commit

本技能会分析暂存的 Git 变更，按意图分组，并生成清晰、可审查的提交计划与提交信息。它优先执行安全检查，并在任何提交执行前要求用户明确确认。


铁律：当置信度较低或检测到敏感文件时，永远不要直接提交 —— 先建议，再提交。

## 需避免的反模式

**本节最重要 —— 每次运行前请先阅读。**

- **不要**在未先展示分组计划的情况下盲目提交（除非用户明确说 "立即提交"）
- **不要**将不相关的意图混到一个提交中（例如：依赖 + 业务逻辑放在同一提交）
- **不要**跳过敏感文件检查 —— 发现 `.env`、`*.pem`、`credentials*` 等必须立即停止流程
- **不要**使用 `--no-verify` 或 `git commit --amend`，除非用户明确要求
- **不要**使用 `push --force`
- **不要**提交二进制产物、构建输出或日志文件
- **不要**只按目录分组 —— 按意图分组（同一目录下的配置变更与业务逻辑变更不应是同一提交）
- **不要**跳过未暂存文件检查 —— 如果同一文件同时处于暂存和未暂存状态，必须先警告再继续
- **不要**在未阅读 diff 的情况下猜测意图 —— 在标注分组前先查看 `git diff --cached` 的补丁内容

## 工作流

### 步骤 0：确定模式（必需）

询问：用户请求的是哪种模式？

| 用户输入 | 模式 |
|---|---|
| "整理/拆分/批量处理我暂存的变更"（未说 "立即提交"） | **建议模式**（默认） |
| "拆分并立即提交" / "无需确认" | **执行模式** |
| "仅分组" / "起草提交信息" | **仅建议模式** |
| "预览" / "空运行" / "看看会怎样" | **空运行模式** |

在模式明确之前不要继续。

### 步骤 1：预检（阻塞式）

警告 —— 在分析任何内容之前先运行：

```bash
python3 scripts/check-staged.py
```

该脚本会检查：
- 是否存在暂存文件
- 是否存在敏感文件（`.env`、`*.pem`、`credentials*` 等）
- 是否存在二进制产物或构建输出
- 是否有文件同时处于暂存和未暂存状态
- 分支状态（未推送提交、上游追踪）

**若发现敏感文件 → 停止。告诉用户具体是哪些文件，并请他们手动处理。**

**若没有暂存变更 → 停止。告诉用户暂存区为空。**

**若同一文件同时暂存与未暂存 → 仅进入建议模式并警告用户。**

**若当前分支存在未推送提交：**
- 警告："当前分支有 N 个未推送提交。重置将重写历史，是否继续？"
- 不要自动继续 —— 在进入步骤 5 前必须获得用户确认。

**跨平台：** 脚本支持 Windows / Linux / macOS（需要 Python 3）。

### 步骤 2：分析分组

必需 —— 在标注前先读取实际 diff 内容。

加载 `references/grouping-rules.md` 获取详细分组策略。

针对每个暂存文件询问：

1. **变更意图是什么？**（新功能、bug 修复、配置、依赖、样式、文档）
2. **是否与其他文件相关？**（controller + service + dto = 同一意图）
3. **这是否是高置信度的独立分组？**（eslint 配置、package.json、样式系统 = 是，几乎总是独立）
4. **应与其他文件合并，还是单独成组？**

高置信度独立分组：
- `eslint.config.js`、`.eslintrc*`、`tsconfig*`、`nest-cli.json` -> `chore(eslint)`
- `package.json` + 锁文件（仅依赖变更） -> `build(deps)`
- `tailwind.config.*`、`*.theme.css`、`token*.css` -> `style(styles)`
- `swagger`、`openapi`、`*response.dto.ts`、`*pagination.dto.ts` -> `feat(api)` 或 `build(deps)`
- `*.spec.ts`、`test/**/*.ts` 与对应源码一起 -> 与源文件同意图

分组 scope 优先级：`auth`、`tasks`、`votes`、`summaries`、`discussions`、`companions`、`users`、`api`、`eslint`、`deps`、`build`、`styles`

### 步骤 3：生成提交信息

加载 `references/commit-types.md` 获取 type/gitmoji 映射与格式规则。

每组生成一条提交信息，格式为：`:gitmoji: type(scope): 中文描述`

规则：
- 使用简体中文
- 描述意图，而非改动的文件
- scope 来自上方优先级列表
- 若不确定 scope，使用更宽泛的类别（`api`、`build`）

### 步骤 4：展示计划 + 确认门（必需）

按以下格式展示计划：

```markdown
我识别出 N 个建议提交：

1. `<commit message>`
   - 文件: ...
   - 理由: ...
   - 置信度: high/medium

2. ...

确认后我将按此顺序提交。
```

#### 中等置信度分组 —— 必须在继续前解决

对每个中等置信度分组明确询问用户：

> **关于分组 X（置信度: medium）：**
> 文件: ...
> 理由: ...
>
> 请选择：
> A. 保持为独立提交
> B. 合并到前一个/后一个分组
> C. 拆分到其他分组
> D. 取消该分组（本次不提交）

**在所有中等置信度分组获得明确的用户决议之前，不要进入步骤 5。**

总体确认问题：**是否按此计划继续（所有中等置信度分组已解决），还是需要调整？**

### 步骤 5：执行提交（仅执行模式）

用户确认且所有中等置信度分组已解决后：

**5a. 重新验证暂存状态** —— 运行 `git diff --cached --name-only`，确认自步骤 1 以来没有新增变更。

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

将该文件写入仓库根目录。

**5c. 提交前提供空运行预览：**

询问：**"执行前是否需要空运行预览？"**

如果需要：

```bash
python3 scripts/batch-commit.py --dry-run
```

空运行展示：
- 每次提交的具体文件列表（glob 展开后）
- 将要运行的 git 命令
- 清单文件保留，供后续执行或调整

**5d. 执行：**

```bash
# 默认：失败时停止，不回滚
python3 scripts/batch-commit.py

# 可选：失败时自动回滚所有已成功提交
python3 scripts/batch-commit.py --rollback-on-fail
```

**回滚行为：**
- 任何提交前，先保存当前 HEAD
- 若某次提交失败，提示是否回滚
- 使用 `--rollback-on-fail`：自动回滚到保存的 HEAD
- 成功提交不会自动回滚 —— 需由用户选择

**若某次提交失败：**
- 停止后续提交
- 报告哪次提交失败及原因
- 报告失败前有多少次提交成功
- 询问："是否回滚已成功提交？"

### Hook 失败处理策略

当 `git commit` 返回非零且 stderr 包含 hook 关键词时：

| stderr 关键词 | 可能原因 | 处理方式 |
|---|---|---|
| `pre-commit` | lint/format 检查失败 | 说明哪条规则失败及如何修复，然后重新运行 |
| `commit-msg` | 提交信息格式无效 | 展示所需格式，生成修正后的信息，重新提交 |
| `post-commit` | 非关键 hook 失败 | 警告用户：提交已成功，但 post-hook 失败 |
| `lint` / `eslint` / `prettier` | 代码检查失败 | 列出失败的文件与规则，建议修复命令 |

**处理流程：**

1. 解析 stderr 并识别 hook 类型
2. 若是 `commit-msg`：生成修正后的信息，请用户确认，重新提交
3. 若是 `pre-commit`（lint/format）：说明失败原因与修复命令，不要自动回滚
4. 若是 `post-commit`：提交已成功，仅警告用户
5. 若无法识别：停止并报告错误文本，请用户手动处理

**禁止：**
- 不要使用 `--no-verify` 绕过 hook
- 不要未分析原因就回滚

### 步骤 6：总结

执行完成后（或在建议模式下展示计划后）：
- 创建了多少个提交
- 每条提交信息 + 短 hash
- 剩余暂存/未暂存文件及未包含原因

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
（基于变更文件给出：DTO 更新 -> 验证 API 响应格式；ESLint 变更 -> 运行 lint）
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
- 按约定类型分组：`Features`、`Bug Fixes`、`Chores`、`Refactors`、`Docs`
- 为可读性移除提交信息中的 gitmoji 与 scope
- 使用 `### [Unreleased]` 章节或追加当日日期
- 标题：使用最重要的提交信息（优先 `feat` > `fix` > 其他）
- 描述：按类型列出所有提交信息
- 添加基于变更文件的"测试建议"（非通用建议）

### 撤销上一批次

如果用户在批量提交后说 "撤销上一批次" / "撤销"：

询问：**"要撤销多少个提交？"**（默认为上一批次全部）

```bash
python3 scripts/batch-undo.py
```

脚本行为：
- 展示上一批次的提交（来自清单）或询问数量
- 使用 `git reset --soft HEAD~N` 撤销（文件回到暂存状态，不会丢失）
- 清理清单文件
- 默认交互式确认；使用 `--all` 跳过确认

**不要使用 `git reset --hard` 撤销 —— 这会丢弃变更。**

## 输出模板

### 建议模式输出
```markdown
我识别出 N 个建议提交：

1. `<msg>`
   - 文件: ...
   - 理由: ...
   - 置信度: high/medium

2. ...

确认后我将按此顺序提交。
```

### 执行模式输出
```markdown
批量提交完成。已创建 N 个提交：

1. `<msg1>` (abc1234)
2. `<msg2>` (def5678)

如需，我可以：
- 检查剩余暂存/未暂存变更
- 生成 PR 摘要 / 标题
```
