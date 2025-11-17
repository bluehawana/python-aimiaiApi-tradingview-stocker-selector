# Design Document

## Overview

The AI Stock Analyzer is a Python-based application that combines web scraping, technical analysis, and AI-powered insights to identify high-potential stocks. The system follows a modular architecture with five core components: Authentication Module, Data Collection Module, Technical Analysis Engine, AI Analysis Module, and Ranking Engine. The application will be implemented in Python using industry-standard libraries for HTTP requests, data processing, and technical analysis calculations.

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Stock Analyzer                         │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Config       │      │ Logger       │                    │
│  │ Manager      │      │ Service      │                    │
│  └──────────────┘      └──────────────┘                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Authentication Module                         │  │
│  │  - Token Manager                                      │  │
│  │  - Credential Validator                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Collection Module                        │  │
│  │  - Stock Data Scraper                                 │  │
│  │  - Rate Limiter                                       │  │
│  │  - Data Storage                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Technical Analysis Engine                     │  │
│  │  - Indicator Calculator (RSI, MACD, MA)               │  │
│  │  - Signal Generator                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI Analysis Module                            │  │
│  │  - API Client                                         │  │
│  │  - Response Parser                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Ranking Engine                                │  │
│  │  - Score Calculator                                   │  │
│  │  - Report Generator                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   ┌──────────────┐
                   │   Output     │
                   │ - Console    │
                   │ - JSON File  │
                   │ - Log Files  │
                   └──────────────┘
```

### Technology Stack

- **Language**: Python 3.8+
- **HTTP Client**: requests library
- **Data Processing**: pandas, numpy
- **Technical Analysis**: ta-lib or pandas-ta
- **Configuration**: python-dotenv, PyYAML
- **Logging**: Python logging module

## Components and Interfaces

### 1. Configuration Manager

**Purpose**: Centralized configuration management for the application.

**Responsibilities**:

- Load configuration from YAML/JSON files
- Read environment variables for sensitive credentials
- Provide default values for optional parameters
- Validate configuration completeness

**Interface**:

```python
class ConfigManager:
    def __init__(self, config_path: str)
    def get_app_id(self) -> str
    def get_app_key(self) -> str
    def get_stock_symbols(self) -> List[str]
    def get_technical_params(self) -> dict
    def validate(self) -> bool
```

**Configuration File Structure** (config.yaml):

```yaml
stocks:
  symbols: ["AAPL", "GOOGL", "MSFT", "TSLA"]

technical_analysis:
  rsi_period: 14
  sma_periods: [20, 50, 200]
  ema_periods: [12, 26]
  macd_params:
    fast: 12
    slow: 26
    signal: 9
  mcdx_params:
    length: "Auto" # Auto, 34-bar, 50-bar, 100-bar
    revision: "12" # 12 or 11

api:
  token_url: "https://aimiai.com/api/token/get"
  analysis_url: "https://aimiai.com/api/analysis"
  retry_attempts: 3
  retry_delay: 2

visualization:
  enabled: true
  web_port: 5000
  auto_refresh: 60 # seconds

output:
  console: true
  file: "results/stock_analysis.json"
  log_level: "INFO"
```

**Environment Variables**:

- `AIMIAI_APP_ID`: Application ID
- `AIMIAI_APP_KEY`: Application Key

### 7. MCDX Analysis Module (NEW)

**Purpose**: Calculate MCDX (Market Chip Distribution X) indicators to determine stock accumulation/distribution phases.

**Responsibilities**:

- Calculate Profitable Chips, Float Chips, and Locked Chips percentages
- Compute Simple Moving Averages for each chip type
- Detect Golden Cross and Death Cross signals
- Identify Bottom Catch, Oversold, and Overbought conditions
- Classify stock behavior (Accumulation, Distribution, Strong Hold, Breakout Ready)

**Components**:

#### MCDXCalculator

```python
class MCDXCalculator:
    def __init__(self, length: str = "Auto", revision: str = "12")
    def calculate_mcdx(self, stock_data: StockData) -> MCDXResult
    def calculate_profit_chips(self, prices: List[float], length: int) -> float
    def calculate_float_chips(self, prices: List[float], length: int) -> float
    def calculate_locked_chips(self, profit_chips: float, float_chips: float) -> float
    def detect_golden_cross(self, sma_pc: float, sma_lc: float) -> bool
    def detect_death_cross(self, sma_pc: float, sma_lc: float) -> bool
    def classify_behavior(self, mcdx_result: MCDXResult) -> str
