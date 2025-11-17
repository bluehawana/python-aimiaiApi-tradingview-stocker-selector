#!/usr/bin/env python3
"""
Analyze Shannon (300475) - The 6x Bull Stock
Find the Golden Cross pattern and similar opportunities
"""

from datetime import datetime, timedelta
import pandas as pd
from src.mcdx.calculator import MCDXCalculator
from src.data.china_stock_api import ChinaStockAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def analyze_shannon():
    """Analyze Shannon (300475) in detail"""
    print("\n" + "=" * 80)
    print("📊 Shannon (300475) - The 6x Bull Stock Analysis")
    print("=" * 80)

    api = ChinaStockAPI()
    calc = MCDXCalculator(length="Auto", revision="12")

    # Get 200 days of data to see the full pattern
    print("\n📈 Fetching 200 days of historical data...")
    df = api.get_stock_data('300475', days=200)

    if df is None or len(df) == 0:
        print("❌ Failed to fetch data")
        return

    print(f"✅ Got {len(df)} days of data")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")

    # Current price
    current_price = df['close'].iloc[-1]
    print(f"\n💰 Current Price: ¥{current_price:.2f}")

    # Calculate MCDX
    print("\n🔍 Calculating MCDX indicators...")
    result = calc.calculate(df, '300475')

    print("\n" + "=" * 80)
    print("📊 MCDX Analysis Results")
    print("=" * 80)
    print(f"Profit Chips:     {result.profit_chips:.1f}%")
    print(f"Float Chips:      {result.float_chips:.1f}%")
    print(f"Locked Chips:     {result.locked_chips:.1f}%")
    print(f"SMA Profit Chips: {result.sma_profit_chips:.1f}%")
    print(f"SMA Locked Chips: {result.sma_locked_chips:.1f}%")
    print(f"Support Price:    ¥{result.support_price:.2f}")
    print(f"\n🎯 Behavior:      {result.behavior}")
    print(f"💡 Recommendation: {result.recommendation}")
    print(f"📊 Confidence:    {result.confidence:.1%}")

    # Signals
    print("\n🚨 Signals:")
    signals = []
    if result.golden_cross:
        signals.append("✅ Golden Cross (GC) - BULLISH!")
    if result.death_cross:
        signals.append("❌ Death Cross (DC) - BEARISH")
    if result.bottom_catch:
        signals.append("🎣 Bottom Catch (BC) - Entry Opportunity")
    if result.double_dragon:
        signals.append("🐉 Double Dragon (DD) - STRONG BULLISH!")
    if result.oversold:
        signals.append("📉 Oversold (OS)")
    if result.overbought:
        signals.append("📈 Overbought (OB)")

    if signals:
        for signal in signals:
            print(f"   {signal}")
    else:
        print("   No special signals detected")

    # Historical analysis - find the June 13 Golden Cross
    print("\n" + "=" * 80)
    print("📅 Historical Pattern Analysis")
    print("=" * 80)

    # Calculate MCDX for each day to find Golden Cross dates
    print("\n🔍 Scanning for Golden Cross patterns...")

    golden_crosses = []
    for i in range(20, len(df)):
        df_slice = df.iloc[:i+1].copy()
        temp_result = calc.calculate(df_slice, '300475')
        if temp_result.golden_cross:
            date = df.iloc[i]['date']
            price = df.iloc[i]['close']
            golden_crosses.append({
                'date': date,
                'price': price,
                'pc': temp_result.profit_chips,
                'lc': temp_result.locked_chips
            })

    if golden_crosses:
        print(f"\n✅ Found {len(golden_crosses)} Golden Cross event(s):")
        for gc in golden_crosses:
            print(f"\n   📅 Date: {gc['date'].strftime('%Y-%m-%d')}")
            print(f"   💰 Price: ¥{gc['price']:.2f}")
            print(f"   📊 Profit Chips: {gc['pc']:.1f}%")
            print(f"   🔒 Locked Chips: {gc['lc']:.1f}%")

            # Calculate gain from that date
            if gc['price'] > 0:
                gain = (current_price / gc['price'] - 1) * 100
                print(f"   🚀 Gain from GC: {gain:.1f}%")

    # Price movement analysis
    print("\n" + "=" * 80)
    print("📈 Price Movement Analysis")
    print("=" * 80)

    # Find lowest and highest prices
    min_price = df['close'].min()
    max_price = df['close'].max()
    min_date = df[df['close'] == min_price]['date'].iloc[0]
    max_date = df[df['close'] == max_price]['date'].iloc[0]

    print(
        f"\n📉 Lowest Price:  ¥{min_price:.2f} on {min_date.strftime('%Y-%m-%d')}")
    print(
        f"📈 Highest Price: ¥{max_price:.2f} on {max_date.strftime('%Y-%m-%d')}")
    print(f"🚀 Total Range:   {(max_price/min_price - 1)*100:.1f}% gain")

    # Recent performance
    if len(df) >= 30:
        price_30d_ago = df['close'].iloc[-30]
        gain_30d = (current_price / price_30d_ago - 1) * 100
        print(f"\n📊 30-Day Performance: {gain_30d:+.1f}%")

    if len(df) >= 90:
        price_90d_ago = df['close'].iloc[-90]
        gain_90d = (current_price / price_90d_ago - 1) * 100
        print(f"📊 90-Day Performance: {gain_90d:+.1f}%")

    return result, df


