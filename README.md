# 🚀 Shannon Stock Analyzer

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **寻找下一个 Shannon** - 一个专业的 A 股技术分析系统，结合 MCDX 筹码分布、Ichimoku Cloud 云层突破和成交量分析，自动扫描全市场 5000+只股票。

## 💡 灵感来源

### Shannon 的故事

2024 年 9 月 11-12 日，一只名为 Shannon（002870）的股票在两天内暴涨超过 20%。这不是偶然，而是多个技术指标完美共振的结果：

- **MCDX 金叉**: Profit Chips 达到 100%，SMA PC 86.65%
- **成交量暴增**: 从 30M 激增到 89M，3.0 倍放量
- **价格突破**: 连续两天强势上涨
- **筹码锁定**: Locked Chips < 15%，筹码高度集中

这个案例让我意识到：**如果能提前识别这种模式，就能抓住下一个 Shannon！**

### 从灵感到实现

我开始思考：如何系统化地寻找这种机会？

1. **MCDX 分析** - 筹码分布是关键，但单一指标不够
2. **Ichimoku Cloud** - 需要确认趋势和突破信号
3. **成交量** - 必须有资金推动
4. **自动化** - 人工筛选 5000 只股票不现实

于是，Shannon Stock Analyzer 诞生了。

## 🎯 核心理念

### 三重技术分析框架

我们不依赖单一指标，而是构建了一个**三重验证系统**：

```
Shannon模式 = MCDX金叉 + Ichimoku突破 + 成交量暴增
```

#### 1️⃣ MCDX (Market Chip Distribution X) - 40 分

**筹码分布分析**，揭示主力行为：

- Profit Chips >= 80% - 大部分筹码获利
- SMA PC >= 85% - 趋势确认
- Locked Chips < 15% - 筹码活跃

#### 2️⃣ Ichimoku Cloud - 30 分

**一目均衡表**，日本最强技术指标：

- 价格突破云层 - 趋势反转
- 云层转为看涨（绿色）- 支撑确认
- Tenkan > Kijun - 短期强于长期

> 💡 **关键信号**: 当价格突破云层且云层转为看涨时，通常会有陡峭上涨！

#### 3️⃣ 成交量分析 - 20 分

**资金推动**，验证真实性：

- 成交量比率 >= 2.5x - 资金大量涌入
- 持续 2 天以上 - 不是昙花一现

#### 4️⃣ 价格确认 - 10 分

**涨幅验证**：

- 5 日涨幅 >= 5%
- 10 日涨幅 >= 10%

### 评分系统

| 评分   | 评级            | 说明                            |
| ------ | --------------- | ------------------------------- |
| 80-100 | 🔥🔥🔥 超级信号 | 极度接近 Shannon 模式，强烈推荐 |
| 60-79  | 🔥🔥 强烈推荐   | 具有明显特征，值得重点关注      |
| 40-59  | 🔥 值得关注     | 有潜力，需要继续观察            |

## 🎉 成功案例

### 容百科技 (688005) - 88 分 🏆

我们的系统成功识别出容百科技，评分 88 分（超级信号）：

```
✅ Ichimoku强势: 价格突破云层，云层转为看涨
✅ MCDX金叉: PC 95.3%, SMA PC 59.5%
✅ 成交量达标: 2.50x
✅ 价格涨幅: +19.8% (5日)
```

**这正是我们要找的 Shannon 模式！**

### 其他强烈推荐

1. **恩捷股份 (002812)** - 78 分

   - Ichimoku 强势 ✅
   - PC 89.9%, SMA PC 88.1% ✅
   - 等待成交量放大

2. **天齐锂业 (002466)** - 76 分

   - Ichimoku 强势 ✅
   - PC 95.1% ✅
   - 等待成交量放大

3. **赣锋锂业 (002460)** - 70 分
   - Ichimoku 强势 ✅
   - MCDX 优秀 ✅
   - 等待成交量放大

**发现**: 前 4 名都是锂电池板块，说明板块共振！

## 🚀 快速开始

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/shannon-stock-analyzer.git
cd shannon-stock-analyzer

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置Token
cp .env.example .env
# 编辑 .env，添加你的 Tushare Token
```

### 一键运行

```bash
# Windows
run_scan.bat

# Linux/Mac
python scripts/find_all_shannon.py
```

就这么简单！系统会自动：

1. 下载全市场数据（5000+只股票，180 天）
2. 应用 Shannon 三重分析
3. 导出结果到 `results/` 文件夹

## 📊 使用示例

### 全市场扫描

```python
from scripts.find_all_shannon import AllMarketShannonFinder

# 创建扫描器
finder = AllMarketShannonFinder("data/tushare")

# 扫描全市场
results = finder.scan_all_stocks()

# 查看超级信号
super_signals = results[results['total_score'] >= 80]
print(super_signals)
```

### 单只股票分析

```python
from src.mcdx.calculator import MCDXCalculator
from src.indicators.ichimoku import IchimokuCalculator
import pandas as pd

