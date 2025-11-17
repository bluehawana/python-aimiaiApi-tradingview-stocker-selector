# 🔧 Token 问题快速修复指南

## ❌ 问题：所有 API 调用都失败

可能的原因：

1. Token 已过期
2. API 端点不正确
3. 认证格式错误
4. 网络连接问题

---

## ✅ 快速修复步骤

### 方法 1: 一键诊断（推荐）

```bash
# Windows 用户 - 双击运行
QUICK_FIX_API.bat

# 或命令行
python test_api_connection.py
```

---

### 方法 2: 手动修复 Token

#### 步骤 1: 删除旧 Token

编辑 `.env` 文件，找到这一行：

```bash
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**删除或注释掉**：

```bash
# token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 步骤 2: 重新测试

```bash
python test_bearer_auth.py
```

系统会自动获取新 token。

---

### 方法 3: 手动获取新 Token

```bash
python -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app_id = os.getenv('AppId')
app_key = os.getenv('AppKey')

response = requests.post(
    'https://aimiai.com/api/token/get',
    json={'appId': app_id, 'appKey': app_key}
)

print('Status:', response.status_code)
print('Response:', response.json())

if response.status_code == 200:
    result = response.json()
    token = result.get('data') or result.get('token')
    if token:
        print('\n新 Token:')
        print(token)
        print('\n请将此 token 更新到 .env 文件中')
"
```

---

## 🔍 详细诊断

如果快速修复无效，运行详细诊断：

```bash
python diagnose_api.py
```

这会检查：

- ✅ 环境变量配置
- ✅ Token 有效性
- ✅ API 端点连接
- ✅ 认证格式
- ✅ 网络连接

---

## 📋 检查清单

在继续之前，请确认：

### 1. .env 文件配置正确

```bash
# 必需
AppId=e916a637eb6a4dfd9722d0baeab8807a
AppKey=6856917787b74fc983fc0da56f41e27b

# 可选（如果过期就删除）
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. AppId 和 AppKey 有效

- 登录 https://aimiai.com/console
- 检查 API Keys 页面
- 确认凭证正确

### 3. 网络连接正常

```bash
# 测试连接
ping aimiai.com

# 或访问
https://aimiai.com
```

### 4. 账号有 API 权限

- 检查账号状态
- 确认未欠费
- 确认有 API 调用权限

---

## 🆘 常见错误和解决方案

### 错误 1: "Token expired"

**解决方案**:

```bash
# 删除 .env 中的 token 行
# 重新运行程序，系统会自动获取新 token
```

---

### 错误 2: "Invalid credentials"

**解决方案**:

1. 检查 AppId 和 AppKey 是否正确
2. 登录 aimiai.com 控制台确认
3. 确认账号有效

---

### 错误 3: "Connection timeout"

**解决方案**:

1. 检查网络连接
2. 检查防火墙设置
3. 尝试使用 VPN（如果在受限网络）

---

### 错误 4: "404 Not Found"

**解决方案**:

1. API 端点可能不正确
2. 联系 aimiai.com 确认正确的 API 地址
3. 查看 API 文档

---

## 🔄 备用数据源

如果 aimiai.com API 暂时无法使用，可以使用：

### 1. akshare（免费，推荐）

```python
import akshare as ak

# 安装
pip install akshare

# 使用
df = ak.stock_zh_a_hist(symbol="600036", period="daily", adjust="qfq")
```

### 2. tushare

```python
import tushare as ts

# 需要注册获取 token
ts.set_token('your_token')
pro = ts.pro_api()

df = pro.daily(ts_code='600036.SH')
```

---

## 📞 获取帮助

### 1. 运行诊断工具

```bash
# 简单测试
python test_api_connection.py

# 详细诊断
python diagnose_api.py
```

### 2. 查看文档

- `API_TROUBLESHOOTING.md` - 完整故障排除指南
- `BEARER_AUTH_UPDATE.md` - API 认证说明

### 3. 联系支持

如果问题仍未解决：

1. 保存诊断输出
2. 联系 aimiai.com 技术支持
3. 提供 AppId（不要提供 AppKey）
4. 描述具体错误信息

---

## 🚀 快速开始

```bash
# 1. 运行快速诊断
python test_api_connection.py

# 2. 如果失败，删除 .env 中的 token 行

# 3. 重新测试
python test_bearer_auth.py

# 4. 如果成功，运行分析
python analyze_recent_2weeks.py
```

---

## 💡 提示

1. **Token 有效期**: 通常 24 小时
2. **自动刷新**: 系统会自动检测过期并刷新
3. **手动刷新**: 删除 .env 中的 token 行即可
4. **保存日志**: 遇到问题时保存错误信息

---

## ✅ 验证修复

修复后，运行以下命令验证：

```bash
# 1. 测试 API 连接
python test_bearer_auth.py

# 2. 快速测试（1只股票）
python test_2weeks_quick.py

# 3. 完整分析
python analyze_recent_2weeks.py
```

如果都成功，说明问题已解决！

---

**需要立即修复？运行：**

```bash
QUICK_FIX_API.bat
```

或

```bash
python test_api_connection.py
```
