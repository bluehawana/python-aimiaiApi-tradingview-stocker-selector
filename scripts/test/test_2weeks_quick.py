"""
Quick test for Recent 2 Weeks Analyzer
测试最近2周分析器 - 只测试1只股票
"""
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.aimiai_stock_api import AimiaiStockAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def test_quick():
    """快速测试 - 只分析1只股票"""
    print("=" * 70)
    print("最近2周分析器 - 快速测试")
    print("=" * 70)

    # 测试股票：宁德时代 (300750)
    test_symbol = "300750"

    try:
        # 1. 初始化 API
        print(f"\n[1/4] 初始化 API...")
        api = AimiaiStockAPI()
        print(f"✓ API 初始化成功")

        # 2. 获取数据
        print(f"\n[2/4] 获取 {test_symbol} 数据（最近60天）...")
        df = api.get_stock_data(test_symbol, days=60)

        if df is None or len(df) < 30:
            print(f"✗ 数据不足")
            return False

        print(f"✓ 获取 {len(df)} 天数据")
        print(
            f"  日期范围: {df['date'].iloc[0].strftime('%Y-%m-%d')} 到 {df['date'].iloc[-1].strftime('%Y-%m-%d')}")

        # 3. 计算 MCDX
        print(f"\n[3/4] 计算 MCDX 指标...")
        mcdx_calc = MCDXCalculator()
        mcdx_result = mcdx_calc.calculate(df, test_symbol)

        print(f"✓ MCDX 计算完成")
        print(f"  Profit Chips: {mcdx_result.profit_chips:.1f}%")
        print(f"  Locked Chips: {mcdx_result.locked_chips:.1f}%")
        print(f"  行为模式: {mcdx_result.behavior}")

        # 4. 分析成交量
        print(f"\n[4/4] 分析成交量...")
        volume_analyzer = VolumeAnalyzer()
        volume_result = volume_analyzer.analyze(df, test_symbol)

        print(f"✓ 成交量分析完成")
        print(f"  当前成交量: {volume_result.current_volume/1e6:.1f}M")
        print(f"  30日平均: {volume_result.avg_volume_30d/1e6:.1f}M")
        print(f"  成交量比率: {volume_result.volume_ratio:.2f}x")
        print(f"  成交量趋势: {volume_result.volume_trend}")

        # 5. 分析最近2周
        print(f"\n[5/5] 分析最近2周变化...")
        recent_2weeks = df.tail(14)

        if len(recent_2weeks) >= 5:
            avg_volume_2w = recent_2weeks['volume'].mean()
            max_volume_2w = recent_2weeks['volume'].max()

            # 价格变化
            price_start = recent_2weeks['close'].iloc[0]
            price_end = recent_2weeks['close'].iloc[-1]
            price_change = (price_end - price_start) / price_start * 100

            print(f"✓ 最近2周分析:")
            print(f"  价格变化: {price_change:+.2f}%")
            print(f"  2周平均成交量: {avg_volume_2w/1e6:.1f}M")
            print(f"  2周最大成交量: {max_volume_2w/1e6:.1f}M")

            # 暴量天数
            spike_days = sum(1 for v in recent_2weeks['volume']
                             if v > volume_result.avg_volume_30d * 2.0)
            print(f"  暴量天数(>2x): {spike_days} 天")

        print(f"\n" + "=" * 70)
        print(f"✓ 测试成功！系统运行正常")
        print(f"=" * 70)
        print(f"\n现在可以运行完整分析:")
        print(f"  python analyze_recent_2weeks.py")
        print(f"  或双击: RUN_2WEEKS_ANALYSIS.bat")

        return True

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        print(f"\n故障排除:")
        print(f"  1. 运行: python test_bearer_auth.py")
        print(f"  2. 检查 .env 文件配置")
        print(f"  3. 确认网络连接")
        return False


if __name__ == '__main__':
    success = test_quick()
    sys.exit(0 if success else 1)
