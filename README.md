<p align="center">
  <a href="#english">English</a> | <a href="#chinese">中文</a>
</p>

---
<a name="english"></a>

# skills

A collection of production-grade agent skills for Claude Code and other AI agent terminals.

<p align="center">
  <img src="https://img.shields.io/badge/Skills-1-blue" alt="1 Skill" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License" />
</p>

## Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [**Git Batch Commit**](./git-batch-commit/) | Automatically organize staged Git changes into unit-level, intent-based commits with gitmoji-style messages in English. | `npx skills add <owner>/<repo> --path git-batch-commit` |

## Quick Start

Install any skill with:

```bash
npx skills add Charry-039/skills --path <skill-path>
```

Then invoke in your agent terminal:

```bash
/git-batch-commit    # Organize staged changes into intent-based commits
```

## License

MIT



<a name="chinese"></a>

# skills

面向 Claude Code 与其他 AI 代理终端的生产级技能集合。

<p align="center">
  <img src="https://img.shields.io/badge/Skills-1-blue" alt="1 Skill" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License" />
</p>

## 技能

| Skill | Description | Install |
|-------|-------------|---------|
| [**Git Batch Commit**](./git-batch-commit/) | 自动将暂存的 Git 变更按意图拆分为单元级提交，并生成英文 gitmoji 风格提交信息。 | `npx skills add <owner>/<repo> --path git-batch-commit` |

## 快速开始

安装任意技能：

```bash
npx skills add Charry-039/skills --path <skill-path>
```

然后在你的代理终端中调用：

```bash
/git-batch-commit    # 将暂存变更按意图拆分提交
```

## 许可证

MIT