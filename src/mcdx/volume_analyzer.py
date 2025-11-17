"""
Volume Analyzer - Detect volume breakouts like Shannon on Sept 11-12
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class VolumeAnalysis:
    """Volume analysis result"""
    symbol: str
    current_volume: float
    avg_volume_30d: float
    volume_ratio: float  # current / average
    volume_breakout: bool  # True if volume > 2x average
    volume_surge: bool  # True if volume > 3x average (like Shannon)
    volume_trend: str  # "Increasing", "Decreasing", "Stable"
    volume_score: float  # 0-100


class VolumeAnalyzer:
    """
    Analyze volume patterns to detect breakouts
    Shannon pattern: Volume surged from 30M to 89M (3x) on Sept 11-12
    """

    def __init__(self, breakout_threshold: float = 2.0, surge_threshold: float = 3.0):
        """
        Initialize Volume Analyzer

        Args:
            breakout_threshold: Volume ratio for breakout (default 2x)
            surge_threshold: Volume ratio for surge (default 3x, like Shannon)
        """
        self.breakout_threshold = breakout_threshold
        self.surge_threshold = surge_threshold

    def analyze(self, df: pd.DataFrame, symbol: str) -> VolumeAnalysis:
        """
        Analyze volume patterns

        Args:
            df: DataFrame with volume data
            symbol: Stock symbol

        Returns:
            VolumeAnalysis object
        """
        if 'volume' not in df.columns or len(df) < 30:
            return self._empty_result(symbol)

        # Current volume (latest day)
        current_volume = df['volume'].iloc[-1]

        # Average volume (30 days, excluding current day)
        avg_volume_30d = df['volume'].iloc[-31:-1].mean()

        # Volume ratio
        volume_ratio = current_volume / avg_volume_30d if avg_volume_30d > 0 else 0

        # Detect breakout and surge
        volume_breakout = volume_ratio >= self.breakout_threshold
        volume_surge = volume_ratio >= self.surge_threshold

        # Volume trend (last 5 days vs previous 5 days)
        recent_avg = df['volume'].iloc[-5:].mean()
        previous_avg = df['volume'].iloc[-10:-5].mean()

        if recent_avg > previous_avg * 1.2:
            volume_trend = "Increasing"
        elif recent_avg < previous_avg * 0.8:
            volume_trend = "Decreasing"
        else:
            volume_trend = "Stable"

        # Calculate volume score (0-100)
        volume_score = self._calculate_volume_score(
            volume_ratio, volume_trend, df['volume']
        )

        return VolumeAnalysis(
            symbol=symbol,
            current_volume=current_volume,
            avg_volume_30d=avg_volume_30d,
            volume_ratio=volume_ratio,
            volume_breakout=volume_breakout,
            volume_surge=volume_surge,
            volume_trend=volume_trend,
            volume_score=volume_score
        )

    def _calculate_volume_score(self, volume_ratio: float,
                                volume_trend: str,
                                volume_series: pd.Series) -> float:
        """
        Calculate volume score (0-100)
        Higher score = stronger volume signal
        """
        score = 0.0

        # Base score from volume ratio
        if volume_ratio >= 3.0:  # Shannon-level surge
            score += 50
        elif volume_ratio >= 2.0:  # Breakout
            score += 30
        elif volume_ratio >= 1.5:  # Above average
            score += 15

        # Trend bonus
        if volume_trend == "Increasing":
            score += 20
        elif volume_trend == "Stable":
            score += 10

        # Consistency bonus (volume increasing over time)
        if len(volume_series) >= 10:
            recent_5 = volume_series.iloc[-5:].mean()
            previous_5 = volume_series.iloc[-10:-5].mean()
            if recent_5 > previous_5:
                score += 15

        # Volatility bonus (sudden spike is more significant)
        if len(volume_series) >= 30:
            vol_std = volume_series.iloc[-30:].std()
            vol_mean = volume_series.iloc[-30:].mean()
            if vol_std > 0 and volume_ratio > 2.0:
                cv = vol_std / vol_mean  # Coefficient of variation
                if cv > 0.5:  # High volatility
                    score += 15

        return min(100.0, score)

    def _empty_result(self, symbol: str) -> VolumeAnalysis:
        """Return empty result when data is insufficient"""
        return VolumeAnalysis(
            symbol=symbol,
            current_volume=0,
            avg_volume_30d=0,
            volume_ratio=0,
            volume_breakout=False,
            volume_surge=False,
            volume_trend="Unknown",
            volume_score=0
        )

    def detect_shannon_pattern(self, df: pd.DataFrame) -> bool:
        """
        Detect Shannon-like volume pattern:
        - Volume surge (3x+ average)
        - Sustained high volume (not just 1 day)
        - Increasing trend

        Args:
            df: DataFrame with volume data

        Returns:
            True if Shannon pattern detected
        """
        if len(df) < 30:
            return False

        # Check recent volume surge
        current_volume = df['volume'].iloc[-1]
        avg_volume = df['volume'].iloc[-31:-1].mean()

        if current_volume < avg_volume * 3.0:
            return False

        # Check if surge is sustained (at least 2 days)
        recent_volumes = df['volume'].iloc[-3:]
        high_volume_days = sum(v > avg_volume * 2.0 for v in recent_volumes)

        if high_volume_days < 2:
            return False

        # Check increasing trend
        recent_avg = df['volume'].iloc[-5:].mean()
        previous_avg = df['volume'].iloc[-10:-5].mean()

        if recent_avg <= previous_avg:
            return False

        return True
