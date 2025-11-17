# 🚀 Quick Start Guide

Get started with Shannon Stock Analyzer in 5 minutes!

## Prerequisites

1. **Python 3.9+**
2. **Tushare Token** - Configure in `.env` file

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/bluehawana/Python-TushareApi-TV-StockSelector.git
cd Python-TushareApi-TV-StockSelector
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Token

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Tushare Token
# Get your token from: https://tushare.pro/register
```

Edit `.env`:

```
TUSHARE_TOKEN=your_token_here
```

## Usage

### Method 1: One-Click Scan (Recommended)

**Windows:**

```bash
batch\run_scan.bat
```

**Linux/Mac:**

```bash
python scripts/find_all_shannon.py
```

This will automatically:

1. Download full market data (5000+ stocks, 180 days)
2. Scan for Shannon candidates
3. Export results to `results/` folder

### Method 2: Step-by-Step

```bash
# Step 1: Download data
python scripts/download/download_all_stocks.py

# Step 2: Run analysis
python scripts/find_all_shannon.py
```

### Method 3: Quick Test (24 Stocks)

```bash
python scripts/find_shannon_with_ichimoku.py
```

## View Results

Results are saved in the `results/` folder:

- `all_shannon_*.csv` - All candidates
- `super_shannon_*.csv` - Super signals (score >= 80)
- `tech_shannon_*.csv` - Technology sector candidates

## Scheduled Scanning

Run automatically at 22:00 (10 PM):

**Windows:**

```bash
tools\run_at_22pm.bat
```

**Python:**

```bash
python tools/schedule_scan.py --time 22:00
```

## Understanding the Results

### Scoring System

| Score  | Rating                     | Description                        |
| ------ | -------------------------- | ---------------------------------- |
| 80-100 | 🔥🔥🔥 Super Signal        | Extremely close to Shannon pattern |
| 60-79  | 🔥🔥 Strong Recommendation | Clear characteristics              |
| 40-59  | 🔥 Worth Watching          | Has potential                      |

### Score Breakdown

- **MCDX**: 40 points - Chip distribution analysis
- **Ichimoku**: 30 points - Cloud breakout detection
- **Volume**: 20 points - Volume surge (>= 2.5x)
- **Price**: 10 points - Price gain confirmation

### Example Output

```
[***] [T] 688005 Rongbai Tech | Battery Materials | 88 points [I]
    Price: 35.40 | Gain: +19.8% | PC: 95.3% | Volume: 2.50x
```

Legend:

- `[***]` - Super signal (80+ points)
- `[T]` - Technology sector
- `[I]` - Ichimoku strong bullish signal

## Common Issues

### Issue 1: Tushare API Rate Limit

**Error**: "You can only access this API once per hour"

**Solution**:

- Wait 1 hour between stock list requests
- Use scheduled scanning at off-peak hours (e.g., 22:00)

### Issue 2: Missing Data

**Error**: "Insufficient data"

**Solution**:

```bash
# Re-download data
python scripts/download/download_all_stocks.py
```

### Issue 3: Import Errors

**Error**: "ModuleNotFoundError"

**Solution**:

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. **Read the Documentation**

   - [Complete Guide](docs/ULTIMATE_SCAN_GUIDE.md)
   - [Shannon Criteria](docs/SHANNON_CRITERIA.md)
   - [Ichimoku Analysis](docs/ICHIMOKU_RESULTS.md)

2. **Explore Examples**

   - Check `examples/basic_usage.py`
   - Try analyzing individual stocks

3. **Customize**
   - Modify scoring weights in `scripts/find_all_shannon.py`
   - Add your own indicators
   - Adjust filtering criteria

## Tips

### Daily Workflow

```bash
# Morning: Update data
python scripts/download/download_all_stocks.py

# Afternoon: Run scan
python scripts/find_all_shannon.py

# Evening: Review results
# Open results/ folder and check CSV files
```

### Focus on Technology Stocks

Technology stocks are prioritized in the results. Look for:

- `[T]` marker in output
- `tech_shannon_*.csv` file
- Semiconductor, battery, AI sectors

### Monitor Volume

The key to Shannon pattern is volume surge:

- Look for volume ratio >= 2.5x
- Check if sustained for 2+ days
- Combine with Ichimoku strong bullish signal

## Performance

- **First Run**: 30-40 minutes (downloading data)
- **Daily Update**: 10-15 minutes (incremental)
- **Scan Time**: 10-15 minutes (5000+ stocks)

## System Requirements

- **Python**: 3.9 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for data storage
- **Internet**: Stable connection for data download

## Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/bluehawana/Python-TushareApi-TV-StockSelector/issues)
- **Examples**: See `examples/` folder

## Success Story

Our system found **Rongbai Technology (688005)** with an 88-point score:

- ✅ Ichimoku strong bullish
- ✅ MCDX golden cross (PC 95.3%)
- ✅ Volume surge (2.50x)
- ✅ Price gain (+19.8%)

This is exactly the Shannon pattern we're looking for!

---

**Ready to find the next Shannon!** 🚀

For more details, see the [Complete Guide](docs/ULTIMATE_SCAN_GUIDE.md).
