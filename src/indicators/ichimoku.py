"""
Ichimoku Cloud Indicator
一目均衡表 (Ichimoku Kinko Hyo)

Strong bullish signal: Price crosses above cloud + Cloud turns bullish (green)
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class IchimokuResult:
    """Ichimoku calculation result"""
    tenkan_sen: float  # Conversion Line (转换线)
    kijun_sen: float   # Base Line (基准线)
    senkou_span_a: float  # Leading Span A (先行带A)
    senkou_span_b: float  # Leading Span B (先行带B)
    chikou_span: float    # Lagging Span (迟行带)

    # Cloud status
    cloud_color: str  # 'bullish' (green) or 'bearish' (red)
    cloud_thickness: float  # Cloud thickness (云层厚度)

    # Price position
    price_vs_cloud: str  # 'above', 'inside', 'below'
    price_vs_tenkan: str  # 'above' or 'below'
    price_vs_kijun: str   # 'above' or 'below'

    # Signals
    tk_cross: Optional[str]  # 'bullish' or 'bearish' or None
    cloud_breakout: bool  # Price just broke above cloud
    strong_bullish: bool  # Strong bullish signal

    # Score
    ichimoku_score: float  # 0-100


class IchimokuCalculator:
    """
    Ichimoku Cloud Calculator
    Based on HPotter's Ichimoku2c script
    """

    def __init__(self,
                 conversion_period: int = 9,
                 base_period: int = 26,
                 lagging_span2_period: int = 52,
                 displacement: int = 26):
        """
        Initialize Ichimoku Calculator

        Args:
            conversion_period: Tenkan-sen period (default: 9)
            base_period: Kijun-sen period (default: 26)
            lagging_span2_period: Senkou Span B period (default: 52)
            displacement: Displacement for Senkou Spans (default: 26)
        """
        self.conversion_period = conversion_period
        self.base_period = base_period
        self.lagging_span2_period = lagging_span2_period
        self.displacement = displacement

    def middle_donchian(self, df: pd.DataFrame, period: int, column: str = 'close') -> pd.Series:
        """
        Calculate middle Donchian channel
        (Highest High + Lowest Low) / 2
        """
        high_col = 'high' if 'high' in df.columns else column
        low_col = 'low' if 'low' in df.columns else column

        highest = df[high_col].rolling(window=period).max()
        lowest = df[low_col].rolling(window=period).min()

        return (highest + lowest) / 2

    def calculate(self, df: pd.DataFrame) -> Optional[IchimokuResult]:
        """
        Calculate Ichimoku Cloud indicators

        Args:
            df: DataFrame with OHLC data

        Returns:
            IchimokuResult or None if insufficient data
        """
        if len(df) < self.lagging_span2_period + self.displacement:
            return None

        try:
            # Make a copy to avoid modifying original
            df = df.copy()

            # 1. Tenkan-sen (Conversion Line) - 9 period
            df['tenkan_sen'] = self.middle_donchian(df, self.conversion_period)

            # 2. Kijun-sen (Base Line) - 26 period
            df['kijun_sen'] = self.middle_donchian(df, self.base_period)

            # 3. Senkou Span A (Leading Span A)
            # (Tenkan-sen + Kijun-sen) / 2, shifted forward by displacement
            df['senkou_span_a'] = (
                (df['tenkan_sen'] + df['kijun_sen']) / 2).shift(self.displacement)

            # 4. Senkou Span B (Leading Span B)
            # 52-period middle Donchian, shifted forward by displacement
            df['senkou_span_b'] = self.middle_donchian(
                df, self.lagging_span2_period).shift(self.displacement)

            # 5. Chikou Span (Lagging Span)
            # Close price shifted backward by displacement
            df['chikou_span'] = df['close'].shift(-self.displacement)

            # Get current values (latest row)
            current = df.iloc[-1]
            current_price = current['close']

            tenkan = current['tenkan_sen']
            kijun = current['kijun_sen']
            senkou_a = current['senkou_span_a']
            senkou_b = current['senkou_span_b']
            chikou = current['chikou_span']

            # Check for NaN values
            if pd.isna(tenkan) or pd.isna(kijun) or pd.isna(senkou_a) or pd.isna(senkou_b):
                return None

            # Cloud analysis
            cloud_top = max(senkou_a, senkou_b)
            cloud_bottom = min(senkou_a, senkou_b)
            cloud_thickness = abs(senkou_a - senkou_b)

            # Cloud color (bullish = green, bearish = red)
            cloud_color = 'bullish' if senkou_a > senkou_b else 'bearish'

            # Price position relative to cloud
            if current_price > cloud_top:
                price_vs_cloud = 'above'
            elif current_price < cloud_bottom:
                price_vs_cloud = 'below'
            else:
                price_vs_cloud = 'inside'

            # Price position relative to lines
            price_vs_tenkan = 'above' if current_price > tenkan else 'below'
            price_vs_kijun = 'above' if current_price > kijun else 'below'

            # TK Cross (Tenkan-Kijun cross)
            tk_cross = None
            if len(df) >= 2:
                prev = df.iloc[-2]
                if not pd.isna(prev['tenkan_sen']) and not pd.isna(prev['kijun_sen']):
                    # Bullish cross: Tenkan crosses above Kijun
                    if prev['tenkan_sen'] <= prev['kijun_sen'] and tenkan > kijun:
                        tk_cross = 'bullish'
                    # Bearish cross: Tenkan crosses below Kijun
                    elif prev['tenkan_sen'] >= prev['kijun_sen'] and tenkan < kijun:
                        tk_cross = 'bearish'

            # Cloud breakout detection
            cloud_breakout = False
            if len(df) >= 2:
                prev = df.iloc[-2]
                prev_price = prev['close']
                prev_cloud_top = max(
                    prev['senkou_span_a'], prev['senkou_span_b'])

                # Price broke above cloud
                if prev_price <= prev_cloud_top and current_price > cloud_top:
                    cloud_breakout = True

            # Strong bullish signal
            # Conditions:
            # 1. Price above cloud
            # 2. Cloud is bullish (green)
            # 3. Tenkan above Kijun
            # 4. Price above both Tenkan and Kijun
            strong_bullish = (
                price_vs_cloud == 'above' and
                cloud_color == 'bullish' and
                tenkan > kijun and
                price_vs_tenkan == 'above' and
                price_vs_kijun == 'above'
            )

            # Calculate Ichimoku score (0-100)
            score = 0

            # Price position (30 points)
            if price_vs_cloud == 'above':
                score += 30
            elif price_vs_cloud == 'inside':
                score += 15

            # Cloud color (20 points)
            if cloud_color == 'bullish':
                score += 20

            # TK relationship (20 points)
            if tenkan > kijun:
                score += 20

            # Price vs lines (15 points)
            if price_vs_tenkan == 'above':
                score += 7.5
            if price_vs_kijun == 'above':
                score += 7.5

            # Cloud breakout bonus (15 points)
            if cloud_breakout:
                score += 15

            # Strong bullish bonus (extra points)
            if strong_bullish:
                score = min(100, score + 10)

            return IchimokuResult(
                tenkan_sen=tenkan,
                kijun_sen=kijun,
                senkou_span_a=senkou_a,
                senkou_span_b=senkou_b,
                chikou_span=chikou if not pd.isna(chikou) else current_price,
                cloud_color=cloud_color,
                cloud_thickness=cloud_thickness,
                price_vs_cloud=price_vs_cloud,
                price_vs_tenkan=price_vs_tenkan,
                price_vs_kijun=price_vs_kijun,
                tk_cross=tk_cross,
                cloud_breakout=cloud_breakout,
                strong_bullish=strong_bullish,
                ichimoku_score=score
            )

        except Exception as e:
            return None

    def get_signal_description(self, result: IchimokuResult) -> str:
        """Get human-readable signal description"""
        if result.strong_bullish:
            return "🚀 强烈看涨 - 价格突破云层，云层转为看涨"
        elif result.cloud_breakout:
            return "⬆️ 云层突破 - 价格刚突破云层"
        elif result.price_vs_cloud == 'above' and result.cloud_color == 'bullish':
            return "📈 看涨 - 价格在云层上方，云层看涨"
        elif result.price_vs_cloud == 'above':
            return "🔼 偏多 - 价格在云层上方"
        elif result.price_vs_cloud == 'inside':
            return "⚖️ 震荡 - 价格在云层内"
        elif result.price_vs_cloud == 'below' and result.cloud_color == 'bearish':
            return "📉 看跌 - 价格在云层下方，云层看跌"
        else:
            return "🔽 偏空 - 价格在云层下方"
