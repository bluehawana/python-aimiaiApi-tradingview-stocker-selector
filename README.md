# 🚀 Shannon Stock Analyzer

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Find the Next Shannon** - A professional Chinese A-share technical analysis system combining MCDX chip distribution, Ichimoku Cloud breakout detection, and volume analysis to automatically scan 5000+ stocks.

## 💡 The Inspiration

### The Shannon Story

In 2024, a stock named Shannon (300475) achieved something extraordinary: **it surged from ¥30 to ¥180 in just 3 months** - a remarkable **6x gain (500% return)**. This wasn't luck. It was the perfect convergence of multiple technical indicators:

- **MCDX Golden Cross**: Profit Chips reached 100%, SMA PC at 86.65%
- **Volume Explosion**: Trading volume surged 3.0x from normal levels
- **Price Breakout**: Strong consecutive daily gains
- **Chip Lock**: Locked Chips < 15%, indicating high concentration

This case made me realize: **If we could identify this pattern early, we could catch the next Shannon!**

### From Inspiration to Implementation

I started thinking: How can we systematically find these opportunities?

1. **MCDX Analysis** - Chip distribution is key, but one indicator isn't enough
2. **Ichimoku Cloud** - Need to confirm trend and breakout signals
3. **Volume** - Must have capital flow to drive the move
4. **Automation** - Manually screening 5000 stocks is impractical

Thus, Shannon Stock Analyzer was born.

## 🎯 Core Philosophy

### Triple Technical Analysis Framework

We don't rely on a single indicator. Instead, we built a **triple verification system**:

```
Shannon Pattern = MCDX Golden Cross + Ichimoku Breakout + Volume Surge
```

#### 1️⃣ MCDX (Market Chip Distribution X) - 40 Points

**Chip distribution analysis** revealing institutional behavior:

- Profit Chips >= 80% - Most chips are profitable
- SMA PC >= 85% - Trend confirmation
- Locked Chips < 15% - Active chip movement

#### 2️⃣ Ichimoku Cloud - 30 Points

**Ichimoku Kinko Hyo**, Japan's most powerful technical indicator:

- Price breaks above cloud - Trend reversal
- Cloud turns bullish (green) - Support confirmed
- Tenkan > Kijun - Short-term stronger than long-term

> 💡 **Key Signal**: When price breaks above the cloud AND the cloud turns bullish, steep rallies typically follow!

#### 3️⃣ Volume Analysis - 20 Points

**Capital flow** validation:

- Volume ratio >= 2.5x - Massive capital inflow
- Sustained 2+ days - Not a flash in the pan

#### 4️⃣ Price Confirmation - 10 Points

**Gain verification**:

- 5-day gain >= 5%
- 10-day gain >= 10%

### Scoring System

| Score  | Rating                     | Description                                            |
| ------ | -------------------------- | ------------------------------------------------------ |
| 80-100 | 🔥🔥🔥 Super Signal        | Extremely close to Shannon pattern, highly recommended |
| 60-79  | 🔥🔥 Strong Recommendation | Clear characteristics, worth close attention           |
| 40-59  | 🔥 Worth Watching          | Potential, needs continued observation                 |

## 🎉 Success Stories

### Rongbai Technology (688005) - 88 Points 🏆

Our system successfully identified Rongbai Technology with an 88-point score (Super Signal):

```
✅ Ichimoku Strong Bullish: Price broke above cloud, cloud turned bullish
✅ MCDX Golden Cross: PC 95.3%, SMA PC 59.5%
✅ Volume Surge: 2.50x
✅ Price Gain: +19.8% (5-day)
```

**This is exactly the Shannon pattern we're looking for!**

### Other Strong Recommendations

1. **Enjie Technology (002812)** - 78 Points

   - Ichimoku strong bullish ✅
   - PC 89.9%, SMA PC 88.1% ✅
   - Waiting for volume surge

2. **Tianqi Lithium (002466)** - 76 Points

   - Ichimoku strong bullish ✅
   - PC 95.1% ✅
   - Waiting for volume surge

3. **Ganfeng Lithium (002460)** - 70 Points
   - Ichimoku strong bullish ✅
   - MCDX excellent ✅
   - Waiting for volume surge

**Discovery**: Top 4 are all lithium battery sector stocks, indicating sector momentum!

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/shannon-stock-analyzer.git
cd shannon-stock-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Token
cp .env.example .env
# Edit .env and add your Tushare Token
```

### One-Click Execution

```bash
# Windows
run_scan.bat

# Linux/Mac
python scripts/find_all_shannon.py
```

That's it! The system will automatically:

1. Download full market data (5000+ stocks, 180 days)
2. Apply Shannon triple analysis
3. Export results to `results/` folder

## 📊 Usage Examples

### Full Market Scan

```python
from scripts.find_all_shannon import AllMarketShannonFinder

# Create scanner
finder = AllMarketShannonFinder("data/tushare")

# Scan full market
results = finder.scan_all_stocks()

# View super signals
super_signals = results[results['total_score'] >= 80]
print(super_signals)
```

### Single Stock Analysis

```python
from src.mcdx.calculator import MCDXCalculator
from src.indicators.ichimoku import IchimokuCalculator
import pandas as pd

