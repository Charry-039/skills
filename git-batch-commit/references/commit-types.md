# Commit Types & Gitmoji Mapping

Priority mapping:

| Scenario | Conventional Type | Gitmoji |
|----------|-------------------|---------|
| New feature | `feat` | `:sparkles:` |
| Bug fix | `fix` | `:bug:` |
| Documentation | `docs` | `:memo:` |
| Style / visual tweaks | `style` | `:lipstick:` |
| Refactor | `refactor` | `:recycle:` |
| Performance | `perf` | `:zap:` |
| Test | `test` | `:white_check_mark:` |
| Build / dependencies | `build` | `:package:` |
| Config / toolchain / chores | `chore` | `:wrench:` |
| CI | `ci` | `:green_heart:` |
| Critical hotfix | `fix` | `:ambulance:` |
| Security fix | `fix` | `:lock:` |
| Breaking change | `feat` | `:boom:` |
| Remove code or files | `refactor` | `:fire:` |
| Move/rename resources | `refactor` | `:truck:` |
| Dependency upgrade | `build` | `:arrow_up:` |
| Dependency downgrade | `build` | `:arrow_down:` |
| Pin dependency versions | `build` | `:pushpin:` |
| Add dependency | `build` | `:heavy_plus_sign:` |
| Remove dependency | `build` | `:heavy_minus_sign:` |
| Release / version tag | `chore` | `:bookmark:` |
| WIP | `chore` | `:construction:` |
| Fix linter warnings | `chore` | `:rotating_light:` |
| Add/update dev scripts | `chore` | `:hammer:` |
| Add/update .gitignore | `chore` | `:see_no_evil:` |
| CI build system | `ci` | `:construction_worker:` |
| Begin a project | `chore` | `:tada:` |

## Scope Priority List

`auth`, `tasks`, `votes`, `summaries`, `discussions`, `companions`, `users`, `deps`, `eslint`, `build`, `styles`, `api`

## Good Examples

- `:wrench: chore(eslint): update ESLint config and fix rule conflicts`
- `:package: build(deps): add Swagger dependency and align response models`
- `:sparkles: feat(tasks): add paginated response schema`
- `:bug: fix(auth): validate refresh token params`
- `:recycle: refactor(api): split shared pagination DTO`
- `:lipstick: style(styles): update style scheme and unify theme tokens`

## Bad Examples

- `update code`
- `fix stuff`
- `commit`
- `changed a lot`
- `:sparkles: feat: update code`

## Format

```
:gitmoji: <type>(<scope>): <English description>
```

Requirements:
- Use English for description
- Be concise and specific, describe the change intent directly
- Prefer scope from the priority list above