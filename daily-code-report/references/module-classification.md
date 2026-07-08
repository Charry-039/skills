# 模块分类指南

## 分类原则

按**业务/功能领域**聚合 commit，不按文件类型或 commit 顺序罗列。

### 判断问题

对每条 commit 问自己：

1. 如果向非技术人员一句话说明这条改动，会提到哪个业务模块？
2. 修改的文件路径中是否反复出现某个目录名？（如 `src/auth/`、`services/order/`）
3. 多条 commit 的 message 是否围绕同一主题？如是，归为同一模块。

## 常见模块示例

| 路径/关键词 | 建议模块名 |
|------------|-----------|
| `auth`, `login`, `logout`, `session`, `token`, `password` | 认证模块 |
| `user`, `profile`, `account` | 用户模块 |
| `order`, `cart`, `checkout`, `payment` | 订单模块 |
| `product`, `goods`, `sku`, `inventory` | 商品模块 |
| `notification`, `message`, `email`, `sms`, `push` | 消息通知模块 |
| `report`, `dashboard`, `chart`, `statistics` | 数据报表模块 |
| `api`, `endpoint`, `controller`, `route` | 接口层 |
| `test`, `spec`, `__tests__`, `*.test.*` | 测试相关（可分散到对应模块或单列） |
| `config`, `ci`, `docker`, `deploy`, `github` | 工程配置（单列"工程配置"或不纳入日报） |
| `doc`, `docs`, `README`, `CHANGELOG` | 文档（单列"文档"或不纳入日报） |

## 合并规则

- 同一模块的多条 commit 合并为一段描述，不逐条列出。
- 若同一模块既有功能修改又有测试补充，可合并为一句话：
  - "完成登录重试限制，补充异常提示与单元测试。"
- 若 commit 涉及两个模块且难以归属，选择主要影响模块，或用"跨模块"说明。

## 忽略项

以下类型通常不纳入"功能模块"日报，可单列"其他"或忽略：

- 纯文档更新
- CI/CD 配置调整
- 依赖版本升级（无业务功能变化）
- 代码格式化、lint 修复（无逻辑变化）
- 会议记录、日常事务
