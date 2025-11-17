"""
MCDX (Market Chip Distribution X) Calculator
Translated from Pine Script mcdx_plus.pine to Python
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class MCDXResult:
    """MCDX calculation result"""
    symbol: str
    profit_chips: float  # 0-100%
    float_chips: float   # 0-100%
    locked_chips: float  # 0-100%
    sma_profit_chips: float
    sma_float_chips: float
    sma_locked_chips: float
    golden_cross: bool
    death_cross: bool
    double_dragon: bool
    bottom_catch: bool
    oversold: bool
    overbought: bool
    behavior: str
    recommendation: str
    support_price: float
    confidence: float


class MCDXCalculator:
    """
    MCDX Calculator - Revision 12
    Based on mcdx_plus.pine script
    """

    def __init__(self, length: str = "Auto", revision: str = "12",
                 sma_pc_len: int = 10, sma_fc_len: int = 10, sma_lc_len: int = 10):
        """
        Initialize MCDX Calculator

        Args:
            length: "Auto", "34-bar", "50-bar", "100-bar", or manual number
            revision: "12" or "11"
            sma_pc_len: SMA length for profit chips
            sma_fc_len: SMA length for float chips
            sma_lc_len: SMA length for locked chips
        """
        self.length_mode = length
        self.revision = revision
        self.sma_pc_len = sma_pc_len
        self.sma_fc_len = sma_fc_len
        self.sma_lc_len = sma_lc_len

    def calculate(self, df: pd.DataFrame, symbol: str) -> MCDXResult:
        """
        Calculate MCDX indicators for stock data

        Args:
            df: DataFrame with columns: date, open, high, low, close, volume
            symbol: Stock symbol

        Returns:
            MCDXResult object
        """
        # Ensure data is sorted by date
        df = df.sort_values('date').reset_index(drop=True)

        # Determine length
        bar_count = len(df)
        length = self._determine_length(bar_count)

        logger.info(
            f"Calculating MCDX for {symbol} with length={length}, bars={bar_count}")

        # Calculate MCDX indicators
        if self.revision == "12":
            pc, fc, lc = self._calculate_mcdx_r12(df, length)
        else:
            pc, fc, lc = self._calculate_mcdx_r11(df, length)

        # Calculate SMAs
        sma_pc = self._sma(pc, self.sma_pc_len)
        sma_fc = self._sma(fc, self.sma_fc_len)
        sma_lc = self._sma(lc, self.sma_lc_len)

        # Get current values (last bar)
        current_pc = pc.iloc[-1] if len(pc) > 0 else 0
        current_fc = fc.iloc[-1] if len(fc) > 0 else 0
        current_lc = lc.iloc[-1] if len(lc) > 0 else 0
        current_sma_pc = sma_pc.iloc[-1] if len(sma_pc) > 0 else 0
        current_sma_fc = sma_fc.iloc[-1] if len(sma_fc) > 0 else 0
        current_sma_lc = sma_lc.iloc[-1] if len(sma_lc) > 0 else 0

        # Detect signals
        golden_cross = self._detect_golden_cross(sma_pc, sma_lc)
        death_cross = self._detect_death_cross(sma_pc, sma_lc)
        double_dragon = self._detect_double_dragon(df, pc, sma_pc)
        bottom_catch = self._detect_bottom_catch(df, pc, lc, sma_pc, sma_lc)
        oversold = self._detect_oversold(df)
        overbought = self._detect_overbought(df)

        # Classify behavior
        behavior = self._classify_behavior(
            current_pc, current_lc, current_sma_pc, current_sma_lc,
            golden_cross, death_cross
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(
            behavior, golden_cross, death_cross, bottom_catch, oversold, overbought
        )

        # Calculate support price (MCD)
        support_price = self._calculate_support_price(df, current_pc, length)

        # Calculate confidence
        confidence = self._calculate_confidence(
            current_pc, current_lc, current_sma_pc, current_sma_lc, behavior
        )

        return MCDXResult(
            symbol=symbol,
            profit_chips=current_pc,
            float_chips=current_fc,
            locked_chips=current_lc,
            sma_profit_chips=current_sma_pc,
            sma_float_chips=current_sma_fc,
            sma_locked_chips=current_sma_lc,
            golden_cross=golden_cross,
            death_cross=death_cross,
            double_dragon=double_dragon,
            bottom_catch=bottom_catch,
            oversold=oversold,
            overbought=overbought,
            behavior=behavior,
            recommendation=recommendation,
            support_price=support_price,
            confidence=confidence
        )

    def _determine_length(self, bar_count: int) -> int:
        """Determine MCDX calculation length based on mode and bar count"""
        if self.length_mode == "Auto":
            return min(bar_count, 100) if bar_count >= 100 else bar_count
        elif self.length_mode == "34-bar":
            return 34
        elif self.length_mode == "50-bar":
            return 50
        elif self.length_mode == "100-bar":
            return 100
        else:
            try:
                return int(self.length_mode)
            except:
                return min(bar_count, 100)

    def _calculate_mcdx_r12(self, df: pd.DataFrame, length: int) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MCDX Revision 12

        Returns:
            Tuple of (profit_chips, float_chips, locked_chips) as pandas Series
        """
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        bar_count = len(df)

        # Initialize arrays
        profit_chips = np.zeros(bar_count)
        float_chips = np.zeros(bar_count)
        locked_chips = np.zeros(bar_count)

        for i in range(bar_count):
            if i < 2:  # Need at least 3 bars
                continue

            # Determine actual length for this bar
            actual_len = min(length, i + 1)

            # Calculate profit chips
            pcr_mult = 0.98 if i <= 100 else 0.96
            xpr = close[i] * pcr_mult
            profit_chips[i] = self._fmcdx(xpr, low[max(0, i-actual_len+1):i+1],
                                          high[max(0, i-actual_len+1):i+1])

            # Calculate float chips (upper bound)
            fcr_mult = 1.02 if i <= 100 else 1.04
            xfur = close[i] * fcr_mult
            fcur = self._fmcdx(xfur, low[max(0, i-actual_len+1):i+1],
                               high[max(0, i-actual_len+1):i+1])

            # Float chips = upper bound - profit chips
            float_chips[i] = max(0, min(100, fcur - profit_chips[i]))

            # Locked chips = 100 - (profit + float)
            locked_chips[i] = max(0, 100 - fcur)

        return (pd.Series(profit_chips, index=df.index),
                pd.Series(float_chips, index=df.index),
                pd.Series(locked_chips, index=df.index))

    def _calculate_mcdx_r11(self, df: pd.DataFrame, length: int) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MCDX Revision 11 (legacy)
        Simplified version for compatibility
        """
        # For now, use R12 logic
        # Full R11 implementation can be added if needed
        return self._calculate_mcdx_r12(df, length)

    def _fmcdx(self, x: float, low_range: np.ndarray, high_range: np.ndarray) -> float:
        """
        MCDX core calculation function
        Translates fmcdx from Pine Script

        Args:
            x: Current value (adjusted close)
            low_range: Array of lows in the range
            high_range: Array of highs in the range

        Returns:
            MCDX value (0-100)
        """
        if len(low_range) == 0 or len(high_range) == 0:
            return 0.0

        lo = np.min(low_range)
        hi = np.max(high_range)

        # Avoid division by zero
        step = max((hi - lo), 0.01) / 100.0

        # Calculate percentage
        pct = (x - lo) / step

        # Clamp to 0-100
        return max(0.0, min(100.0, pct))

    def _sma(self, series: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return series.rolling(window=period, min_periods=1).mean()

    def _detect_golden_cross(self, sma_pc: pd.Series, sma_lc: pd.Series) -> bool:
        """Detect Golden Cross: SMA PC crosses above SMA LC"""
        if len(sma_pc) < 2 or len(sma_lc) < 2:
            return False

        # Check if crossover happened in last bar
        prev_pc = sma_pc.iloc[-2]
        curr_pc = sma_pc.iloc[-1]
        prev_lc = sma_lc.iloc[-2]
        curr_lc = sma_lc.iloc[-1]

        return prev_pc <= prev_lc and curr_pc > curr_lc

    def _detect_death_cross(self, sma_pc: pd.Series, sma_lc: pd.Series) -> bool:
        """Detect Death Cross: SMA PC crosses below SMA LC"""
        if len(sma_pc) < 2 or len(sma_lc) < 2:
            return False

        prev_pc = sma_pc.iloc[-2]
        curr_pc = sma_pc.iloc[-1]
        prev_lc = sma_lc.iloc[-2]
        curr_lc = sma_lc.iloc[-1]

        return prev_pc >= prev_lc and curr_pc < curr_lc

    def _detect_double_dragon(self, df: pd.DataFrame, pc: pd.Series, sma_pc: pd.Series) -> bool:
        """Detect Double Dragon signal"""
        if len(pc) < 2 or len(sma_pc) < 2:
            return False

        close = df['close'].iloc[-1]
        open_price = df['open'].iloc[-1]
        curr_pc = pc.iloc[-1]
        prev_pc = pc.iloc[-2]
        curr_sma_pc = sma_pc.iloc[-1]

        # Conditions for Double Dragon
        cond1 = curr_pc > curr_sma_pc
        cond2 = close > open_price
        cond3 = prev_pc < 75 and curr_pc > 75

        return cond1 and cond2 and cond3

    def _detect_bottom_catch(self, df: pd.DataFrame, pc: pd.Series, lc: pd.Series,
                             sma_pc: pd.Series, sma_lc: pd.Series) -> bool:
        """Detect Bottom Catch signal"""
        if len(pc) < 3 or len(lc) < 3:
            return False

        curr_pc = pc.iloc[-1]
        prev_pc = pc.iloc[-2]
        prev2_pc = pc.iloc[-3]

        curr_lc = lc.iloc[-1]
        prev_lc = lc.iloc[-2]
        prev2_lc = lc.iloc[-3]

        curr_sma_pc = sma_pc.iloc[-1]

        # PC forming a bottom
        pc_bottom = prev2_pc > prev_pc and prev_pc < curr_pc and curr_pc > curr_sma_pc

        # LC forming a top
        lc_top = prev2_lc < prev_lc and prev_lc > curr_lc and curr_lc > 0

        return pc_bottom and lc_top

    def _detect_oversold(self, df: pd.DataFrame) -> bool:
        """Detect Oversold condition"""
        if len(df) < 20:
            return False

        close = df['close'].iloc[-1]
        sma20 = df['close'].rolling(20).mean().iloc[-1]

        # Simplified oversold: price significantly below SMA20
        return close < sma20 * 0.95

    def _detect_overbought(self, df: pd.DataFrame) -> bool:
        """Detect Overbought condition"""
        if len(df) < 20:
            return False

        close = df['close'].iloc[-1]
        sma20 = df['close'].rolling(20).mean().iloc[-1]

        # Simplified overbought: price significantly above SMA20
        return close > sma20 * 1.05

    def _classify_behavior(self, pc: float, lc: float, sma_pc: float, sma_lc: float,
                           golden_cross: bool, death_cross: bool) -> str:
        """
        Classify stock behavior based on MCDX indicators

        Returns:
            "Accumulation", "Distribution", "Strong Hold", "Breakout Ready", or "Neutral"
        """
        uptrend = sma_pc > sma_lc
        downtrend = sma_pc < sma_lc

        # Accumulation: Low PC, High LC, Uptrend
        if pc < 40 and lc >= 20 and uptrend:
            return "Accumulation"

        # Strong Hold: High PC, Very Low LC, Uptrend
        if pc > 80 and lc < 5 and uptrend:
            return "Strong Hold"

        # Breakout Ready: Medium PC, Low LC, Uptrend
        if 50 < pc < 80 and lc < 10 and uptrend:
            return "Breakout Ready"

        # Distribution: High PC, Some LC, Downtrend
        if pc > 85 and lc > 5 and downtrend:
            return "Distribution"

        return "Neutral"

    def _generate_recommendation(self, behavior: str, golden_cross: bool,
                                 death_cross: bool, bottom_catch: bool,
                                 oversold: bool, overbought: bool) -> str:
        """
        Generate trading recommendation

        Returns:
            "BUY", "SELL", or "HOLD"
        """
        # Strong buy signals
        if behavior == "Accumulation" or golden_cross or bottom_catch:
            return "BUY"

        # Buy signals
        if behavior == "Breakout Ready" or oversold:
            return "BUY"

        # Sell signals
        if behavior == "Distribution" or death_cross or overbought:
            return "SELL"

        # Hold for everything else
        return "HOLD"

    def _calculate_support_price(self, df: pd.DataFrame, pc: float, length: int) -> float:
        """
        Calculate MCD support price level

        Args:
            df: Stock data
            pc: Current profit chips percentage
            length: MCDX length

        Returns:
            Support price level
        """
        if len(df) < length:
            return df['close'].iloc[-1]

        # Get price range
        recent_data = df.tail(length)
        lo = recent_data['low'].min()
        hi = recent_data['high'].max()

        # Convert PC percentage to price
        support = lo + (hi - lo) * (pc / 100.0)

        return support

    def _calculate_confidence(self, pc: float, lc: float, sma_pc: float,
                              sma_lc: float, behavior: str) -> float:
        """
        Calculate confidence score for the recommendation

        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence

        # Increase confidence for clear trends
        if abs(sma_pc - sma_lc) > 20:
            confidence += 0.2

        # Increase confidence for extreme values
        if pc < 30 or pc > 80:
            confidence += 0.15

        # Increase confidence for clear behavior patterns
        if behavior in ["Accumulation", "Distribution", "Strong Hold"]:
            confidence += 0.15

        return min(1.0, confidence)
