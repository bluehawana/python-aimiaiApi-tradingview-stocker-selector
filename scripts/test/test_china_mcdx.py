#!/usr/bin/env python3
"""
Test script for China stock market data and MCDX calculation
Tests data fetching from Shanghai/Shenzhen exchanges and MCDX indicators
"""

from datetime import datetime
import pandas as pd
from src.mcdx.calculator import MCDXCalculator
from src.data.china_stock_api import ChinaStockAPI, POPULAR_CHINA_STOCKS
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def test_data_fetch():
    """Test fetching China stock data"""
    print("=" * 60)
    print("Testing China Stock Data Fetch")
    print("=" * 60)

    api = ChinaStockAPI(source="akshare")

    # Test with a few stocks
    test_stocks = ["600036", "000001", "300750"]  # 招商银行, 平安银行, 宁德时代

    for symbol in test_stocks:
        print(f"\n📊 Fetching data for {symbol}...")
        try:
            df = api.get_stock_data(symbol, days=100)
            print(f"✅ Success! Got {len(df)} days of data")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
            print(f"   Latest close: ¥{df['close'].iloc[-1]:.2f}")
            print(f"   Data preview:")
            print(df.tail(3).to_string(index=False))
        except Exception as e:
            print(f"❌ Error: {e}")

    return True


def test_mcdx_calculation():
    """Test MCDX calculation on China stocks"""
    print("\n" + "=" * 60)
    print("Testing MCDX Calculation")
    print("=" * 60)

    api = ChinaStockAPI(source="akshare")
    calculator = MCDXCalculator(length="Auto", revision="12")

    # Test with popular stocks
    test_stocks = [
        ("600036", "招商银行"),
        ("600519", "贵州茅台"),
        ("000001", "平安银行"),
        ("002594", "比亚迪"),
        ("300750", "宁德时代"),
    ]

    results = []

    for symbol, name in test_stocks:
        print(f"\n📈 Analyzing {symbol} ({name})...")
        try:
            # Fetch data
            df = api.get_stock_data(symbol, days=100)

            # Calculate MCDX
            mcdx = calculator.calculate(df, symbol)

            # Display results
            print(f"✅ MCDX Analysis Complete!")
            print(f"   Current Price: ¥{df['close'].iloc[-1]:.2f}")
            print(f"   Support Price: ¥{mcdx.support_price:.2f}")
            print(f"   Profit Chips:  {mcdx.profit_chips:.1f}%")
            print(f"   Float Chips:   {mcdx.float_chips:.1f}%")
            print(f"   Locked Chips:  {mcdx.locked_chips:.1f}%")
            print(f"   SMA PC:        {mcdx.sma_profit_chips:.1f}%")
            print(f"   SMA LC:        {mcdx.sma_locked_chips:.1f}%")
            print(
                f"   Behavior:      {get_behavior_icon(mcdx.behavior)} {mcdx.behavior}")
            print(f"   Signals:       {get_signals_text(mcdx)}")
            print(
                f"   Recommendation: {get_recommendation_icon(mcdx.recommendation)} {mcdx.recommendation}")
            print(f"   Confidence:    {mcdx.confidence:.1%}")

            results.append({
                'symbol': symbol,
                'name': name,
                'price': df['close'].iloc[-1],
                'mcdx': mcdx
            })

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    # Summary table
    if results:
        print("\n" + "=" * 60)
        print("📊 MCDX Analysis Summary - 2025.11.17")
        print("=" * 60)
        print(f"{'Symbol':<10} {'Name':<12} {'Price':>8} {'Behavior':<18} {'Rec':<6} {'PC%':>6} {'LC%':>6}")
        print("-" * 80)

        for r in results:
            mcdx = r['mcdx']
            print(f"{r['symbol']:<10} {r['name']:<12} ¥{r['price']:>7.2f} "
                  f"{get_behavior_icon(mcdx.behavior)} {mcdx.behavior:<15} "
                  f"{get_recommendation_icon(mcdx.recommendation)} {mcdx.recommendation:<4} "
                  f"{mcdx.profit_chips:>5.1f}% {mcdx.locked_chips:>5.1f}%")

        print("\n💡 Legend:")
        print("   🟢 Accumulation - BUY signal (smart money buying)")
        print("   🔵 Strong Hold - HOLD signal (strong uptrend)")
        print("   🟡 Breakout Ready - BUY signal (ready to breakout)")
        print("   🔴 Distribution - SELL signal (smart money selling)")
        print("   ⚪ Neutral - HOLD signal (no clear trend)")
        print("\n   GC = Golden Cross (bullish)")
        print("   DC = Death Cross (bearish)")
        print("   BC = Bottom Catch (entry opportunity)")
        print("   DD = Double Dragon (strong bullish)")


def get_behavior_icon(behavior: str) -> str:
    """Get emoji icon for behavior"""
    icons = {
        'Accumulation': '🟢',
        'Distribution': '🔴',
        'Strong Hold': '🔵',
        'Breakout Ready': '🟡',
        'Neutral': '⚪'
    }
    return icons.get(behavior, '⚪')


def get_recommendation_icon(rec: str) -> str:
    """Get emoji icon for recommendation"""
    icons = {
        'BUY': '🟢',
        'SELL': '🔴',
        'HOLD': '🟡'
    }
    return icons.get(rec, '⚪')


def get_signals_text(mcdx) -> str:
    """Get signals as text"""
    signals = []
    if mcdx.golden_cross:
        signals.append('GC')
    if mcdx.death_cross:
        signals.append('DC')
    if mcdx.bottom_catch:
        signals.append('BC')
    if mcdx.double_dragon:
        signals.append('DD')
    if mcdx.oversold:
        signals.append('OS')
    if mcdx.overbought:
        signals.append('OB')

    return ', '.join(signals) if signals else 'None'


def main():
    """Main test function"""
    print("\n🇨🇳 China Stock Market MCDX Analyzer Test")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏛️  Markets: Shanghai Stock Exchange (SSE) & Shenzhen Stock Exchange (SZSE)")

    try:
        # Test data fetching
        test_data_fetch()

        # Test MCDX calculation
        test_mcdx_calculation()

        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Configure your aimiai.com credentials in .env")
        print("   3. Run the full analyzer: python main.py --web")
        print("   4. Open browser to: http://localhost:5000")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
