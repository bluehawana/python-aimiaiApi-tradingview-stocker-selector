# 📦 本地数据分析指南

## ✅ 无需 API - 使用本地 ZIP 文件

你已经下载了 **2024 年 11 月 6 日-17 日** 的股票数据（共 12 天），可以直接分析，不需要任何 API！

---

## 🚀 快速开始（3 步）

### 步骤 1: 导入数据文件

**方式 1: 一键导入（推荐）**

```bash
双击运行: 1_IMPORT_DATA.bat
```

**方式 2: 手动复制**
将这些文件从桌面复制到 `data/local/` 目录：

- 20251106.zip
- 20251107.zip
- 20251110.zip
- 20251111.zip
- 20251112.zip
- 20251113.zip
- 20251114.zip
- 20251117.zip

---

### 步骤 2: 测试数据加载

```bash
双击运行: 2_TEST_DATA.bat
```

这会：

- ✅ 列出所有可用日期
- ✅ 加载第一个 ZIP 文件
- ✅ 显示包含的数据表
- ✅ 列出所有股票代码

---

### 步骤 3: 运行分析

```bash
双击运行: 3_ANALYZE_LOCAL.bat
```

这会使用 **4 大严格标准** 筛选突破股票：

1. ✅ 近期接近金叉
2. ✅ 成交量 >= 3x 正常日均量
3. ✅ MCDX: PC >= 95%, SMA PC >= 80%
4. ✅ 当天涨幅 >= 5%

---

## 📊 数据覆盖范围

### 时间范围

- **开始日期**: 2024 年 11 月 6 日（周三）
- **结束日期**: 2024 年 11 月 17 日（周日）
- **总天数**: 12 天（约 2 周）
- **交易日**: 约 8-9 个交易日

### 数据内容

每个 ZIP 文件包含：

- 所有 A 股股票数据
- 日 K 线数据（开盘、最高、最低、收盘、成交量）
- 可能包含其他指标数据

---

## 🎯 分析功能

### 1. 突破股票筛选（4 大标准）

```bash
# 基础分析
python analyze_local_data.py

# 自定义参数
python analyze_local_data.py --min-volume 3.0 --min-pc 95 --min-gain 5

# 只分析特定股票
python analyze_local_data.py --symbols 600036 000001 300750

# 导出结果
python analyze_local_data.py --export results/my_analysis.csv
```

**输出示例**:

```
🚀 600036
================================================================================
突破次数: 2 次
最新日期: 2024-11-17
最新价格: ¥45.80
最新 MCDX: PC=96.3%, SMA PC=85.2%

突破日详情:

  [1] 2024-11-12
      ✅ 价格: ¥44.50 (涨幅 +6.5%)
      ✅ 成交量: 125.5M (3.2x)
      ✅ MCDX: PC=95.8%, SMA PC=82.1%
      ✅ 金叉: 已金叉
```

---

### 2. 查看所有股票代码

```bash
python -c "
from src.data.local_data_loader import LocalDataLoader
loader = LocalDataLoader('data/local')
symbols = loader.get_all_symbols()
print(f'共 {len(symbols)} 只股票')
print('示例:', symbols[:20])
"
```

---

### 3. 获取单只股票数据

```python
from src.data.local_data_loader import LocalDataLoader

# 初始化加载器
loader = LocalDataLoader('data/local')

# 获取股票数据
df = loader.get_stock_data('600036')  # 招商银行

print(f"数据天数: {len(df)}")
print(df.head())
```

---

## 📁 文件结构

```
.
├── data/
│   └── local/              # 本地数据目录
│       ├── 20251106.zip
│       ├── 20251107.zip
│       ├── 20251110.zip
│       ├── 20251111.zip
│       ├── 20251112.zip
│       ├── 20251113.zip
│       ├── 20251114.zip
│       └── 20251117.zip
│
├── src/data/
│   └── local_data_loader.py    # 本地数据加载器
│
├── import_local_data.py         # 导入数据脚本
├── analyze_local_data.py        # 分析脚本
│
├── 1_IMPORT_DATA.bat           # 步骤1: 导入数据
├── 2_TEST_DATA.bat             # 步骤2: 测试数据
└── 3_ANALYZE_LOCAL.bat         # 步骤3: 运行分析
```

---

## 🔍 筛选标准详解

### 标准 1: 近期接近金叉

- **金叉**: SMA Profit Chips 上穿 SMA Locked Chips
- **已金叉**: SMA PC > SMA LC
- **接近金叉**: 差距 < 10%

### 标准 2: 成交量暴增

- **计算**: 当天成交量 / 30 日平均成交量
- **要求**: >= 3.0x（300%）
- **示例**: 正常 30M，突破日 90M+

### 标准 3: MCDX 指标

- **Profit Chips (PC)**: >= 95%（红色柱状图接近 100）
- **SMA Profit Chips**: >= 80%（深红色线在 80 以上）
- **含义**: 筹码高度集中，获利盘充足

### 标准 4: 价格涨幅

