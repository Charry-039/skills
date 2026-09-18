# Commit Types

Priority mapping:

| Scenario | Conventional Type |
|----------|-------------------|
| New feature | `feat` |
| Bug fix | `fix` |
| Documentation | `docs` |
| Style / visual tweaks | `style` |
| Refactor | `refactor` |
| Performance | `perf` |
| Test | `test` |
| Build / dependencies | `build` |
| Config / toolchain / chores | `chore` |
| CI | `ci` |
| Critical hotfix | `fix` |
| Security fix | `fix` |
| Breaking change | `feat` |
| Remove code or files | `refactor` |
| Move/rename resources | `refactor` |
| Dependency upgrade | `build` |
| Dependency downgrade | `build` |
| Pin dependency versions | `build` |
| Add dependency | `build` |
| Remove dependency | `build` |
| Release / version tag | `chore` |
| WIP | `chore` |
| Fix linter warnings | `chore` |
| Add/update dev scripts | `chore` |
| Add/update .gitignore | `chore` |
| CI build system | `ci` |
| Begin a project | `chore` |

## Scope Priority List

`auth`, `tasks`, `votes`, `summaries`, `discussions`, `companions`, `users`, `deps`, `eslint`, `build`, `styles`, `api`

## Good Examples

- `chore(eslint): update ESLint config and fix rule conflicts`
- `build(deps): add Swagger dependency and align response models`
- `feat(tasks): add paginated response schema`
- `fix(auth): validate refresh token params`
- `refactor(api): split shared pagination DTO`
- `style(styles): update style scheme and unify theme tokens`

## Bad Examples

- `update code`
- `fix stuff`
- `commit`
- `changed a lot`
- `feat: update code`

## Format

```
<type>(<scope>): <中文描述>
```

Requirements:
- 描述使用简体中文
- 简洁具体，直接说明变更意图
- 优先使用上方 Scope 优先级列表中的 scope
