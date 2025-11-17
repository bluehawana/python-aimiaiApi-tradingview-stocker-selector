# Changelog

All notable changes to Shannon Stock Analyzer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-17

### 🎉 Initial Release

The first production-ready release of Shannon Stock Analyzer!

### ✨ Added

#### Core Features

- **MCDX Calculator** - Complete implementation of Market Chip Distribution X indicator
  - Profit Chips, Float Chips, Locked Chips calculation
  - Golden Cross and Death Cross detection
  - Behavior analysis and trading recommendations
- **Ichimoku Cloud Indicator** - Full implementation of Ichimoku Kinko Hyo

  - Tenkan-sen (Conversion Line)
  - Kijun-sen (Base Line)
  - Senkou Span A & B (Leading Spans / Cloud)
  - Chikou Span (Lagging Span)
  - Cloud breakout detection
  - Strong bullish signal identification

- **Volume Analysis** - Advanced volume surge detection

  - 30-day moving average comparison
  - Volume ratio calculation
  - Surge day counting
  - Trend analysis

- **Shannon Scoring System** - Comprehensive 100-point scoring
  - MCDX: 40 points
  - Ichimoku: 30 points
  - Volume: 20 points
  - Price: 10 points
  - Special bonus: 15 points

#### Scanning Capabilities

- **Full Market Scanner** - Scan 5000+ A-share stocks

  - Shanghai Stock Exchange support
  - Shenzhen Stock Exchange support
  - 180-day historical data analysis
  - Automatic filtering (Golden Cross + Score >= 40)

- **24-Stock Quick Scan** - Fast analysis of known golden cross stocks
  - Pre-filtered quality stocks
  - Detailed analysis output

#### Automation

- **One-Click Execution** - `run_scan.bat` for Windows
- **Scheduled Tasks** - Run at specific times (e.g., 22:00)
- **Auto Export** - Results automatically saved to CSV

#### Data Management

- **Tushare Integration** - Primary data source
- **Incremental Updates** - Skip existing data
- **180-Day History** - Sufficient for Ichimoku analysis

### 📊 Results

#### Discovered Signals

- **Super Signal (88 points)**: 688005 (容百科技)

  - Ichimoku strong bullish ✅
  - MCDX golden cross (PC 95.3%) ✅
  - Volume surge (2.50x) ✅
  - Price gain (+19.8%) ✅

- **Strong Recommendations (70-78 points)**:
  - 002812 (恩捷股份) - 78 points
  - 002466 (天齐锂业) - 76 points
  - 002460 (赣锋锂业) - 70 points

### 📚 Documentation

- Comprehensive README with inspiration story
- QUICKSTART guide for new users
- ULTIMATE_SCAN_GUIDE for detailed usage
- SHANNON_CRITERIA for scoring explanation
- ICHIMOKU_RESULTS for cloud analysis
- CONTRIBUTING guide for developers
- Example code in `examples/`

### 🏗️ Project Structure

- Professional folder organization
- Separated scripts by function
- Legacy code preserved in `legacy/` folders
- Clean root directory

### 🔧 Tools

- Scheduled scan support
- Cleanup and reorganization scripts
- GitHub Actions CI/CD setup

### 📦 Dependencies

- pandas >= 2.0.0
- numpy >= 1.21.0
- tushare >= 1.4.0
- python-dotenv >= 0.19.0
- schedule >= 1.1.0

### 🔒 Security

- `.env` for credentials (gitignored)
- `.env.example` template provided
- No hardcoded secrets

### 🎨 Code Quality

- Type hints throughout
- Docstrings for all functions
- Error handling
- Encoding compatibility (Windows Chinese)

## [Unreleased]

### 🚀 Planned Features

- [ ] Web dashboard interface
- [ ] Real-time monitoring
- [ ] Email/WeChat notifications
- [ ] More technical indicators (RSI, MACD, etc.)
- [ ] Backtesting framework
- [ ] Portfolio management
- [ ] Multi-language support (English)

### 🐛 Known Issues

- Tushare API rate limit (1 request per hour for stock list)
- Windows console encoding issues with emojis (fixed with ASCII alternatives)

---

## Version History

- **1.0.0** (2025-11-17) - Initial release
  - Full Shannon pattern detection
  - MCDX + Ichimoku + Volume analysis
  - Full market scanning capability
  - Professional project structure

---

**Legend**:

- ✨ Added - New features
- 🔧 Changed - Changes in existing functionality
- 🐛 Fixed - Bug fixes
- 🗑️ Removed - Removed features
- 🔒 Security - Security improvements
- 📚 Documentation - Documentation changes