```

**MCDX Data Model**:

```python
@dataclass
class MCDXResult:
    symbol: str
    timestamp: datetime
    profit_chips: float  # 0-100%
    float_chips: float   # 0-100%
    locked_chips: float  # 0-100%
    sma_profit_chips: float
    sma_float_chips: float
    sma_locked_chips: float
    golden_cross: bool
    death_cross: bool
    bottom_catch: bool
    oversold: bool
    overbought: bool
    behavior: str  # "Accumulation", "Distribution", "Strong Hold", "Breakout Ready", "Neutral"
    recommendation: str  # "BUY", "SELL", "HOLD"
    support_price: float  # MCD support level
```

**MCDX Behavior Classification Logic**:

1. **Accumulation** (BUY Signal):

   - Profit Chips < 40%
   - Locked Chips >= 20%
   - Uptrend (SMA PC > SMA LC)
   - Fund inflow detected

2. **Strong Hold** (HOLD Signal):

   - Profit Chips > 80%
   - Locked Chips < 5%
   - Uptrend maintained
   - High fund momentum

3. **Breakout Ready** (BUY Signal):

   - Profit Chips 50-80%
   - Locked Chips < 10%
   - SMA PC > SMA LC
   - Golden Cross signal

4. **Distribution** (SELL Signal):

   - Profit Chips > 85%
   - Locked Chips > 5%
   - Downtrend (SMA PC < SMA LC)
   - Fund outflow detected

5. **Neutral** (HOLD Signal):
   - None of the above conditions met

### 8. Visualization Module (NEW)

**Purpose**: Provide web-based visualization of stock analysis results with MCDX indicators.

**Technology Stack**:

- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js or Plotly.js
- **Real-time Updates**: AJAX polling or WebSocket

**Components**:

#### WebServer

```python
class WebServer:
    def __init__(self, port: int = 5000)
    def start(self)
    def stop(self)
    def update_data(self, analysis_results: List[StockAnalysis])
```

#### DashboardGenerator

```python
class DashboardGenerator:
    def generate_overview_page(self, results: List[StockAnalysis]) -> str
    def generate_stock_detail_page(self, stock: StockAnalysis) -> str
    def generate_mcdx_chart(self, mcdx_result: MCDXResult) -> dict
    def generate_comparison_table(self, results: List[StockAnalysis]) -> str
```

**Dashboard Features**:

1. **Overview Page**:

   - Summary table of all analyzed stocks
   - Color-coded recommendations (Green=BUY, Red=SELL, Yellow=HOLD)
   - MCDX behavior classification for each stock
   - Sortable by score, recommendation, behavior
   - Quick filters (Show only BUY signals, etc.)

2. **Stock Detail Page**:

   - MCDX indicator chart showing:
     - Profit Chips (red bars)
     - Float Chips (yellow bars)
     - Locked Chips (green bars)
     - SMA lines for each chip type
     - Golden Cross / Death Cross markers
     - Bottom Catch / Oversold / Overbought alerts
   - Technical indicators (RSI, MACD, Moving Averages)
   - AI analysis insights
   - Price chart with support/resistance levels
   - Historical behavior classification

3. **Comparison View**:
   - Side-by-side comparison of multiple stocks
   - MCDX metrics comparison
   - Recommendation summary
   - Risk/reward analysis

**Dashboard Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│  AI Stock Analyzer Dashboard                    [Refresh]   │
├─────────────────────────────────────────────────────────────┤
│  Filters: [All] [BUY] [SELL] [HOLD]   Sort: [Score ▼]      │
├─────────────────────────────────────────────────────────────┤
│  Stock  │ Price │ MCDX Behavior    │ Recommendation │ Score│
├─────────┼───────┼──────────────────┼────────────────┼──────┤
│  AAPL   │ $150  │ 🟢 Accumulation  │ 🟢 BUY         │ 87.5 │
│  GOOGL  │ $140  │ 🟡 Neutral       │ 🟡 HOLD        │ 65.2 │
│  MSFT   │ $380  │ 🔵 Strong Hold   │ 🟡 HOLD        │ 78.3 │
│  TSLA   │ $240  │ 🔴 Distribution  │ 🔴 SELL        │ 42.1 │
└─────────┴───────┴──────────────────┴────────────────┴──────┘

[Click any stock for detailed MCDX chart and analysis]
```

