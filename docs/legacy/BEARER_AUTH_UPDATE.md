# Bearer Token Authentication - 更新说明

## ✅ 已完成更新

### 1. 从 .env 加载 Token

系统现在会自动从 `.env` 文件读取已有的 token：

```bash
# .env 文件
AppId=e916a637eb6a4dfd9722d0baeab8807a
AppKey=6856917787b74fc983fc0da56f41e27b
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Bearer Token 认证格式

所有业务 API 请求现在使用标准的 Bearer token 格式：

```python
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'  # 注意 Bearer 后有空格
}
```

### 3. 更新的 API 方法

#### ✅ `get_stock_data()` - 获取 K 线数据

```python
# 请求头
Authorization: Bearer {token}

# 请求体
{
  "code": "600036",
  "startDate": "20240101",
  "endDate": "20241231",
  "klt": "101",  # 日K线
  "fqt": "1"     # 前复权
}
```

#### ✅ `get_stock_list()` - 获取股票列表

```python
# 请求头
Authorization: Bearer {token}

# 请求体
{
  "sector": "芯片"  # 可选
}
```

#### ✅ `get_realtime_price()` - 获取实时行情

```python
# 请求头
Authorization: Bearer {token}

# 请求体
{
  "code": "600036"
}
```

## 认证流程

### 方式 1: 使用 .env 中的 token（推荐）

如果你已经有 token，直接添加到 `.env` 文件：

```bash
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6ImU5MTZhNjM3ZWI2YTRkZmQ5NzIyZDBiYWVhYjg4MDdhIiwidXNlcklkIjoiODQ1ODAxMyIsImV4cCI6MTc2NTk5MjAyOX0.mgtX1DjOrgOdqSa4-2Ca3TUHxWHTeI_uLoLV6WYuMHc
```

系统会自动使用这个 token，无需重新请求。

### 方式 2: 自动获取新 token

如果 `.env` 中没有 token，系统会自动请求：

```python
# POST https://aimiai.com/api/token/get
{
  "appId": "你的_app_id",
  "appKey": "你的_app_key"
}

# 响应
{
  "code": 200,
  "data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 测试 Bearer 认证

运行测试脚本验证 Bearer token 认证：

```bash
python test_bearer_auth.py
```

测试内容：

1. ✓ 检查 .env 中的 token
2. ✓ 初始化 API 客户端
3. ✓ 获取/使用 token
4. ✓ 测试 API 调用（使用 Bearer token）

## 完整示例

### Python 代码示例

```python
from src.data.aimiai_stock_api import AimiaiStockAPI

# 初始化 API（会自动加载 .env 中的 token）
api = AimiaiStockAPI()

# 获取股票数据（自动使用 Bearer token）
df = api.get_stock_data("600036", days=100)

# 获取实时价格（自动使用 Bearer token）
price = api.get_realtime_price("600036")
```

### HTTP 请求示例

```bash
# 获取 Token
curl -X POST https://aimiai.com/api/token/get \
  -H "Content-Type: application/json" \
  -d '{"appId":"你的_app_id","appKey":"你的_app_key"}'

# 使用 Token 获取数据
curl -X POST https://aimiai.com/api/stock/kline \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"code":"600036","startDate":"20240101","endDate":"20241231","klt":"101","fqt":"1"}'
```

## 关键变更

### 之前的格式（已废弃）

```python
headers = {
    'Content-Type': 'application/json',
    'AppId': self.app_id,
    'AppKey': self.app_key,
    'Token': token  # ❌ 旧格式
}
```

### 现在的格式（正确）

```python
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'  # ✅ 新格式
}
```

## 注意事项

### ⚠️ Bearer 后面有空格

```python
# ✅ 正确
'Authorization': f'Bearer {token}'

# ❌ 错误
'Authorization': f'Bearer{token}'  # 缺少空格
```

### ⚠️ Token 有效期

- Token 通常有效期为 24 小时
- 系统会自动检查 token 是否过期
- 过期后会自动请求新 token

### ⚠️ Token 安全

- 不要在代码中硬编码 token
- 使用 `.env` 文件存储
- 不要提交 `.env` 到版本控制

## 快速开始

### 1. 确认 .env 配置

```bash
# 检查 .env 文件
cat .env

# 应该包含
AppId=你的_app_id
AppKey=你的_app_key
token=你的_token  # 可选
```

### 2. 测试认证

```bash
python test_bearer_auth.py
```

### 3. 运行 Shannon 扫描

```bash
python find_shannon_pattern.py
```

## 故障排除

### 问题 1: 401 Unauthorized

**原因**: Token 无效或过期

**解决方案**:

1. 删除 `.env` 中的 token 行
2. 系统会自动请求新 token
3. 或手动更新 token

### 问题 2: Token 格式错误

**原因**: Authorization header 格式不正确

**解决方案**:

- 确保格式为: `Authorization: Bearer {token}`
- 检查 Bearer 后面有空格
- 检查 token 字符串完整

### 问题 3: API 调用失败

**原因**: 可能是网络问题或 API 端点错误

**解决方案**:

1. 检查网络连接
2. 验证 API 端点 URL
3. 查看详细错误日志

## 更新的文件

1. ✅ `src/data/aimiai_stock_api.py` - 主 API 客户端
2. ✅ `test_bearer_auth.py` - Bearer 认证测试
3. ✅ `SHANNON_PATTERN_GUIDE.md` - 更新文档
4. ✅ `SHANNON_CRITERIA.md` - 更新快速参考
5. ✅ `.env` - 包含 token

## 总结

✅ **已完成**:

- Bearer token 认证格式
- 从 .env 自动加载 token
- 所有业务 API 使用 Bearer 格式
- 完整的测试脚本
- 更新的文档

🚀 **现在可以使用**:

```bash
python find_shannon_pattern.py
```

系统会自动使用 `.env` 中的 token，并以正确的 `Authorization: Bearer {token}` 格式发送请求！
