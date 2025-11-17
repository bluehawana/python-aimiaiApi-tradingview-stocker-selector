# AI Stock Analyzer with MCDX Visualization

An intelligent stock analysis application that combines technical analysis, MCDX (Market Chip Distribution X) indicators, and AI-powered insights from aimiai.com to identify high-potential stocks with visual dashboard.

## Features

- 🔐 Automatic authentication with aimiai.com API
- 📊 Real-time stock data collection
- 📈 Technical indicator calculations (RSI, MACD, Moving Averages)
- 🎯 MCDX Analysis (Profit/Float/Locked Chips, Golden/Death Cross)
- 🤖 AI-powered stock analysis
- 🏆 Intelligent stock ranking system
- 📊 **Web Dashboard** - Visual interface showing MCDX charts and buy/sell/hold signals
- 📝 Comprehensive reporting

## MCDX Indicators

The MCDX (Market Chip Distribution X) system analyzes market chip distribution to identify:

- **Profit Chips**: Percentage of shares held at profit
- **Float Chips**: Percentage of freely trading shares
- **Locked Chips**: Percentage of shares held long-term

### MCDX Signals

- **🟢 Accumulation** (BUY): Smart money is buying, low profit chips, high locked chips
- **🔵 Strong Hold** (HOLD): High profit chips, very low locked chips, strong uptrend
- **🟡 Breakout Ready** (BUY): Moderate profit chips, low locked chips, golden cross
- **🔴 Distribution** (SELL): High profit chips, downtrend, fund outflow
- **⚪ Neutral** (HOLD): No clear signal

### Special Alerts

- **GC (Golden Cross)**: SMA Profit Chips crosses above SMA Locked Chips - Bullish
- **DC (Death Cross)**: SMA Profit Chips crosses below SMA Locked Chips - Bearish
- **BC (Bottom Catch)**: Potential bottom formation - Entry opportunity
- **OS (Oversold)**: Stock is oversold - Potential bounce
- **OB (Overbought)**: Stock is overbought - Potential pullback

## Prerequisites

- Python 3.8 or higher
- aimiai.com API credentials (appId and appKey)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ai-stock-analyzer
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your credentials:

   - Edit `.env` file
   - Get your credentials from https://aimiai.com/console (API Keys tab)
   - Add your `AIMIAI_APP_ID` and `AIMIAI_APP_KEY` to `.env`

5. (Optional) Customize configuration:
   - Edit `config.yaml` to adjust stock symbols, MCDX parameters, etc.

## Usage

### Run with Web Dashboard (Recommended)

```bash
python main.py --web
```

Then open your browser to: `http://localhost:5000`

The dashboard will show:

- Overview table with all stocks and their MCDX behavior
- Color-coded recommendations (🟢 BUY, 🔴 SELL, 🟡 HOLD)
- Click any stock to see detailed MCDX chart
- Auto-refresh every 60 seconds

### Run Console Only

```bash
python main.py
```

Results will be saved to `results/stock_analysis.json` and displayed in the console.

## Configuration

### Environment Variables (.env)

- `AIMIAI_APP_ID`: Your aimiai.com application ID
- `AIMIAI_APP_KEY`: Your aimiai.com application key

### Configuration File (config.yaml)

- `stocks.symbols`: List of stock symbols to analyze
- `technical_analysis.mcdx_params`: MCDX calculation parameters
  - `length`: Auto, 34-bar, 50-bar, 100-bar (Auto recommended for new stocks)
  - `revision`: 12 or 11 (12 is latest)
- `visualization.enabled`: Enable/disable web dashboard
- `visualization.port`: Web server port (default: 5000)
- `visualization.auto_refresh`: Dashboard refresh interval in seconds

## Project Structure

```
ai-stock-analyzer/
├── src/
│   ├── auth/           # Authentication module
│   ├── data/           # Data collection module
│   ├── analysis/       # Technical analysis engine
│   ├── mcdx/           # MCDX analysis module (NEW)
│   ├── ai/             # AI analysis module
│   ├── ranking/        # Ranking engine
│   ├── visualization/  # Web dashboard (NEW)
│   └── utils/          # Utilities (config, logging)
├── templates/          # HTML templates for web dashboard
├── static/             # CSS, JS, images for web dashboard
├── logs/               # Log files
├── results/            # Analysis results
├── mcdx_plus.pine      # Pine Script reference (TradingView)
├── config.yaml         # Configuration file
├── .env                # Environment variables (not in git)
├── requirements.txt    # Python dependencies
└── main.py            # Entry point
```

## Dashboard Features

### Overview Page

- Summary table of all analyzed stocks
- MCDX behavior classification for each stock
- Sortable by score, recommendation, behavior
- Quick filters (Show only BUY signals, etc.)

### Stock Detail Page

- MCDX indicator chart showing:
  - Profit Chips (red bars)
  - Float Chips (yellow bars)
  - Locked Chips (green bars)
  - SMA lines for each chip type
  - Golden Cross / Death Cross markers
  - Bottom Catch / Oversold / Overbought alerts
- Technical indicators (RSI, MACD, Moving Averages)
- AI analysis insights
- Support price level (MCD indicator)
- Historical behavior classification

## Understanding MCDX

MCDX is based on the concept that stock price movements are driven by the distribution of "chips" (shares) among different types of holders:

1. **Profitable Holders**: Those who bought at lower prices and are in profit
2. **Floating Holders**: Short-term traders who can sell anytime
3. **Locked Holders**: Long-term investors who won't sell easily

By analyzing the percentage and movement of these chips, MCDX can identify:

- When smart money is accumulating (BUY signal)
- When distribution is happening (SELL signal)
- When a breakout is imminent (BUY signal)
- When to hold strong positions (HOLD signal)

## Security

- Never commit `.env` file to version control
- Keep your API credentials secure
- Tokens are stored in memory only and never persisted to disk
- Web dashboard is local by default (127.0.0.1)

## License

MIT License
