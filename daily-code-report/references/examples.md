# 输出示例

## Good Example

输入 commits：

- `feat(auth): add login retry limit`
- `test(auth): add retry limit unit tests`
- `fix(auth): correct error message on max retry`
- `refactor(order): optimize list query with cache`
- `docs: update API documentation`

输出（formal）：

```markdown
## 工作日报 — 2026-07-08

**作者：** charry
**日期：** 2026-07-08

### 功能模块

1. **认证模块**：完成登录重试限制功能，补充相关单元测试并修正超限提示文案，提升账户安全性。
2. **订单模块**：优化订单列表查询性能，引入缓存策略减少重复读取。

### 其他

- 更新接口文档。
```

输出（concise）：

```markdown
## 日报 — 2026-07-08

**作者：** charry

- 认证模块：完成登录重试限制并补充测试。
- 订单模块：优化列表查询并加入缓存。
```

## Bad Examples

### 错误 1：按 commit 逐条罗列

```markdown
1. feat(auth): add login retry limit
2. test(auth): add retry limit unit tests
3. fix(auth): correct error message on max retry
```

问题：未按模块聚合，像 commit log 摘要，不像日报。

### 错误 2：过度技术化

```markdown
1. **认证模块**：在 `LoginController.authenticate()` 中新增 `retryCounter` 字段，修改 `RedisTokenStore` 的 `incr()` 调用，更新 `AuthErrorCode.MAX_RETRY_EXCEEDED` 枚举值，并在 `login.test.ts` 第 42 行添加测试用例。
```

问题：堆砌方法名、文件名、行号，超出 100 字，阅读负担重。

### 错误 3：凭空补充未提交内容

```markdown
### 明日计划

- 继续优化订单模块缓存失效策略。
```

问题：日报应仅基于已提交的工作，禁止添加未在 commit 中体现的计划。

### 错误 4：空 commit 仍生成长篇日报

当指定日期无 commit 时：

```markdown
## 工作日报 — 2026-07-08

今日主要进行了代码审查与需求沟通，为后续开发做准备。
```

问题：无 git commit 支撑，属于捏造内容。正确做法是报告"该范围内无提交"。
