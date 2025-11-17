# 🎉 开始本地数据分析！

## ✅ 无需 API - 直接使用本地数据

你有 **2024 年 11 月 6-17 日** 的完整股票数据（12 天），可以立即开始分析！

---

## 🚀 3 步开始

### 1️⃣ 导入数据（1 分钟）

```bash
双击运行: 1_IMPORT_DATA.bat
```

这会将桌面上的 8 个 ZIP 文件复制到 `data/local/` 目录。

---

### 2️⃣ 测试数据（30 秒）

```bash
双击运行: 2_TEST_DATA.bat
```

验证数据加载正常，查看包含多少只股票。

---

### 3️⃣ 运行分析（2-5 分钟）

```bash
双击运行: 3_ANALYZE_LOCAL.bat
```

使用 **4 大严格标准** 筛选突破股票！

---

## 📊 你将得到什么

### 筛选标准

1. ✅ **金叉**: 近期接近或已发生金叉
2. ✅ **成交量**: >= 3x 正常日均量（如 30M → 90M+）
3. ✅ **MCDX**: PC >= 95%, SMA PC >= 80%
4. ✅ **涨幅**: 当天 >= 5%

### 输出结果

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
      ✅ 成交量: 125.5M (3.2x 正常)
      ✅ MCDX: PC=95.8%, SMA PC=82.1%
      ✅ 金叉: 已金叉
      ✅ 行为: Strong Hold
```

### 自动导出

结果自动保存到 `results/local_breakout_YYYYMMDD_HHMMSS.csv`

---

## 💡 数据说明

### 时间范围

- **11 月 6 日** (周三) - **11 月 17 日** (周日)
- **12 天数据**，约 8-9 个交易日
- 足够计算 MCDX 和成交量指标

### 数据内容

- ✅ 所有 A 股股票
- ✅ 日 K 线（开高低收量）
- ✅ 完整的历史数据

---

## 🎯 优势

| 特点            | 说明                         |
| --------------- | ---------------------------- |
| ✅ **无需 API** | 不需要 aimiai.com 或其他 API |
| ✅ **完全离线** | 无需网络连接                 |
| ✅ **快速分析** | 本地读取，速度快             |
| ✅ **可重复**   | 随时重新运行                 |
| ✅ **灵活配置** | 可调整筛选标准               |

---

## 🔧 自定义分析

### 调整筛选标准

```bash
# 降低标准，找更多候选
python analyze_local_data.py --min-pc 90 --min-sma-pc 75 --min-gain 3

# 提高标准，只要最强的
python analyze_local_data.py --min-pc 98 --min-sma-pc 85 --min-gain 7

# 只看成交量暴增的
python analyze_local_data.py --min-volume 4.0
```

### 分析特定股票

```bash
# 只分析宁德时代、比亚迪、隆基绿能
python analyze_local_data.py --symbols 300750 002594 601012
```

### 导出结果

```bash
# 导出到指定文件
python analyze_local_data.py --export results/my_analysis.csv
```

---

## 📁 文件位置

```
你的项目/
├── data/local/              ← ZIP 文件放这里
│   ├── 20251106.zip
│   ├── 20251107.zip
│   ├── ...
│   └── 20251117.zip
│
├── results/                 ← 分析结果保存这里
│   └── local_breakout_*.csv
│
├── 1_IMPORT_DATA.bat       ← 步骤1
├── 2_TEST_DATA.bat         ← 步骤2
└── 3_ANALYZE_LOCAL.bat     ← 步骤3
```

---

## ✅ 检查清单

开始前确认：

- [ ] 桌面上有 8 个 ZIP 文件（20251106.zip 到 20251117.zip）
- [ ] Python 已安装
- [ ] 已安装依赖：pandas, numpy

如果缺少依赖：

```bash
pip install pandas numpy openpyxl
```

---

## 🆘 遇到问题？

### 问题 1: 找不到 ZIP 文件

**解决方案**:

- 确认 ZIP 文件在桌面
- 或手动复制到 `data/local/` 目录

### 问题 2: 无法读取数据

**解决方案**:

```bash
# 运行测试
python src/data/local_data_loader.py
```

### 问题 3: 没有找到突破股票

**解决方案**:

- 降低筛选标准
- 检查数据日期范围
- 确认数据完整

---

## 📚 详细文档

- `LOCAL_DATA_GUIDE.md` - 完整使用指南
- `src/data/local_data_loader.py` - 数据加载器源码
- `analyze_local_data.py` - 分析脚本源码

---

## 🚀 立即开始！

```bash
# 第1步
双击: 1_IMPORT_DATA.bat

# 第2步
双击: 2_TEST_DATA.bat

# 第3步
双击: 3_ANALYZE_LOCAL.bat
```

---

## 🎯 预期结果

运行完成后，你会得到：

1. ✅ 符合 4 大标准的突破股票列表
2. ✅ 每只股票的突破日详情
3. ✅ MCDX 指标和成交量分析
4. ✅ CSV 文件，可用 Excel 打开

---

**开始发现 11 月 6-17 日的突破股票！** 🚀

无需 API，无需网络，立即开始！