def find_similar_stocks():
    """Find stocks with similar patterns to Shannon"""
    print("\n" + "=" * 80)
    print("🔍 Finding Similar Opportunities (AI/Semiconductor Sector)")
    print("=" * 80)

    # AI and semiconductor related stocks
    ai_stocks = [
        ("300475", "Shannon - 圣邦股份 (Reference)"),
        ("688256", "寒武纪 - Cambricon (AI Chips)"),
        ("688981", "中芯国际 - SMIC (Semiconductor)"),
        ("002371", "北方华创 - NAURA (Semiconductor Equipment)"),
        ("603501", "韦尔股份 - Will Semiconductor"),
        ("688008", "澜起科技 - Montage Technology (Memory Interface)"),
        ("688012", "中微公司 - AMEC (Semiconductor Equipment)"),
        ("300782", "卓胜微 - Maxscend (RF Chips)"),
        ("688396", "华润微 - CR Micro (Power Semiconductor)"),
        ("688099", "晶晨股份 - Amlogic (AI SoC)"),
    ]

    api = ChinaStockAPI()
    calc = MCDXCalculator(length="Auto", revision="12")

    results = []

    for symbol, name in ai_stocks:
        print(f"\n📊 Analyzing {symbol} ({name})...")
        try:
            df = api.get_stock_data(symbol, days=100)
            if df is None or len(df) == 0:
                print(f"   ⚠️  No data available")
                continue

            result = calc.calculate(df, symbol)
            price = df['close'].iloc[-1]

            # Calculate score for similarity to Shannon's pattern
            score = 0

            # Golden Cross is the key signal
            if result.golden_cross:
                score += 50
                print(f"   ✅ GOLDEN CROSS DETECTED!")

            # Low profit chips + high locked chips = accumulation
            if result.profit_chips < 40 and result.locked_chips > 20:
                score += 30
                print(f"   ✅ Accumulation pattern detected")

            # Bottom catch signal
            if result.bottom_catch:
                score += 20
                print(f"   ✅ Bottom Catch signal")

            # Uptrend (SMA PC > SMA LC)
            if result.sma_profit_chips > result.sma_locked_chips:
                score += 10

            print(f"   💰 Price: ¥{price:.2f}")
            print(
                f"   📊 PC: {result.profit_chips:.1f}% | LC: {result.locked_chips:.1f}%")
            print(f"   🎯 Behavior: {result.behavior}")
            print(f"   💡 Recommendation: {result.recommendation}")
            print(f"   ⭐ Similarity Score: {score}/100")

            results.append({
                'symbol': symbol,
                'name': name,
                'price': price,
                'result': result,
                'score': score
            })

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)

    # Summary
    print("\n" + "=" * 80)
    print("🏆 Top Opportunities (Ranked by Similarity to Shannon)")
    print("=" * 80)
    print(f"{'Rank':<6} {'Symbol':<10} {'Name':<30} {'Score':<8} {'Rec':<6} {'PC%':<8} {'LC%':<8}")
    print("-" * 90)

    for i, r in enumerate(results[:10], 1):
        rec_icon = "🟢" if r['result'].recommendation == "BUY" else "🔴" if r['result'].recommendation == "SELL" else "🟡"
        print(f"{i:<6} {r['symbol']:<10} {r['name']:<30} {r['score']:<8} {rec_icon} {r['result'].recommendation:<4} "
              f"{r['result'].profit_chips:>6.1f}% {r['result'].locked_chips:>6.1f}%")

    return results


def main():
    """Main analysis function"""
    print("\n🚀 Shannon Pattern Analysis - Finding the Next 6x Bull Stock")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Analyze Shannon first
    shannon_result, shannon_df = analyze_shannon()

    # Find similar opportunities
    similar_stocks = find_similar_stocks()

    print("\n" + "=" * 80)
    print("✅ Analysis Complete!")
    print("=" * 80)
    print("\n💡 Key Insights:")
    print("   1. Golden Cross (GC) is the strongest bullish signal")
    print("   2. Look for: Low Profit Chips (<40%) + High Locked Chips (>20%)")
    print("   3. AI/Semiconductor sector follows global trends (MU, NVDA)")
    print("   4. RAM demand is universal: servers, DC, laptops, PCs")
    print("\n🎯 Next Steps:")
    print("   1. Monitor top-ranked stocks daily")
    print("   2. Wait for Golden Cross signal")
    print("   3. Check news for AI industry catalysts")
    print("   4. Compare with US semiconductor stocks (MU, NVDA, AMD)")


if __name__ == "__main__":
    main()
