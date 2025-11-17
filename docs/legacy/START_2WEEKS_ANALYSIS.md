# 🚀 开始最近 2 周热点分析

## ✅ 系统已就绪

你现在拥有一个完整的**最近 2 周多板块热点分析系统**！

## 🎯 核心功能

### 1. 实时数据分析

- ✅ 分析最近 14 天（2 周）的实时数据
- ✅ 不再依赖 9 月的历史数据
- ✅ 每天都能发现最新热点

### 2. 多维度指标

- ✅ **成交量分析**: 2 周平均、最大值、暴量天数
- ✅ **MCDX 指标**: PC、LC、SMA 及 2 周变化趋势
- ✅ **技术信号**: Golden Cross、Double Dragon、Volume Surge
- ✅ **热度评分**: 0-100 分综合评分系统

### 3. 全面板块覆盖

- ✅ 芯片半导体（5 只）
- ✅ 存储芯片（3 只）
- ✅ CPO 光学（3 只）
- ✅ 固态电池（4 只）
- ✅ 六氟磷酸锂（4 只）
- ✅ 储能（5 只）
- ✅ 光伏（5 只）
- ✅ 智能电网（4 只）
- ✅ 机器人（5 只）
- ✅ 新能源汽车（4 只）

**总计**: 50+ 只优质股票

## 🚀 立即开始

### 方式 1: 一键运行（最简单）

**Windows 用户**:

```bash
双击运行: RUN_2WEEKS_ANALYSIS.bat
```

**Mac/Linux 用户**:

```bash
python analyze_recent_2weeks.py
```

### 方式 2: 自定义参数

```bash
# 高标准筛选（热度 >= 60）
python analyze_recent_2weeks.py --min-score 60

# 分析最近10天
python analyze_recent_2weeks.py --days 10

# 导出结果
python analyze_recent_2weeks.py --export results/my_report.csv
```

## 📊 你将看到什么

### 输出示例

```
================================================================================
🔥 300750 - solid_state_battery
================================================================================
热度评分: 85.5/100
日期: 2024-11-17
价格: ¥245.80 (+8.5% 近2周)

📈 MCDX 指标:
  Profit Chips: 92.3% (SMA: 88.5%)
  Locked Chips: 4.2% (SMA: 6.1%)
  行为模式: Strong Hold
  建议: BUY
  最近2周趋势: 强势上升 (PC变化: +12.5%)

📊 成交量分析:
  最新成交量: 125.5M
  30日平均: 38.2M
  成交量比率: 3.28x
  最近2周趋势: 显著放量
  2周平均成交量: 95.3M
  2周最大成交量: 145.8M
  暴量天数(>2x): 8 天

🎯 技术信号:
  ✨ Golden Cross, 🐉 Double Dragon, 🔥 Volume Surge
```

## 🔥 热度等级

| 分数   | 等级   | 说明                |
| ------ | ------ | ------------------- |
| 80-100 | 🔥🔥🔥 | 超级热点 - 重点关注 |
| 60-79  | 🔥🔥   | 高热度 - 值得关注   |
| 50-59  | 🔥     | 中等热度 - 观察     |
| < 50   | ⚪     | 低热度 - 暂不关注   |

## 📁 输出文件

### 自动生成 CSV

```
results/recent_2weeks_20241117_143025.csv
```

包含完整数据：

- 股票代码、板块
- 价格、涨跌幅
- MCDX 指标（当前值 + 2 周变化）
- 成交量分析（比率、趋势、暴量天数）
- 技术信号
- 热度评分

## 🎯 使用场景

### 每日盘后

```bash
# 找出今日热点
python analyze_recent_2weeks.py --min-score 60
```

### 周末复盘

```bash
# 分析整周表现
python analyze_recent_2weeks.py --days 7
```

### 板块轮动

```bash
# 低门槛扫描，观察轮动
python analyze_recent_2weeks.py --min-score 40
```

## 🔧 系统要求

### 已配置

- ✅ Python 环境
- ✅ aimiai.com API 凭证（.env）
- ✅ Bearer Token 认证
- ✅ 所有依赖库

### 测试连接

```bash
python test_bearer_auth.py
```

## 📚 文档

- `RECENT_2WEEKS_GUIDE.md` - 完整使用指南
- `BEARER_AUTH_UPDATE.md` - API 认证说明
- `config_multi_sector.yaml` - 板块配置

## 🆚 对比其他工具

| 工具                         | 时间范围  | 数据来源        | 更新频率 |
| ---------------------------- | --------- | --------------- | -------- |
| **analyze_recent_2weeks.py** | 最近 2 周 | aimiai.com 实时 | 每日     |
| find_shannon_pattern.py      | 历史模式  | aimiai.com      | 按需     |
| analyze_with_news.py         | 实时新闻  | Yahoo Finance   | 实时     |

## ⚡ 快速命令

```bash
# 基础分析
python analyze_recent_2weeks.py

# 高标准
python analyze_recent_2weeks.py --min-score 70

# 最近7天
python analyze_recent_2weeks.py --days 7

# 导出报告
python analyze_recent_2weeks.py --export results/report.csv

# 测试 API
python test_bearer_auth.py
```

## 🎉 开始使用

### 第一次运行

1. **确认配置**

```bash
# 检查 .env 文件
cat .env

# 应该包含:
# AppId=...
# AppKey=...
# token=...
```

2. **测试连接**

```bash
python test_bearer_auth.py
```

3. **运行分析**

```bash
python analyze_recent_2weeks.py
```

### 预期结果

- ✅ 扫描 50+ 只股票
- ✅ 分析最近 2 周数据
- ✅ 显示热点股票列表
- ✅ 自动导出 CSV 报告
- ✅ 用时约 2-5 分钟

## 💡 提示

### 最佳实践

1. **每日运行**: 盘后运行，发现当日热点
2. **对比分析**: 保存每日报告，观察趋势
3. **结合基本面**: 热度高的股票需验证基本面
4. **风险控制**: 仅供参考，不构成投资建议

### 优化建议

1. **调整阈值**: 根据市场情况调整 min-score
2. **关注板块**: 重点关注热度高的板块
3. **追踪变化**: 观察热度评分的变化趋势

## 🔥 立即开始！

```bash
# Windows
RUN_2WEEKS_ANALYSIS.bat

# Mac/Linux
python analyze_recent_2weeks.py
```

---

**发现最近 2 周的热点股票！** 🚀

有问题？查看 `RECENT_2WEEKS_GUIDE.md` 获取详细帮助。
