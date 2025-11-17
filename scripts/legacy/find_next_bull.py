#!/usr/bin/env python3
"""
Find Next Bull Stock - 寻找下一个金股
专注科技板块 + Shannon模式 (成交量暴增 + MCDX极值)
"""

from datetime import datetime
import yaml
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.china_stock_api import ChinaStockAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def load_tech_stocks():
    """加载科技板块股票列表"""
    with open('config_tech_focus.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    stocks = []
    sectors = config['stocks']['tech_sectors']

    for sector_name, symbols in sectors.items():
        for symbol in symbols:
            stocks.append({
                'symbol': symbol,
                'sector': sector_name
            })

    return stocks, config


def analyze_stock(symbol, sector, api, mcdx_calc, vol_analyzer, config):
    """分析单只股票"""
    try:
        # 获取数据
        df = api.get_stock_data(symbol, days=100)
        if df is None or len(df) < 50:
            return None

        # MCDX分析
        mcdx = mcdx_calc.calculate(df, symbol)

        # 成交量分析
        volume = vol_analyzer.analyze(df, symbol)

        # Shannon模式检测
        shannon_pattern = vol_analyzer.detect_shannon_pattern(df)

        # 计算综合得分
        score = calculate_score(mcdx, volume, shannon_pattern, config)

        # 只返回高分股票 (节约资源)
        threshold = config['scoring']['alert_threshold']
        if score < threshold:
            return None

        return {
            'symbol': symbol,
            'sector': sector,
            'price': df['close'].iloc[-1],
            'mcdx': mcdx,
            'volume': volume,
            'shannon_pattern': shannon_pattern,
            'score': score
        }

    except Exception as e:
        print(f"   ❌ Error analyzing {symbol}: {e}")
        return None


def calculate_score(mcdx, volume, shannon_pattern, config):
    """计算综合得分"""
    score = 0
    scoring = config['scoring']

    # 成交量得分 (40分)
    if volume.volume_surge:  # 3倍成交量
        score += scoring['volume_surge_3x']
    elif volume.volume_breakout:  # 2倍成交量
        score += scoring['volume_breakout_2x']

    if volume.volume_trend == "Increasing":
        score += scoring['volume_increasing_trend']

    # MCDX得分 (40分)
    if mcdx.profit_chips > 85:  # 极值
        score += scoring['profit_chips_extreme']

    if mcdx.golden_cross:
        score += scoring['golden_cross']

    if mcdx.double_dragon:
        score += scoring['double_dragon']

    if mcdx.bottom_catch:
        score += scoring['bottom_catch']

    # 组合信号 (20分)
    if volume.volume_surge and mcdx.profit_chips > 85:
        score += scoring['volume_plus_mcdx']

    # Shannon模式额外加分
    if shannon_pattern:
        score += 20

    return min(100, score)


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🚀 寻找下一个金股 - 科技板块专注版")
    print("=" * 80)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 策略：Shannon模式 (成交量暴增 + MCDX极值)")
    print("   - 成交量：3倍暴增 (如Shannon 9月11-12日: 30M -> 89M)")
    print("   - MCDX：利润筹码>85% (红柱100%，深红线86.65%)")
    print("   - 板块：只关注科技成长股 (CPO、AI芯片、固态电池等)")

    # 加载配置
    print("\n📋 加载科技板块股票...")
    stocks, config = load_tech_stocks()
    print(f"   ✅ 共 {len(stocks)} 只科技股")

    # 统计板块
    sectors = {}
    for stock in stocks:
        sector = stock['sector']
        sectors[sector] = sectors.get(sector, 0) + 1

    print("\n📊 板块分布:")
    for sector, count in sectors.items():
        print(f"   - {sector}: {count}只")

    # 初始化分析器
    api = ChinaStockAPI()
    mcdx_calc = MCDXCalculator(length="Auto", revision="12")
    vol_analyzer = VolumeAnalyzer(breakout_threshold=2.0, surge_threshold=3.0)

    # 分析所有股票
    print("\n" + "=" * 80)
    print("🔍 开始分析...")
    print("=" * 80)

    results = []
    analyzed = 0

    for stock in stocks:
        symbol = stock['symbol']
        sector = stock['sector']

        print(f"\n📊 {symbol} ({sector})...", end=" ")

        result = analyze_stock(symbol, sector, api,
                               mcdx_calc, vol_analyzer, config)

        if result:
            print(f"✅ 得分: {result['score']:.0f}")
            results.append(result)
        else:
            print("⏭️  跳过")

        analyzed += 1

        # 显示进度
        if analyzed % 10 == 0:
            print(f"\n   进度: {analyzed}/{len(stocks)}")

    # 排序结果
    results.sort(key=lambda x: x['score'], reverse=True)

    # 显示结果
    print("\n" + "=" * 80)
    print("🏆 高分股票 (潜在金股)")
    print("=" * 80)

    if not results:
        print("\n⚠️  暂无符合条件的股票")
        print("   建议：降低阈值或等待市场机会")
        return

    print(
        f"\n{'排名':<6} {'代码':<10} {'板块':<20} {'得分':<8} {'成交量':<10} {'利润筹码':<10} {'信号':<20}")
    print("-" * 100)

    for i, r in enumerate(results[:20], 1):  # 只显示前20
        vol_status = "🔥3x" if r['volume'].volume_surge else "⚡2x" if r['volume'].volume_breakout else "📊正常"
        pc_status = f"{r['mcdx'].profit_chips:.1f}%"

        signals = []
        if r['shannon_pattern']:
            signals.append("Shannon")
        if r['mcdx'].golden_cross:
            signals.append("GC")
        if r['mcdx'].double_dragon:
            signals.append("DD")
        if r['volume'].volume_surge:
            signals.append("Vol3x")

        signal_str = ",".join(signals) if signals else "-"

        print(
            f"{i:<6} {r['symbol']:<10} {r['sector']:<20} {r['score']:<8.0f} {vol_status:<10} {pc_status:<10} {signal_str:<20}")

    # 详细分析前5名
    print("\n" + "=" * 80)
    print("📈 Top 5 详细分析")
    print("=" * 80)

    for i, r in enumerate(results[:5], 1):
        print(f"\n🏅 #{i} {r['symbol']} - {r['sector']}")
        print(f"   💰 价格: ¥{r['price']:.2f}")
        print(f"   ⭐ 得分: {r['score']:.0f}/100")
        print(f"\n   📊 成交量分析:")
        print(f"      当前成交量: {r['volume'].current_volume/10000:.0f}万")
        print(f"      30日均量: {r['volume'].avg_volume_30d/10000:.0f}万")
        print(f"      成交量比: {r['volume'].volume_ratio:.2f}x")
        print(f"      趋势: {r['volume'].volume_trend}")
        if r['volume'].volume_surge:
            print(f"      🔥 成交量暴增 (3倍+) - Shannon级别!")
        elif r['volume'].volume_breakout:
            print(f"      ⚡ 成交量突破 (2倍+)")

        print(f"\n   📈 MCDX分析:")
        print(f"      利润筹码: {r['mcdx'].profit_chips:.1f}%")
        print(f"      锁定筹码: {r['mcdx'].locked_chips:.1f}%")
        print(f"      SMA利润: {r['mcdx'].sma_profit_chips:.1f}%")
        print(f"      支撑价: ¥{r['mcdx'].support_price:.2f}")
        print(f"      行为: {r['mcdx'].behavior}")
        print(f"      建议: {r['mcdx'].recommendation}")

        print(f"\n   🚨 信号:")
        if r['shannon_pattern']:
            print(f"      ✅ Shannon模式 - 成交量+MCDX极值!")
        if r['mcdx'].golden_cross:
            print(f"      ✅ 金叉 (Golden Cross)")
        if r['mcdx'].double_dragon:
            print(f"      ✅ 双龙 (Double Dragon)")
        if r['mcdx'].bottom_catch:
            print(f"      ✅ 抄底 (Bottom Catch)")
        if r['volume'].volume_surge:
            print(f"      ✅ 成交量暴增 (3倍+)")

    # 板块统计
    print("\n" + "=" * 80)
    print("📊 板块机会统计")
    print("=" * 80)

    sector_stats = {}
    for r in results:
        sector = r['sector']
        if sector not in sector_stats:
            sector_stats[sector] = []
        sector_stats[sector].append(r)

    print(f"\n{'板块':<25} {'机会数':<10} {'平均得分':<12} {'最高得分':<12}")
    print("-" * 70)

    for sector, stocks in sorted(sector_stats.items(), key=lambda x: len(x[1]), reverse=True):
        avg_score = sum(s['score'] for s in stocks) / len(stocks)
        max_score = max(s['score'] for s in stocks)
        print(f"{sector:<25} {len(stocks):<10} {avg_score:<12.1f} {max_score:<12.1f}")

    # 总结
    print("\n" + "=" * 80)
    print("✅ 分析完成")
    print("=" * 80)
    print(f"\n📊 统计:")
    print(f"   - 分析股票: {analyzed}只")
    print(f"   - 高分股票: {len(results)}只")
    print(
        f"   - Shannon模式: {sum(1 for r in results if r['shannon_pattern'])}只")
    print(
        f"   - 成交量暴增: {sum(1 for r in results if r['volume'].volume_surge)}只")
    print(
        f"   - MCDX极值: {sum(1 for r in results if r['mcdx'].profit_chips > 85)}只")

    print("\n💡 下一步:")
    print("   1. 重点关注Top 5股票")
    print("   2. 监控成交量变化")
    print("   3. 等待金叉确认")
    print("   4. 查看行业新闻催化剂")

    # 保存结果
    print("\n💾 保存结果到 results/watchlist.json")
    import json
    Path("results").mkdir(exist_ok=True)

    watchlist = []
    for r in results[:10]:  # 保存前10
        watchlist.append({
            'symbol': r['symbol'],
            'sector': r['sector'],
            'score': r['score'],
            'price': r['price'],
            'volume_ratio': r['volume'].volume_ratio,
            'profit_chips': r['mcdx'].profit_chips,
            'recommendation': r['mcdx'].recommendation
        })

    with open('results/watchlist.json', 'w', encoding='utf-8') as f:
        json.dump(watchlist, f, ensure_ascii=False, indent=2)

    print("✅ 完成!")


if __name__ == "__main__":
    main()
