# Grouping Strategy

## Changes That Priority Independent Batches

The following types default to independent commits:

1. **Dependency/lockfile changes**: `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`
2. **Toolchain/config changes**: `eslint.config.js`, `.eslintrc*`, `tsconfig*`, `nest-cli.json`, build configs
3. **Style system changes**: tailwind, theme tokens, global styles, UI style scheme migration
4. **Single functional domain changes**: e.g., auth, tasks, votes, summaries each independently
5. **Pure documentation changes**: README, docs/

## Cases That Can Be Merged

- A dependency change only supports a specific feature change and is very clear
- controller/service/dto/entity/test change together around the same feature
- Config change only supports that feature's operation, not independent toolchain upgrade

## Cases That Should Be Split

Even if files are in the same directory, split:

- Contains both "dependency install" and "new feature"
- Contains both "lint fix" and "feature logic adjustment"
- Contains both "style adjustment" and "API response structure change"

## Conflict Resolution

When the same file could belong to multiple groups:

1. **High-confidence semantic association** takes priority over directory location
2. **Independent toolchain changes** are independent, don't mix with business logic
3. **Independent dependency changes** are independent, unless proven to serve only one feature
4. **Swagger/DTO additions** covering multiple modules should be separate batch
5. **README/docs** if independent documentation revision, should be separate commit

If still undecided: choose the more conservative splitting scheme, mark as "low confidence".

## Recognition Signals

### A. File Roles
Source code, DTO/schema/type definitions, tests, config files, lockfiles, style files, docs, migration files

### B. Change Intent Signals
- `package.json` / lockfile changes → dependency or build commit
- `eslint`, `prettier`, `tsconfig`, `nest-cli`, `vite`, `webpack`, `babel`, `jest`, `vitest` → toolchain/config commit
- `swagger`, `openapi`, `@ApiProperty`, response DTO, pagination DTO → API modeling/docs commit
- `*.css`, `*.scss`, `tailwind`, `theme`, `token`, `design system` → style commit
- controller/service/dto/entity changing together → feature or bugfix commit
- `*.spec.*`, `test/`, `__tests__/` → test commit
- `README`, `docs/` → documentation commit

### C. Diff Semantics
Judge from patch content: new capability, bug fix, rename/cleanup/refactor, style transformation, dependency install or config upgrade, Swagger/response model completion, validation rule enhancement

### D. Correlation
Multiple files meeting any of the following should be grouped:
- Service, controller, DTO changing around the same API
- A config file change is clearly related to corresponding fix files
- Dependency change is strongly correlated with corresponding code usage
- Pagination DTO, response DTO, Swagger annotations around the same API documentation