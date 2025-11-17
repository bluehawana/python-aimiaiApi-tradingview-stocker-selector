# 🎯 Tushare 使用指南 (推荐)

## 为什么选择 Tushare？

✅ **最稳定** - 专业的中国金融数据平台  
✅ **免费** - 注册即可使用  
✅ **完整** - 覆盖所有 A 股数据  
✅ **可靠** - 不会有网络连接问题

---

## 🚀 快速开始 (3 步)

### 步骤 1: 注册并获取 Token (2 分钟)

1. **注册账号**: https://tushare.pro/register
2. **获取 Token**: https://tushare.pro/user/token
3. **复制 Token** (类似: `1234567890abcdef1234567890abcdef`)

### 步骤 2: 配置 Token (30 秒)

打开 `.env` 文件，找到这一行:

```
TUSHARE_TOKEN=your_tushare_token_here
```

替换为你的 token:

```
TUSHARE_TOKEN=1234567890abcdef1234567890abcdef
```

### 步骤 3: 下载数据 (5-10 分钟)

```bash
双击运行: DOWNLOAD_TUSHARE.bat
```

或命令行:

```bash
python download_tushare.py
```

---

## 📊 下载内容

### 时间范围

- **最近 3 个月** 的日 K 线数据
- 足够计算 MCDX 和成交量指标

### 覆盖板块 (50+ 只股票)

1. 芯片半导体 (5 只)
2. 存储芯片 (3 只)
3. CPO 光学 (3 只)
4. 固态电池 (4 只)
5. 六氟磷酸锂 (4 只)
6. 储能 (5 只)
7. 光伏 (5 只)
8. 智能电网 (4 只)
9. 机器人 (5 只)
10. 新能源汽车 (4 只)

### 数据字段

- 日期 (date)
- 开盘价 (open)
- 最高价 (high)
- 最低价 (low)
- 收盘价 (close)
- 成交量 (volume)
- 成交额 (amount)
- 涨跌幅 (change_pct)

### 数据质量

- ✅ 前复权数据
- ✅ 准确可靠
- ✅ 实时更新

---

## 🎯 完整流程

```bash
# 1. 下载数据
DOWNLOAD_TUSHARE.bat

# 2. 分析数据
2_ANALYZE_STOCKS.bat
```

或命令行:

```bash
# 1. 下载
python download_tushare.py

# 2. 分析
python analyze_akshare_data.py --data-dir data/tushare
```

---

## 📁 数据保存位置

```
D:\projects\TW\
└── data/
    └── tushare/
        ├── 600036.csv  (招商银行)
        ├── 000001.csv  (平安银行)
        ├── 300750.csv  (宁德时代)
        └── ...
```

---

## 🔍 分析标准

下载完成后，系统会使用 **4 大严格标准** 筛选突破股票:

1. ✅ **金叉**: 近期接近或已发生金叉
2. ✅ **成交量**: >= 3x 正常日均量
3. ✅ **MCDX**: PC >= 95%, SMA PC >= 80%
4. ✅ **涨幅**: 当天 >= 5%

---

## 📊 输出结果

### 控制台输出

```
🚀 300750
================================================================================
突破次数: 2 次
最新日期: 2024-11-17
最新价格: ¥245.80

突破日详情:

  2024-11-12
    ✅ 价格: ¥240.50 (涨幅 +6.5%)
    ✅ 成交量: 1.25亿 (3.2x)
    ✅ MCDX: PC=95.8%, SMA PC=82.1%
    ✅ 金叉: 已金叉
```

### CSV 导出

`results/akshare_breakout_YYYYMMDD_HHMMSS.csv`

包含所有突破日的详细数据，可用 Excel 打开。

---

## ⚙️ 高级选项

### 自定义日期范围

编辑 `download_tushare.py`，修改这一行:

```python
start_date = end_date - timedelta(days=90)  # 改为 180 = 6个月
```

### 只下载特定股票

```bash
python download_tushare.py --symbols 600036 000001 300750
```

### 调整筛选标准

```bash
python analyze_akshare_data.py --data-dir data/tushare --min-pc 90 --min-gain 3
```

---

## 💡 Tushare 积分说明

### 免费用户

- ✅ 日线数据: 无限制
- ✅ 基础指标: 无限制
- ⚠️ 分钟数据: 需要积分

### 获取积分

1. 完成注册: 100 积分
2. 完善资料: 100 积分
3. 邀请好友: 每人 100 积分
4. 分享文章: 获得积分

### 查看积分

https://tushare.pro/user/vip

---

## 🆚 对比其他方案

| 方案        | 稳定性     | 速度       | 难度       | 推荐度        |
| ----------- | ---------- | ---------- | ---------- | ------------- |
| **Tushare** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ✅ 强烈推荐   |
| akshare     | ⭐⭐       | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | ⚠️ 网络不稳定 |
| 通达信导出  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ✅ 推荐       |
| 手动下载    | ⭐⭐⭐⭐   | ⭐⭐       | ⭐⭐       | ⚠️ 太慢       |

---

## 🆘 故障排除

### 问题 1: Token 无效

**解决方案**:

1. 访问 https://tushare.pro/user/token
2. 确认 token 正确
3. 重新复制到 .env 文件

### 问题 2: 下载失败

**解决方案**:

1. 检查网络连接
2. 确认积分充足
3. 稍后重试

### 问题 3: 数据不完整

**解决方案**:

1. 检查日期范围
2. 确认股票代码正确
3. 查看 Tushare 数据更新时间

---

## 📞 获取帮助

- **Tushare 文档**: https://tushare.pro/document/2
- **API 接口**: https://tushare.pro/document/2?doc_id=27
- **社区论坛**: https://tushare.pro/forum

---

## 🎉 开始使用

```bash
# 1. 注册获取 token
https://tushare.pro/register

# 2. 配置 .env
TUSHARE_TOKEN=your_token_here

# 3. 下载数据
DOWNLOAD_TUSHARE.bat

# 4. 分析数据
2_ANALYZE_STOCKS.bat
```

**Tushare 是最稳定可靠的方案！** 🚀