- **要求**: 当天涨幅 >= 5%
- **上限**: < 20%（过滤异常）
- **含义**: 有明显的突破动作

---

## 📊 输出结果

### 控制台输出

- 每只股票的突破次数
- 每个突破日的详细信息
- MCDX 指标
- 成交量比率
- 金叉状态

### CSV 导出

自动导出到 `results/local_breakout_YYYYMMDD_HHMMSS.csv`

包含字段：

- symbol: 股票代码
- breakout_date: 突破日期
- close: 收盘价
- price_gain: 涨幅%
- volume: 成交量
- volume_ratio: 成交量比率
- profit_chips: PC
- sma_profit_chips: SMA PC
- golden_cross_status: 金叉状态
- ... 等

---

## 🎯 使用场景

### 场景 1: 发现历史突破股票

```bash
# 找出11月6-17日期间的所有突破股票
python analyze_local_data.py
```

### 场景 2: 验证特定股票

```bash
# 只分析宁德时代、比亚迪
python analyze_local_data.py --symbols 300750 002594
```

### 场景 3: 调整筛选标准

```bash
# 降低标准，找更多候选
python analyze_local_data.py --min-pc 90 --min-sma-pc 75 --min-gain 3

# 提高标准，只要最强的
python analyze_local_data.py --min-pc 98 --min-sma-pc 85 --min-gain 7
```

### 场景 4: 导出数据分析

```bash
# 导出到 Excel 进一步分析
python analyze_local_data.py --export results/breakout_analysis.csv
```

---

## 💡 优势

### ✅ 无需 API

- 不需要 aimiai.com API
- 不需要网络连接
- 不需要 token 认证
- 完全离线运行

### ✅ 数据完整

- 11 月 6-17 日完整数据
- 包含所有 A 股
- 足够计算 MCDX 和成交量指标

### ✅ 快速分析

- 本地读取，速度快
- 无 API 限流问题
- 可重复运行

### ✅ 灵活配置

- 可调整筛选标准
- 可指定股票列表
- 可导出结果

---

## 🔧 高级用法

### 1. 批量分析特定板块

```python
from src.data.local_data_loader import LocalDataLoader
from analyze_local_data import LocalBreakoutFinder

# 芯片板块
chip_stocks = ['688981', '002371', '603501', '688008']

finder = LocalBreakoutFinder('data/local')
results = finder.scan_all_stocks(chip_stocks)
```

### 2. 自定义筛选条件

```python
finder = LocalBreakoutFinder('data/local')

# 调整标准
finder.min_volume_ratio = 2.5  # 降低成交量要求
finder.min_profit_chips = 90.0  # 降低 PC 要求
finder.min_price_gain = 3.0     # 降低涨幅要求

results = finder.scan_all_stocks()
```

### 3. 获取原始数据

```python
from src.data.local_data_loader import LocalDataLoader

loader = LocalDataLoader('data/local')

# 获取所有日期
dates = loader.list_available_dates()
print(f"可用日期: {dates}")

# 加载特定日期
data = loader.load_zip_file('20251117')
print(f"包含 {len(data)} 个数据表")

# 获取股票数据
df = loader.get_stock_data('600036', dates)
print(df)
```

---

## 📝 注意事项

### 1. 数据格式

- ZIP 文件必须包含 CSV 或 Excel 文件
- 必须有股票代码列（代码/code/symbol）
- 必须有 OHLCV 数据（开高低收量）

### 2. 数据质量

- 确保数据完整无缺失
- 检查日期格式正确
- 验证成交量单位一致

### 3. 计算限制

- 需要至少 30 天数据计算 MCDX
- 成交量比率需要 30 日均量
- 数据越多，结果越准确

---

## 🆘 故障排除

### 问题 1: 找不到数据文件

**解决方案**:

```bash
# 检查文件是否存在
dir data\local\*.zip

# 重新导入
python import_local_data.py
```

### 问题 2: 无法读取 ZIP 文件

**解决方案**:

- 确认 ZIP 文件未损坏
- 尝试手动解压查看内容
- 检查文件权限

### 问题 3: 没有找到股票

**解决方案**:

- 检查股票代码是否正确（6 位数字）
- 查看数据文件中包含哪些股票
- 运行 `python src/data/local_data_loader.py` 查看所有股票

### 问题 4: 数据列名不匹配

**解决方案**:

- 查看 `src/data/local_data_loader.py` 中的 `column_mapping`
- 根据实际数据调整列名映射

---

## 🚀 立即开始

```bash
# 1. 导入数据
双击: 1_IMPORT_DATA.bat

# 2. 测试数据
双击: 2_TEST_DATA.bat

# 3. 运行分析
双击: 3_ANALYZE_LOCAL.bat
```

---

## 📞 获取帮助

如果遇到问题：

1. 运行 `python src/data/local_data_loader.py` 测试数据加载
2. 检查 `data/local/` 目录是否有 ZIP 文件
3. 查看错误日志了解具体问题

---

**开始使用本地数据分析！** 🎉

无需 API，无需网络，立即发现突破股票！
