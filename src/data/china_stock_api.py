"""
China Stock Market Data API
Supports Shanghai Stock Exchange (SSE) and Shenzhen Stock Exchange (SZSE)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ChinaStockAPI:
    """
    API client for fetching China A-share stock data
    Supports multiple data sources: THS (同花顺), Tushare, AKShare
    """

    def __init__(self, source: str = "akshare"):
        """
        Initialize China Stock API

        Args:
            source: Data source - "ths", "tushare", or "akshare"
        """
        self.source = source
        self.session = requests.Session()

    def get_stock_data(self, symbol: str, days: int = 100) -> pd.DataFrame:
        """
        Get historical stock data for Chinese stocks

        Args:
            symbol: Stock code (e.g., "000001" for Ping An Bank, "600000" for SPDB)
            days: Number of days of historical data

        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        # Determine exchange based on stock code
        exchange = self._get_exchange(symbol)
        full_symbol = f"{symbol}.{exchange}"

        logger.info(f"Fetching data for {full_symbol} from {self.source}")

        if self.source == "akshare":
            return self._fetch_akshare(symbol, days)
        elif self.source == "ths":
            return self._fetch_ths(symbol, days)
        elif self.source == "tushare":
            return self._fetch_tushare(symbol, days)
        else:
            raise ValueError(f"Unsupported data source: {self.source}")

    def _get_exchange(self, symbol: str) -> str:
        """
        Determine exchange based on stock code

        Shanghai (SH): 600xxx, 601xxx, 603xxx, 688xxx (科创板)
        Shenzhen (SZ): 000xxx, 001xxx, 002xxx, 003xxx, 300xxx (创业板)
        """
        if symbol.startswith(('600', '601', '603', '688')):
            return 'SH'
        elif symbol.startswith(('000', '001', '002', '003', '300')):
            return 'SZ'
        else:
            # Default to SH
            return 'SH'

    def _fetch_akshare(self, symbol: str, days: int) -> pd.DataFrame:
        """
        Fetch data using AKShare (free, no API key required)
        """
        try:
            import akshare as ak

            # Get stock code with exchange prefix
            exchange = self._get_exchange(symbol)

            # Fetch daily data
            # AKShare uses different functions for different exchanges
            if exchange == 'SH':
                df = ak.stock_zh_a_hist(
                    symbol=symbol, period="daily", adjust="qfq")
            else:
                df = ak.stock_zh_a_hist(
                    symbol=symbol, period="daily", adjust="qfq")

            # Rename columns to standard format
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume'
            })

            # Convert date to datetime
            df['date'] = pd.to_datetime(df['date'])

            # Sort by date and get last N days
            df = df.sort_values('date').tail(days)

            # Select only needed columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

            logger.info(f"Fetched {len(df)} days of data for {symbol}")
            return df

        except ImportError:
            logger.error(
                "AKShare not installed. Install with: pip install akshare")
            raise
        except Exception as e:
            logger.error(f"Error fetching data from AKShare: {e}")
            raise

    def _fetch_ths(self, symbol: str, days: int) -> pd.DataFrame:
        """
        Fetch data using THS (同花顺) API
        Requires THS API credentials
        """
        # TODO: Implement THS API integration
        # This requires THS API key and specific endpoint
        logger.warning("THS API not yet implemented, falling back to AKShare")
        return self._fetch_akshare(symbol, days)

    def _fetch_tushare(self, symbol: str, days: int) -> pd.DataFrame:
        """
        Fetch data using Tushare API
        Requires Tushare token
        """
        try:
            import tushare as ts

            # Initialize Tushare (requires token in environment or config)
            # ts.set_token('your_token_here')
            pro = ts.pro_api()

            # Get exchange
            exchange = self._get_exchange(symbol)
            ts_code = f"{symbol}.{exchange}"

            # Calculate date range
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days+30)
                          ).strftime('%Y%m%d')

            # Fetch data
            df = pro.daily(ts_code=ts_code,
                           start_date=start_date, end_date=end_date)

            # Rename columns
            df = df.rename(columns={
                'trade_date': 'date',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'vol': 'volume'
            })

            # Convert date
            df['date'] = pd.to_datetime(df['date'])

            # Sort and limit
            df = df.sort_values('date').tail(days)

            return df[['date', 'open', 'high', 'low', 'close', 'volume']]

        except ImportError:
            logger.error(
                "Tushare not installed. Install with: pip install tushare")
            return self._fetch_akshare(symbol, days)
        except Exception as e:
            logger.error(f"Error fetching data from Tushare: {e}")
            return self._fetch_akshare(symbol, days)

    def get_stock_list(self, exchange: str = "all") -> List[Dict]:
        """
        Get list of stocks from specified exchange

        Args:
            exchange: "SH", "SZ", or "all"

        Returns:
            List of dicts with stock info
        """
        try:
            import akshare as ak

            # Get stock list
            df = ak.stock_zh_a_spot_em()

            # Filter by exchange if specified
            if exchange.upper() == "SH":
                df = df[df['代码'].str.startswith(('600', '601', '603', '688'))]
            elif exchange.upper() == "SZ":
                df = df[df['代码'].str.startswith(
                    ('000', '001', '002', '003', '300'))]

            # Convert to list of dicts
            stocks = []
            for _, row in df.iterrows():
                stocks.append({
                    'code': row['代码'],
                    'name': row['名称'],
                    'price': row['最新价'],
                    'change_pct': row['涨跌幅']
                })

            return stocks

        except Exception as e:
            logger.error(f"Error fetching stock list: {e}")
            return []

    def get_realtime_price(self, symbol: str) -> Optional[float]:
        """
        Get real-time price for a stock

        Args:
            symbol: Stock code

        Returns:
            Current price or None
        """
        try:
            import akshare as ak

            df = ak.stock_zh_a_spot_em()
            stock = df[df['代码'] == symbol]

            if not stock.empty:
                return float(stock.iloc[0]['最新价'])

            return None

        except Exception as e:
            logger.error(f"Error fetching realtime price: {e}")
            return None


# Popular China A-share stocks for testing
POPULAR_CHINA_STOCKS = [
    # Shanghai Stock Exchange
    "600000",  # 浦发银行 SPDB
    "600036",  # 招商银行 China Merchants Bank
    "600519",  # 贵州茅台 Kweichow Moutai
    "600887",  # 伊利股份 Inner Mongolia Yili
    "601318",  # 中国平安 Ping An Insurance
    "601398",  # 工商银行 ICBC
    "601857",  # 中国石油 PetroChina
    "601988",  # 中国银行 Bank of China

    # Shenzhen Stock Exchange
    "000001",  # 平安银行 Ping An Bank
    "000002",  # 万科A Vanke
    "000333",  # 美的集团 Midea Group
    "000858",  # 五粮液 Wuliangye
    "002594",  # 比亚迪 BYD
    "002714",  # 牧原股份 Muyuan Foods
    "300059",  # 东方财富 East Money
    "300750",  # 宁德时代 CATL
]
