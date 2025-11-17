# API 故障排除指南

## 🔍 问题诊断

如果所有 API 调用都失败，请按以下步骤排查：

### 步骤 1: 运行诊断工具

```bash
# 简单测试
python test_api_connection.py

# 详细诊断
python diagnose_api.py
```

---

## 常见问题和解决方案

### 问题 1: Token 已过期

**症状**:

- API 返回 401 Unauthorized
- 提示 "token expired" 或 "invalid token"

**解决方案**:

```bash
# 方法 1: 删除旧 token，让系统重新获取
# 编辑 .env 文件，删除或注释掉 token 行
# token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 方法 2: 手动获取新 token
python -c "
import requests
response = requests.post(
    'https://aimiai.com/api/token/get',
    json={'appId': 'your_app_id', 'appKey': 'your_app_key'}
)
print(response.json())
"
```

---

### 问题 2: API 端点不正确

**症状**:

- 404 Not Found
- API 无响应

**可能的端点**:

```python
# 尝试这些端点
endpoints = [
    "https://aimiai.com/api/token/get",
    "https://aimiai.com/api/stock/kline",
    "https://aimiai.com/api/stock/list",
    "https://aimiai.com/api/stock/quote",
]

# 或者可能是其他域名
alternative_domains = [
    "https://api.aimiai.com",
    "https://data.aimiai.com",
]
```

**解决方案**:

1. 登录 aimiai.com 控制台
2. 查看 API 文档
3. 确认正确的 API 端点

---

### 问题 3: 认证格式不对

**症状**:

- 401 Unauthorized
- "invalid authorization header"

**测试不同的认证格式**:

```python
# 格式 1: Bearer Token (当前使用)
headers = {
    'Authorization': f'Bearer {token}'
}

# 格式 2: 直接 Token
headers = {
    'Token': token
}

# 格式 3: AppId + AppKey + Token
headers = {
    'AppId': app_id,
    'AppKey': app_key,
    'Token': token
}

# 格式 4: X-Auth-Token
headers = {
    'X-Auth-Token': token
}
```

---

### 问题 4: AppId/AppKey 无效

**症状**:

- 获取 token 失败
- "invalid credentials"

**解决方案**:

1. 登录 https://aimiai.com/console
2. 检查 API Keys 页面
3. 确认 AppId 和 AppKey 正确
4. 检查账号是否有 API 权限
5. 确认账号是否欠费或被禁用

---

### 问题 5: 网络连接问题

**症状**:

- Connection timeout
- Network error

**解决方案**:

```bash
# 测试网络连接
ping aimiai.com

# 测试 HTTPS 连接
curl https://aimiai.com

# 检查代理设置
echo %HTTP_PROXY%
echo %HTTPS_PROXY%

# 如果在公司网络，可能需要配置代理
```

---

### 问题 6: API 限流

**症状**:

- 429 Too Many Requests
- "rate limit exceeded"

**解决方案**:

1. 减少请求频率
2. 添加延迟：`time.sleep(1)`
3. 检查 API 配额
4. 升级 API 套餐

---

## 🔧 手动测试 API

### 使用 curl 测试

```bash
# 1. 获取 token
curl -X POST https://aimiai.com/api/token/get \
  -H "Content-Type: application/json" \
  -d "{\"appId\":\"your_app_id\",\"appKey\":\"your_app_key\"}"

# 2. 使用 token 获取数据
curl -X POST https://aimiai.com/api/stock/kline \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d "{\"code\":\"600036\",\"startDate\":\"20241101\",\"endDate\":\"20241117\",\"klt\":\"101\",\"fqt\":\"1\"}"
```

### 使用 Python 测试

```python
import requests

# 1. 获取 token
response = requests.post(
    'https://aimiai.com/api/token/get',
    json={'appId': 'your_app_id', 'appKey': 'your_app_key'}
)
print(response.json())
token = response.json()['data']

# 2. 获取数据
response = requests.post(
    'https://aimiai.com/api/stock/kline',
    json={
        'code': '600036',
        'startDate': '20241101',
        'endDate': '20241117',
        'klt': '101',
        'fqt': '1'
    },
    headers={'Authorization': f'Bearer {token}'}
)
print(response.json())
```

---

## 📝 检查清单

在联系技术支持前，请确认：

- [ ] AppId 和 AppKey 正确
- [ ] Token 未过期
- [ ] 网络连接正常
- [ ] API 端点正确
- [ ] 认证格式正确
- [ ] 账号有 API 权限
- [ ] 未超过 API 限额
- [ ] 防火墙未阻止连接

---

## 🆘 获取帮助

### 1. 查看 aimiai.com 文档

- 登录控制台
- 查看 API 文档
- 查看示例代码

### 2. 联系 aimiai.com 支持

- 提供 AppId（不要提供 AppKey）
- 描述具体错误信息
- 提供请求和响应日志

### 3. 检查系统状态

- 访问 aimiai.com 查看是否有维护公告
- 检查 API 服务状态

---

## 🔄 临时解决方案

如果 aimiai.com API 暂时无法使用，可以尝试：

### 方案 1: 使用 akshare（免费）

```python
import akshare as ak

# 获取股票数据
df = ak.stock_zh_a_hist(symbol="600036", period="daily", adjust="qfq")
```

### 方案 2: 使用 tushare

```python
import tushare as ts

ts.set_token('your_tushare_token')
pro = ts.pro_api()

# 获取股票数据
df = pro.daily(ts_code='600036.SH', start_date='20241101', end_date='20241117')
```

### 方案 3: 使用 Yahoo Finance（美股）

```python
import yfinance as yf

# 获取美股数据
df = yf.download('AAPL', start='2024-11-01', end='2024-11-17')
```

---

## 📊 诊断输出示例

### 成功的输出

```
[1/5] 检查环境变量...
  ✓ AppId: e916a637eb6a4dfd97...
  ✓ AppKey: 6856917787b74fc983...
  ✓ Token: eyJhbGciOiJIUzI1NiIsInR5cCI...

[2/5] 测试获取 token...
  → POST https://aimiai.com/api/token/get
  ← Status: 200
  ✓ 成功获取 token

[3/5] 测试业务 API...
  ✓ 获取K线数据 成功
  ✓ 获取股票列表 成功
```

### 失败的输出

```
[2/5] 测试获取 token...
  → POST https://aimiai.com/api/token/get
  ← Status: 401
  ✗ API 返回错误: invalid credentials

建议操作:
1. 检查 AppId 和 AppKey 是否正确
2. 登录 aimiai.com 控制台确认
```

---

## 🚀 快速修复

```bash
# 1. 运行诊断
python test_api_connection.py

# 2. 如果 token 过期，删除旧 token
# 编辑 .env，删除 token 行

# 3. 重新测试
python test_bearer_auth.py

# 4. 如果还是失败，运行详细诊断
python diagnose_api.py
```

---

## 💡 提示

1. **Token 有效期**: 通常 24 小时，过期后需重新获取
2. **API 限流**: 注意不要频繁调用，建议间隔 1 秒
3. **错误日志**: 保存错误信息，便于排查
4. **备用方案**: 准备其他数据源作为备用

---

**需要帮助？运行诊断工具获取详细信息！**

```bash
python diagnose_api.py
```
