# git-batch-commit Skill 汉化设计

## 背景

中文用户调用 `git-batch-commit` skill 时发现：
1. agent 全程以英语交互；
2. 生成的 commit message 描述部分也是英语。

本设计将 skill 的主要语言更替为中文简体，同时保留约定式提交的类型与 gitmoji。

## 目标

- 用户与 skill 交互时，agent 使用中文简体回复。
- 生成的 commit message 格式为：`:gitmoji: type(scope): 中文描述`。
- 脚本运行时面向用户的输出改为中文。
- 所有参考文档改为中文简体。

## 非目标

- 不改动约定式提交类型名（`feat`、`fix`、`chore` 等）。
- 不改动 gitmoji 表情符号。
- 不改动脚本内部逻辑、Git 命令、文件路径与 glob 模式。
- 不改动安全边界与钩子处理逻辑。

## 方案

采用**全用户界面汉化**方案：翻译所有用户可见内容，保持底层行为不变。

## 改动清单

### 1. `SKILL.md`

- 更新 `description`，移除 "in English"，声明本 skill 以中文简体交互。
- 翻译所有工作流步骤、门控问题、输出模板。
- Step 3 明确生成格式：`:gitmoji: type(scope): 中文描述`。
- 所有示例提交信息改为中文描述。

### 2. `references/commit-types.md`

- 保留类型名与 gitmoji 不变。
- 格式规则改为“描述使用中文”。
- 示例改为中文描述。

### 3. `references/grouping-rules.md`

- 全篇翻译为中文简体。

### 4. `references/security.md`

- 全篇翻译为中文简体。

### 5. `scripts/*.py`

- `batch-commit.py`、`batch-undo.py`、`check-staged.py` 中所有用户可见的输出提示改为中文。
- 脚本内部逻辑、命令调用保持不变。

### 6. `README.md`

- 中文部分更新：移除“生成英文 gitmoji 风格提交信息”的描述。
- 典型工作流示例中的提交信息改为中文描述。
- 英文部分保留，作为双语文档。

## 预期效果

调用 skill 后，agent 用中文交互并生成如下提交信息：

```text
:sparkles: feat(api): 添加响应 DTO 和 Swagger 文档
:wrench: chore(eslint): 更新 ESLint 配置并修复规则冲突
```

脚本输出示例：

```text
=== 暂存区检查 ===
未发现敏感文件。
=== 检查完成 ===
```

## 验证方式

1. 通读所有改动文件，确认无遗漏的英文用户提示。
2. 检查提交信息示例符合 `:gitmoji: type(scope): 中文描述` 格式。
3. 运行脚本，确认输出为中文。
