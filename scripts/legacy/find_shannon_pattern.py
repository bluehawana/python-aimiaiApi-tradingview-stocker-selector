"""
Shannon Pattern Finder
Detects stocks with Shannon-like patterns:
- Volume surge (89M vs 30M normal = 3x)
- MCDX red column at 100
- MCDX dark red line around 86.65
- Sustained high volume (Sept 11-12 pattern)

Covers multiple sectors:
- Chips & Memory
- CPO (Co-Packaged Optics)
- Solid State Batteries
- Lithium Hexafluorophosphate
- Energy Storage
- Solar Energy
- Smart Grids
- Robotics
"""

import logging
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.aimiai_stock_api import AimiaiStockAPI
from typing import List, Dict
import pandas as pd
import yaml
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ShannonPatternFinder:
    """Find stocks with Shannon-like patterns"""

    def __init__(self, config_file: str = 'config_multi_sector.yaml'):
        """Initialize with configuration"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.api = AimiaiStockAPI()
        self.mcdx_calc = MCDXCalculator()
        self.volume_analyzer = VolumeAnalyzer(
            breakout_threshold=2.0,
            surge_threshold=3.0
        )

        # Shannon pattern criteria
        self.criteria = self.config.get('screening', {}).get('criteria', {})
        self.min_profit_chips = self.criteria.get('min_profit_chips', 80)
        self.max_locked_chips = self.criteria.get('max_locked_chips', 15)
        self.min_volume_ratio = self.criteria.get('min_volume_ratio', 2.5)

    def get_all_symbols(self) -> Dict[str, List[str]]:
        """Get all symbols from all sectors"""
        sectors = self.config['stocks']['sectors']
        return sectors

    def analyze_stock(self, symbol: str, sector: str) -> Dict:
        """
        Analyze a single stock for Shannon pattern

        Returns:
            Analysis result with Shannon pattern score
        """
        try:
            # Get stock data
            df = self.api.get_stock_data(symbol, days=100)
            if df is None or len(df) < 30:
                return None

            # Calculate MCDX
            mcdx_result = self.mcdx_calc.calculate(df, symbol)

            # Analyze volume
            volume_result = self.volume_analyzer.analyze(df, symbol)

            # Check Shannon pattern
            shannon_pattern = self.volume_analyzer.detect_shannon_pattern(df)

            # Calculate Shannon score (0-100)
            shannon_score = self._calculate_shannon_score(
                mcdx_result, volume_result, shannon_pattern
            )

            # Get latest price info
            latest = df.iloc[-1]

            result = {
                'symbol': symbol,
                'sector': sector,
                'date': latest['date'].strftime('%Y-%m-%d'),
                'close': latest['close'],

                # MCDX indicators
                'profit_chips': mcdx_result.profit_chips,
                'locked_chips': mcdx_result.locked_chips,
                'sma_profit_chips': mcdx_result.sma_profit_chips,
                'behavior': mcdx_result.behavior,
                'recommendation': mcdx_result.recommendation,

                # Volume indicators
                'current_volume': volume_result.current_volume,
                'avg_volume_30d': volume_result.avg_volume_30d,
                'volume_ratio': volume_result.volume_ratio,
                'volume_surge': volume_result.volume_surge,
                'volume_trend': volume_result.volume_trend,
                'volume_score': volume_result.volume_score,

                # Shannon pattern
                'shannon_pattern': shannon_pattern,
                'shannon_score': shannon_score,

                # Signals
                'golden_cross': mcdx_result.golden_cross,
                'double_dragon': mcdx_result.double_dragon,
                'bottom_catch': mcdx_result.bottom_catch
            }

            return result

        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return None

    def _calculate_shannon_score(self, mcdx_result, volume_result, shannon_pattern) -> float:
        """
        Calculate Shannon pattern score (0-100)
        Higher score = more similar to Shannon pattern
        """
        score = 0.0

        # MCDX score (40 points max)
        # Shannon: PC reached 100, dark red line ~86.65
        if mcdx_result.profit_chips >= 95:
            score += 20
        elif mcdx_result.profit_chips >= 86:
            score += 15
        elif mcdx_result.profit_chips >= 80:
            score += 10

        if mcdx_result.sma_profit_chips >= 85:
            score += 15
        elif mcdx_result.sma_profit_chips >= 80:
            score += 10

        if mcdx_result.locked_chips < 5:
            score += 5

        # Volume score (40 points max)
        # Shannon: 89M vs 30M normal = 3x surge
        if volume_result.volume_ratio >= 3.0:
            score += 25
        elif volume_result.volume_ratio >= 2.5:
            score += 20
        elif volume_result.volume_ratio >= 2.0:
            score += 15

        if volume_result.volume_surge:
            score += 10

        if volume_result.volume_trend == "Increasing":
            score += 5

        # Pattern detection (20 points max)
        if shannon_pattern:
            score += 15

        if mcdx_result.golden_cross or mcdx_result.double_dragon:
            score += 5

        return min(100.0, score)

    def screen_all_stocks(self) -> pd.DataFrame:
        """
        Screen all stocks across all sectors

        Returns:
            DataFrame with analysis results, sorted by Shannon score
        """
        print("=" * 80)
        print("Shannon Pattern Finder - Multi-Sector Screening")
        print("=" * 80)

        all_sectors = self.get_all_symbols()
        results = []

        total_stocks = sum(len(symbols) for symbols in all_sectors.values())
        current = 0

        for sector, symbols in all_sectors.items():
            print(f"\n📊 Scanning {sector} ({len(symbols)} stocks)...")

            for symbol in symbols:
                current += 1
                print(f"  [{current}/{total_stocks}] {symbol}...", end=' ')

                result = self.analyze_stock(symbol, sector)
                if result:
                    results.append(result)
                    print(f"✓ Shannon Score: {result['shannon_score']:.1f}")
                else:
                    print("✗ No data")

        # Convert to DataFrame
        df = pd.DataFrame(results)

        if len(df) == 0:
            print("\n⚠️  No stocks found")
            return df

        # Sort by Shannon score
        df = df.sort_values('shannon_score', ascending=False)

        return df

    def find_top_candidates(self, min_shannon_score: float = 60) -> pd.DataFrame:
        """
        Find top Shannon pattern candidates

        Args:
            min_shannon_score: Minimum Shannon score threshold

        Returns:
            DataFrame with top candidates
        """
        df = self.screen_all_stocks()

        if len(df) == 0:
            return df

        # Filter by Shannon score
        candidates = df[df['shannon_score'] >= min_shannon_score].copy()

        print("\n" + "=" * 80)
        print(f"TOP SHANNON PATTERN CANDIDATES (Score >= {min_shannon_score})")
        print("=" * 80)

        if len(candidates) == 0:
            print(
                f"\n⚠️  No stocks found with Shannon score >= {min_shannon_score}")
            print(f"   Showing top 10 stocks instead:\n")
            candidates = df.head(10)

        # Display results
        for idx, row in candidates.iterrows():
            print(f"\n{'='*80}")
            print(f"🎯 {row['symbol']} - {row['sector']}")
            print(f"{'='*80}")
            print(f"Shannon Score: {row['shannon_score']:.1f}/100")
            print(f"Date: {row['date']}")
            print(f"Price: ¥{row['close']:.2f}")
            print(f"\nMCDX Indicators:")
            print(
                f"  Profit Chips: {row['profit_chips']:.1f}% (SMA: {row['sma_profit_chips']:.1f}%)")
            print(f"  Locked Chips: {row['locked_chips']:.1f}%")
            print(f"  Behavior: {row['behavior']}")
            print(f"  Recommendation: {row['recommendation']}")
            print(f"\nVolume Analysis:")
            print(f"  Current: {row['current_volume']/1e6:.1f}M")
            print(f"  30-Day Avg: {row['avg_volume_30d']/1e6:.1f}M")
            print(f"  Ratio: {row['volume_ratio']:.2f}x")
            print(f"  Surge: {'YES' if row['volume_surge'] else 'NO'}")
            print(f"  Trend: {row['volume_trend']}")
            print(f"\nSignals:")
            signals = []
            if row['shannon_pattern']:
                signals.append("🔥 SHANNON PATTERN")
            if row['golden_cross']:
                signals.append("✨ Golden Cross")
            if row['double_dragon']:
                signals.append("🐉 Double Dragon")
            if row['bottom_catch']:
                signals.append("🎣 Bottom Catch")
            print(f"  {', '.join(signals) if signals else 'None'}")

        print("\n" + "=" * 80)
        print(f"✓ Found {len(candidates)} Shannon pattern candidates")
        print("=" * 80)

        return candidates


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Find Shannon pattern stocks')
    parser.add_argument('--config', '-c', default='config_multi_sector.yaml',
                        help='Configuration file')
    parser.add_argument('--min-score', '-s', type=float, default=60,
                        help='Minimum Shannon score (default: 60)')
    parser.add_argument('--export', '-e', default='results/shannon_candidates.csv',
                        help='Export results to CSV')

    args = parser.parse_args()

    finder = ShannonPatternFinder(args.config)
    candidates = finder.find_top_candidates(args.min_score)

    # Export results
    if len(candidates) > 0 and args.export:
        Path(args.export).parent.mkdir(parents=True, exist_ok=True)
        candidates.to_csv(args.export, index=False, encoding='utf-8-sig')
        print(f"\n💾 Results exported to: {args.export}")


if __name__ == '__main__':
    main()