**MCDX Chart Visualization**:

```
Stock: AAPL - Accumulation Phase (BUY Signal)
┌─────────────────────────────────────────────────────────────┐
│ 100%│                                                         │
│     │ ████████████████ Locked Chips (Green)                  │
│  75%│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ Float Chips (Yellow)                  │
│     │ ░░░░░░░░░░░░░░░░ Profit Chips (Red)                    │
│  50%│ ─────────────── SMA Profit Chips (Maroon Line)         │
│     │ ─ ─ ─ ─ ─ ─ ─ ─ SMA Locked Chips (Green Line)          │
│  25%│                                                         │
│     │     BC    GC                                            │
│   0%└─────────────────────────────────────────────────────────┘
│      Day 1  Day 5  Day 10  Day 15  Day 20  Day 25  Day 30    │
└─────────────────────────────────────────────────────────────┘

Signals:
• BC (Bottom Catch) at Day 5 - Entry opportunity
• GC (Golden Cross) at Day 12 - Bullish confirmation
• Current: Profit Chips 35%, Locked Chips 28%
• Behavior: Accumulation - Smart money buying
• Support Price: $145.50 (MCD indicator)

Recommendation: 🟢 STRONG BUY
```

**API Endpoints**:

```python
GET  /                          # Dashboard overview
GET  /stock/<symbol>            # Stock detail page
GET  /api/stocks                # JSON data for all stocks
GET  /api/stock/<symbol>        # JSON data for specific stock
GET  /api/refresh               # Trigger new analysis
POST /api/config                # Update configuration
```

## Updated Data Models

### StockAnalysis (Enhanced)

```python
@dataclass
class StockAnalysis:
    symbol: str
    timestamp: datetime
    current_price: float
    stock_data: StockData
    technical_indicators: TechnicalIndicators
    mcdx_result: MCDXResult  # NEW
    ai_analysis: AIAnalysisResult
    final_score: float
    recommendation: str  # BUY, SELL, HOLD
    confidence: float
```

## Updated Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Stock Analyzer                         │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │ Config       │      │ Logger       │                    │
│  │ Manager      │      │ Service      │                    │
│  └──────────────┘      └──────────────┘                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Authentication Module                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Collection Module                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Technical Analysis Engine                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         MCDX Analysis Module (NEW)                    │  │
│  │  - MCDX Calculator                                    │  │
│  │  - Behavior Classifier                                │  │
│  │  - Signal Detector                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         AI Analysis Module                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Ranking Engine                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Visualization Module (NEW)                    │  │
│  │  - Web Server (Flask)                                 │  │
│  │  - Dashboard Generator                                │  │
│  │  - Chart Renderer                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
                   ┌──────────────┐
                   │   Output     │
                   │ - Web UI     │
                   │ - JSON API   │
                   │ - Console    │
                   │ - Log Files  │
                   └──────────────┘
```

## Updated Technology Stack

- **Language**: Python 3.8+
- **HTTP Client**: requests library
- **Data Processing**: pandas, numpy
- **Technical Analysis**: pandas-ta
- **MCDX Calculation**: Custom implementation based on Pine Script logic
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Configuration**: python-dotenv, PyYAML
- **Logging**: Python logging module

## Implementation Notes

1. **MCDX Calculation**: The MCDX indicators will be calculated using Python, translating the Pine Script logic from the mcdx_plus.pine file.

2. **Real-time Updates**: The web dashboard will auto-refresh every 60 seconds (configurable) to show latest analysis.

3. **Historical Data**: Store MCDX calculations for trend analysis and behavior pattern recognition.

4. **Mobile Responsive**: Dashboard will be mobile-friendly for on-the-go monitoring.

5. **Export Features**: Allow users to export analysis results and charts as PDF or images.