# 加载数据
df = pd.read_csv('data/tushare/688005.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# MCDX分析
mcdx = MCDXCalculator()
mcdx_result = mcdx.calculate(df, '688005')
print(f"PC: {mcdx_result.profit_chips:.1f}%")

# Ichimoku分析
ichimoku = IchimokuCalculator()
ichimoku_result = ichimoku.calculate(df)
print(f"强烈看涨: {ichimoku_result.strong_bullish}")
```

更多示例请查看 [examples/basic_usage.py](examples/basic_usage.py)

## 🏗️ 项目架构

```
shannon-stock-analyzer/
├── src/                    # 核心代码
│   ├── mcdx/              # MCDX计算器
│   │   ├── calculator.py  # 筹码分布分析
│   │   └── volume_analyzer.py
│   ├── indicators/        # 技术指标
│   │   └── ichimoku.py    # 一目均衡表
│   └── data/              # 数据加载器
│
├── scripts/               # 分析脚本
│   ├── find_all_shannon.py          # 全市场扫描 ⭐
│   ├── find_shannon_with_ichimoku.py # 24只股票分析
│   └── download/                    # 数据下载
│
├── batch/                 # Windows批处理
├── tools/                 # 工具脚本
├── docs/                  # 文档
└── examples/              # 示例代码
```

## 🔧 技术实现

### MCDX 计算器

基于 Pine Script 的 MCDX 指标，完整移植到 Python：

```python
class MCDXCalculator:
    """
    MCDX (Market Chip Distribution X) Calculator
    计算筹码分布，识别主力行为
    """

    def calculate(self, df: pd.DataFrame, symbol: str) -> MCDXResult:
        # 计算Profit Chips, Float Chips, Locked Chips
        # 识别金叉、死叉、双龙出海等形态
        # 给出行为分析和交易建议
```

### Ichimoku Cloud

完整实现一目均衡表的 5 条线和云层：

```python
class IchimokuCalculator:
    """
    Ichimoku Cloud Calculator
    一目均衡表 - 日本最强技术指标
    """

    def calculate(self, df: pd.DataFrame) -> IchimokuResult:
        # Tenkan-sen (转换线)
        # Kijun-sen (基准线)
        # Senkou Span A & B (先行带，形成云层)
        # Chikou Span (迟行带)

        # 识别云层突破和强烈看涨信号
```

### 智能评分

综合三个维度，自动计算 Shannon 评分：

```python
def calculate_shannon_score(mcdx, ichimoku, volume, price):
    score = 0

    # MCDX (40分)
    if mcdx.profit_chips >= 90: score += 20
    if mcdx.sma_profit_chips >= 85: score += 15
    if mcdx.locked_chips < 10: score += 5

    # Ichimoku (30分)
    score += ichimoku.ichimoku_score * 0.3

    # 成交量 (20分)
    if volume_ratio >= 3.0: score += 20
    elif volume_ratio >= 2.5: score += 15

    # 价格 (10分)
    if gain_5d >= 10: score += 10

    # 特殊加分 (15分)
    if ichimoku.strong_bullish and mcdx.pc >= 80 and volume >= 2.0:
        score += 15

    return score
```

## 📈 数据来源

- **Tushare** - 中国 A 股数据（需要 Token）
- **支持市场**: 上海证券交易所 + 深圳证券交易所
- **数据范围**: 主板、创业板、科创板
- **历史数据**: 180 天（可配置）

## 🎯 使用场景

### 1. 日常监控

每日运行扫描，寻找新的 Shannon 候选

### 2. 板块分析

系统自动统计行业分布，发现热点板块

### 3. 定时任务

设置 22:00 自动运行（避开 API 限制）：

```bash
python tools/schedule_scan.py --time 22:00
```

### 4. 量化策略

作为量化交易策略的信号源

## 📚 文档

- [快速开始](QUICKSTART.md) - 5 分钟上手
- [完整指南](docs/ULTIMATE_SCAN_GUIDE.md) - 详细使用说明
- [Shannon 标准](docs/SHANNON_CRITERIA.md) - 评分标准详解
- [Ichimoku 分析](docs/ICHIMOKU_RESULTS.md) - 云层突破解析
- [贡献指南](CONTRIBUTING.md) - 如何参与开发

## 🤝 贡献

这个项目是开源的，欢迎所有人贡献！

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献方向

- 🔧 添加新的技术指标
- 📊 改进评分算法
- 🌐 支持更多数据源
- 📱 开发 Web 界面
- 📖 完善文档
- 🐛 修复 Bug

## 🙏 致谢

### 灵感来源

- **Shannon (002870)** - 启发了整个项目
- **TradingView** - MCDX 指标的原始实现
- **Ichimoku Kinko Hyo** - 日本技术分析大师的智慧

### 技术栈

- **Python** - 强大的数据分析能力
- **pandas** - 数据处理
- **Tushare** - 数据源
- **NumPy** - 数值计算

### 社区

感谢所有使用和反馈的用户！

## ⚠️ 免责声明

**重要提示**：

1. 本工具仅供**学习和研究**使用
2. 不构成任何**投资建议**
3. 历史模式不代表未来表现
4. 股市有风险，投资需谨慎
5. 请结合基本面分析和市场环境
6. 建议设置止损位，控制风险

**使用本工具进行投资决策的风险由用户自行承担。**

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源。

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/yourusername/shannon-stock-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shannon-stock-analyzer/discussions)

## 🌟 Star History

如果这个项目对你有帮助，请给我们一个 ⭐️！

---

<div align="center">

**🚀 寻找下一个 Shannon！**

Made with ❤️ by the Shannon Stock Analyzer Team

[快速开始](QUICKSTART.md) · [文档](docs/) · [示例](examples/) · [贡献](CONTRIBUTING.md)

</div>
