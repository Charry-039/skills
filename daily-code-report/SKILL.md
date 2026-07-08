---
name: daily-code-report
description: "基于本地 Git commit history 生成软件开发工作日报。当用户说'写日报'、'今天做了什么'、'生成工作日报'、'下班总结'、'今日代码总结'、'git 日报'、'daily report'、'work summary'、'what did I do today'、'code report' 时触发。Actions: summarize, generate, write, report, review, analyze commits, daily standup, work log. 按功能模块聚合当日代码提交，每条不超过 100 字，文风严谨简短，不过度使用技术名词。"
argument-hint: "[--date YYYY-MM-DD] [--author NAME] [--repo PATH] [--style formal|concise] [--quick]"
---

# Daily Code Report

IRON LAW: 不读取本地 git commit history 就不生成日报；禁止凭空捏造或推测未提交的工作内容。

Red Flags（回到 Step 2 重新获取 commits）：
- 当前目录不是 git 仓库且用户未指定 `--repo`
- 指定日期范围内零条 commit 却强行"补充"内容
- 输出里出现未在 commit 中出现过的功能模块

## Workflow

Copy this checklist and check off items as you complete them:

```
Daily Code Report Progress:

- [ ] Step 1: 解析参数与范围 ⚠️ REQUIRED
  - [ ] 1.1 读取 $ARGUMENTS
  - [ ] 1.2 确定日期范围（默认今天 00:00–23:59）
  - [ ] 1.3 确定作者（默认当前 git user）
  - [ ] 1.4 确定仓库路径（默认当前工作目录）
- [ ] Step 2: 获取 git commit history ⛔ BLOCKING
- [ ] Step 3: 分析并分类功能模块
- [ ] Step 4: 生成日报草稿
- [ ] Step 5: 用户确认 ⚠️ REQUIRED (unless --quick)
- [ ] Step 6: 输出最终日报
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--date YYYY-MM-DD` | 要总结的日期 | 今天 |
| `--author NAME` | 要筛选的提交作者 | 当前 git user.name |
| `--repo PATH` | 目标仓库路径 | 当前工作目录 |
| `--style formal\|concise` | 文风：`formal` 正式；`concise` 极简 | `formal` |
| `--quick` | 跳过确认门，直接输出 | false |

## Step 1: 解析参数与范围 ⚠️ REQUIRED

读取 `$ARGUMENTS` 并解析：

1. `--date`：提取 `YYYY-MM-DD`。未提供则使用当前系统日期。
2. `--author`：提取作者名。未提供则运行 `git config user.name` 获取。
3. `--repo`：提取绝对路径。未提供则使用当前工作目录。
4. `--style`：仅允许 `formal` 或 `concise`。
5. `--quick`：布尔标志，存在即跳过 Step 5 确认门。

Ask: 用户是否明确指定了日期/作者/仓库？未指定的默认值是否合理？

## Step 2: 获取 git commit history ⛔ BLOCKING

运行脚本：

```bash
python3 scripts/get_commits.py --repo <PATH> --since <YYYY-MM-DDT00:00:00> --until <YYYY-MM-DDT23:59:59> --author <NAME>
```

输出为 JSON 数组：

```json
[
  {
    "hash": "abc1234",
    "date": "2026-07-08T14:32:00",
    "author": "charry",
    "message": "feat(auth): add login retry limit",
    "files": ["src/auth/login.ts", "src/auth/guard.ts"]
  }
]
```

⛔ 如果脚本返回空数组：
- 先检查 `--date`、`--author`、`--repo` 是否正确
- 向用户报告"该范围内无提交"，并询问是否切换日期/作者/仓库
- **禁止** 编造内容填补

## Step 3: 分析并分类功能模块

Load `references/module-classification.md` 获取模块分类规则。

对每条 commit 问自己：

1. 该 commit 主要修改了哪个业务/功能领域？
2. 修改的文件路径暗示了哪个模块？（如 `src/auth/` → 认证模块）
3. 多条 commit 是否属于同一模块？如是，合并描述。
4. 该 commit 是否主要涉及非代码工作（会议、文档、配置环境）？如是，单独标注或忽略。

分类原则：
- 按**业务模块**聚合，不按 commit 逐条罗列
- 每个模块用一段自然语言描述，避免枚举文件名和方法名
- 技术名词只保留对理解工作必要的部分

## Step 4: 生成日报草稿

Load `references/report-template.md` 获取输出模板。
Load `references/examples.md` 获取风格示例。

输出结构：

```markdown
## 工作日报 — 2026-07-08

**作者：** charry
**日期：** 2026-07-08

### 功能模块

1. **认证模块**：完成登录重试限制逻辑，补充异常提示与单元测试，提升账户安全性。
2. **订单模块**：优化订单列表查询性能，调整分页参数与缓存策略。

### 其他

- 无
```

约束：
- 每个模块描述 **≤ 100 字**（含标点）
- `--style concise` 时每个模块描述 **≤ 50 字**
- 不列出具体文件名、方法名、类名，除非它是理解工作的关键
- 不添加"计划明天做…"等未在 commit 中体现的内容

## Step 5: 用户确认 ⚠️ REQUIRED

If `--quick`：跳过本步骤，直接输出。

否则，呈现草稿并询问用户：

- 直接输出最终日报？
- 需要调整某个模块的描述？
- 发现遗漏或想补充内容？
- 只查看，不输出？

⚠️ 未取得用户确认前，不要输出最终日报。

## Step 6: 输出最终日报

按 Step 4 模板输出，确保：

- 标题、作者、日期完整
- 模块按业务重要性排序，或按时间顺序排序（保持一致）
- 无多余解释、无"以下是您的日报"等寒暄

## Anti-Patterns

- 不读取 git log，直接根据"常见开发工作"编造日报
- 按 commit 逐条罗列，而不是按功能模块聚合
- 描述中堆砌技术名词（具体方法名、文件名、框架版本）
- 单个模块描述超过 100 字
- 把非代码工作（会议记录、文档整理、环境配置）混入"功能模块"
- 添加未在 commit 中出现的"明天计划"或"待办事项"
- 对空 commit 列表仍生成看似充实的日报

## Pre-Delivery Checklist

- [ ] 日报内容完全基于实际 git commit history
- [ ] 每个功能模块描述 ≤ 100 字（concise 模式 ≤ 50 字）
- [ ] 未捏造、未推测、未添加未提交的工作
- [ ] 文风严谨简短，不过度技术化
- [ ] 输出包含日期与作者
- [ ] 无 TODO / FIXME / 占位符
- [ ] 所有 workflow checklist 项已勾选