# Load data
df = pd.read_csv('data/tushare/688005.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# MCDX analysis
mcdx = MCDXCalculator()
mcdx_result = mcdx.calculate(df, '688005')
print(f"PC: {mcdx_result.profit_chips:.1f}%")

# Ichimoku analysis
ichimoku = IchimokuCalculator()
ichimoku_result = ichimoku.calculate(df)
print(f"Strong Bullish: {ichimoku_result.strong_bullish}")
```

More examples in [examples/basic_usage.py](examples/basic_usage.py)

## 🏗️ Project Architecture

```
shannon-stock-analyzer/
├── src/                    # Core code
│   ├── mcdx/              # MCDX calculator
│   │   ├── calculator.py  # Chip distribution analysis
│   │   └── volume_analyzer.py
│   ├── indicators/        # Technical indicators
│   │   └── ichimoku.py    # Ichimoku Kinko Hyo
│   └── data/              # Data loaders
│
├── scripts/               # Analysis scripts
│   ├── find_all_shannon.py          # Full market scan ⭐
│   ├── find_shannon_with_ichimoku.py # 24-stock analysis
│   └── download/                    # Data download
│
├── batch/                 # Windows batch files
├── tools/                 # Utility scripts
├── docs/                  # Documentation
└── examples/              # Example code
```

## 🔧 Technical Implementation

### MCDX Calculator

Complete Python port of the Pine Script MCDX indicator:

```python
class MCDXCalculator:
    """
    MCDX (Market Chip Distribution X) Calculator
    Calculates chip distribution to identify institutional behavior
    """

    def calculate(self, df: pd.DataFrame, symbol: str) -> MCDXResult:
        # Calculate Profit Chips, Float Chips, Locked Chips
        # Identify golden cross, death cross, double dragon patterns
        # Provide behavior analysis and trading recommendations
```

### Ichimoku Cloud

Full implementation of Ichimoku Kinko Hyo's 5 lines and cloud:

```python
class IchimokuCalculator:
    """
    Ichimoku Cloud Calculator
    Ichimoku Kinko Hyo - Japan's most powerful technical indicator
    """

    def calculate(self, df: pd.DataFrame) -> IchimokuResult:
        # Tenkan-sen (Conversion Line)
        # Kijun-sen (Base Line)
        # Senkou Span A & B (Leading Spans, forming the cloud)
        # Chikou Span (Lagging Span)

        # Identify cloud breakouts and strong bullish signals
```

### Intelligent Scoring

Comprehensive scoring across three dimensions:

```python
def calculate_shannon_score(mcdx, ichimoku, volume, price):
    score = 0

    # MCDX (40 points)
    if mcdx.profit_chips >= 90: score += 20
    if mcdx.sma_profit_chips >= 85: score += 15
    if mcdx.locked_chips < 10: score += 5

    # Ichimoku (30 points)
    score += ichimoku.ichimoku_score * 0.3

    # Volume (20 points)
    if volume_ratio >= 3.0: score += 20
    elif volume_ratio >= 2.5: score += 15

    # Price (10 points)
    if gain_5d >= 10: score += 10

    # Special bonus (15 points)
    if ichimoku.strong_bullish and mcdx.pc >= 80 and volume >= 2.0:
        score += 15

    return score
```

## 📈 Data Sources

- **Tushare** - Chinese A-share data (Token required)
- **Supported Markets**: Shanghai Stock Exchange + Shenzhen Stock Exchange
- **Coverage**: Main Board, ChiNext, STAR Market
- **Historical Data**: 180 days (configurable)

## 🎯 Use Cases

### 1. Daily Monitoring

Run daily scans to find new Shannon candidates

### 2. Sector Analysis

System automatically tracks industry distribution to discover hot sectors

### 3. Scheduled Tasks

Set to run at 22:00 (avoiding API limits):

```bash
python tools/schedule_scan.py --time 22:00
```

### 4. Quantitative Strategy

Use as a signal source for quantitative trading strategies

## 📚 Documentation

- [Quick Start](QUICKSTART.md) - Get started in 5 minutes
- [Complete Guide](docs/ULTIMATE_SCAN_GUIDE.md) - Detailed usage
- [Shannon Criteria](docs/SHANNON_CRITERIA.md) - Scoring system explained
- [Ichimoku Analysis](docs/ICHIMOKU_RESULTS.md) - Cloud breakout analysis
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## 🤝 Contributing

This project is open source and welcomes contributions from everyone!

### How to Contribute

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Contribution Ideas

- 🔧 Add new technical indicators
- 📊 Improve scoring algorithms
- 🌐 Support more data sources
- 📱 Develop web interface
- 📖 Enhance documentation
- 🐛 Fix bugs

## 🙏 Acknowledgments

### Inspiration

- **Shannon (300475)** - The stock that inspired this entire project (¥30 → ¥180 in 3 months)
- **TradingView** - Original MCDX indicator implementation
- **Ichimoku Kinko Hyo** - Wisdom from Japanese technical analysis masters

### Technology Stack

- **Python** - Powerful data analysis capabilities
- **pandas** - Data processing
- **Tushare** - Data source
- **NumPy** - Numerical computing

### Community

Thanks to all users who use and provide feedback!

## ⚠️ Disclaimer

**Important Notice**:

1. This tool is for **educational and research purposes only**
2. Does not constitute any **investment advice**
3. Historical patterns do not guarantee future performance
4. Stock market involves risks, invest cautiously
5. Please combine with fundamental analysis and market conditions
6. Recommend setting stop-loss levels and controlling risk

**Users assume all risks from investment decisions made using this tool.**

## 📄 License

This project is open source under the [MIT License](LICENSE).

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/shannon-stock-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shannon-stock-analyzer/discussions)

## 🌟 Star History

If this project helps you, please give us a ⭐️!

---

<div align="center">

**🚀 Find the Next Shannon!**

Made with ❤️ by the Shannon Stock Analyzer Team

[Quick Start](QUICKSTART.md) · [Documentation](docs/) · [Examples](examples/) · [Contributing](CONTRIBUTING.md)

</div>
