# 🚨 Token 问题？从这里开始！

## 问题：所有 API 调用都失败了

**不要慌！** 这通常是 token 过期导致的，很容易修复。

---

## 🔧 立即修复（3 步）

### 步骤 1: 运行诊断

**Windows 用户**:

```bash
双击运行: QUICK_FIX_API.bat
```

**Mac/Linux 用户**:

```bash
python test_api_connection.py
```

---

### 步骤 2: 查看输出

#### ✅ 如果看到 "✓ 获取 token 成功"

恭喜！Token 没问题，继续步骤 3。

#### ❌ 如果看到 "✗ 获取 token 失败"

需要检查 AppId 和 AppKey：

1. 打开 `.env` 文件
2. 确认这两行正确：
   ```
   AppId=e916a637eb6a4dfd9722d0baeab8807a
   AppKey=6856917787b74fc983fc0da56f41e27b
   ```
3. 登录 https://aimiai.com/console 确认凭证

#### ⚠️ 如果看到 "Token 已过期"

删除旧 token：

1. 打开 `.env` 文件
2. 找到这一行：
   ```
   token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
3. 删除或注释掉（在前面加 #）：
   ```
   # token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. 保存文件
5. 重新运行步骤 1

---

### 步骤 3: 验证修复

```bash
python test_bearer_auth.py
```

如果看到 "✓ Bearer token authentication working!"，说明修复成功！

---

## 🎯 现在可以运行分析了

### 选项 1: 最近 2 周热点分析（推荐）

```bash
# Windows
双击: RUN_2WEEKS_ANALYSIS.bat

# 或命令行
python analyze_recent_2weeks.py
```

### 选项 2: 突破股票筛选（4 大标准）

```bash
# Windows
双击: RUN_BREAKOUT_FINDER.bat

# 或命令行
python find_breakout_stocks.py
```

### 选项 3: Shannon 历史模式

```bash
python find_shannon_pattern.py
```

---

## 📊 可用的工具

| 工具              | 用途         | 命令                              |
| ----------------- | ------------ | --------------------------------- |
| **最近 2 周分析** | 发现当前热点 | `python analyze_recent_2weeks.py` |
| **突破股票筛选**  | 4 大严格标准 | `python find_breakout_stocks.py`  |
| **Shannon 模式**  | 历史突破模式 | `python find_shannon_pattern.py`  |
| **新闻分析**      | 美股新闻情绪 | `python analyze_with_news.py`     |

---

## 🔍 还是不行？

### 运行详细诊断

```bash
python diagnose_api.py
```

这会检查：

- ✅ 环境变量
- ✅ Token 有效性
- ✅ API 端点
- ✅ 网络连接
- ✅ 认证格式

---

## 📚 详细文档

- `FIX_TOKEN_ISSUE.md` - Token 问题修复指南
- `API_TROUBLESHOOTING.md` - 完整故障排除
- `BEARER_AUTH_UPDATE.md` - API 认证说明

---

## 🆘 常见问题

### Q: Token 多久过期？

A: 通常 24 小时。系统会自动刷新。

### Q: 如何手动刷新 token？

A: 删除 `.env` 中的 token 行，系统会自动获取新的。

### Q: AppId 和 AppKey 在哪里？

A: 登录 https://aimiai.com/console，查看 API Keys 页面。

### Q: 为什么一直失败？

A: 可能原因：

1. AppId/AppKey 不正确
2. 账号没有 API 权限
3. 网络连接问题
4. API 端点不正确

---

## 💡 快速提示

```bash
# 测试 API 连接
python test_api_connection.py

# 测试 Bearer 认证
python test_bearer_auth.py

# 快速测试（1只股票）
python test_2weeks_quick.py

# 完整分析（50+只股票）
python analyze_recent_2weeks.py
```

---

## ✅ 检查清单

修复前请确认：

- [ ] `.env` 文件存在
- [ ] AppId 和 AppKey 正确
- [ ] 网络连接正常
- [ ] 可以访问 aimiai.com
- [ ] 账号有 API 权限

---

## 🚀 立即开始

```bash
# 1. 修复 token
python test_api_connection.py

# 2. 验证修复
python test_bearer_auth.py

# 3. 运行分析
python analyze_recent_2weeks.py
```

---

**遇到问题？**

1. 运行 `QUICK_FIX_API.bat`
2. 查看 `FIX_TOKEN_ISSUE.md`
3. 运行 `python diagnose_api.py`

**一切正常？**

开始分析：`python analyze_recent_2weeks.py` 🚀
