# 分组策略

## 优先作为独立批次提取的变更

以下类型默认作为独立提交：

1. **依赖 / 锁文件变更**：`package.json`、`package-lock.json`、`pnpm-lock.yaml`、`yarn.lock`
2. **工具链 / 配置变更**：`eslint.config.js`、`.eslintrc*`、`tsconfig*`、`nest-cli.json`、构建配置
3. **样式系统变更**：tailwind、主题 token、全局样式、UI 样式方案迁移
4. **单一功能领域变更**：例如 auth、tasks、votes、summaries 各自独立
5. **纯文档变更**：README、`docs/`

## 可以合并的情况

- 某项依赖变更仅服务于某个明确的新功能，且关系非常清晰
- controller/service/dto/entity/test 围绕同一功能一起变更
- 配置变更仅服务于该功能的运行，而非独立的工具链升级

## 应该拆分的情况

即使文件位于同一目录，也应拆分：

- 同时包含"依赖安装"和"新功能"
- 同时包含"lint 修复"和"功能逻辑调整"
- 同时包含"样式调整"和"API 响应结构变更"

## 冲突解决

当同一文件可能属于多个分组时：

1. **高置信度的语义关联**优先于目录位置
2. **独立的工具链变更**是独立的，不要与业务逻辑混合
3. **独立的依赖变更**是独立的，除非能证明仅服务于某一个功能
4. **Swagger/DTO 新增**覆盖多个模块时应作为独立批次
5. **README/docs** 若为独立的文档修订，应作为独立提交

如果仍然无法决定：选择更保守的拆分方案，并标记为"low confidence"。

## 识别信号

### A. 文件角色
源码、DTO/schema/类型定义、测试、配置文件、锁文件、样式文件、文档、迁移文件

### B. 变更意图信号
- `package.json` / 锁文件变更 → 依赖或构建提交
- `eslint`、`prettier`、`tsconfig`、`nest-cli`、`vite`、`webpack`、`babel`、`jest`、`vitest` → 工具链/配置提交
- `swagger`、`openapi`、`@ApiProperty`、response DTO、pagination DTO → API 建模/文档提交
- `*.css`、`*.scss`、`tailwind`、`theme`、`token`、`design system` → 样式提交
- controller/service/dto/entity 同时变更 → 功能或 bugfix 提交
- `*.spec.*`、`test/`、`__tests__/` → 测试提交
- `README`、`docs/` → 文档提交

### C. Diff 语义
从补丁内容判断：新增能力、bug 修复、重命名/清理/重构、样式改造、依赖安装或配置升级、Swagger/响应模型补全、校验规则增强

### D. 关联性
满足以下任一条件的多文件应归为一组：
- Service、controller、DTO 围绕同一 API 变更
- 配置文件变更与对应修复文件明显相关
- 依赖变更与对应代码使用强相关
- pagination DTO、response DTO、Swagger 注解围绕同一 API 文档
