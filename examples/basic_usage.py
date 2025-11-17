"""
Shannon Stock Analyzer - 使用示例
"""

from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mcdx.calculator import MCDXCalculator
from src.indicators.ichimoku import IchimokuCalculator
import pandas as pd

def example_mcdx():
    """MCDX分析示例"""
    print("=" * 80)
    print("MCDX分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # 计算MCDX
    calc = MCDXCalculator()
    result = calc.calculate(df, '688005')
    
    print(f"\n股票: 688005")
    print(f"Profit Chips: {result.profit_chips:.1f}%")
    print(f"SMA PC: {result.sma_profit_chips:.1f}%")
    print(f"Locked Chips: {result.locked_chips:.1f}%")
    print(f"行为: {result.behavior}")
    print(f"建议: {result.recommendation}")

def example_ichimoku():
    """Ichimoku分析示例"""
    print("\n" + "=" * 80)
    print("Ichimoku分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # 计算Ichimoku
    calc = IchimokuCalculator()
    result = calc.calculate(df)
    
    print(f"\n股票: 688005")
    print(f"云层颜色: {result.cloud_color}")
    print(f"价格位置: {result.price_vs_cloud}")
    print(f"强烈看涨: {result.strong_bullish}")
    print(f"Ichimoku评分: {result.ichimoku_score:.0f}/100")
    print(f"信号: {calc.get_signal_description(result)}")

def example_combined():
    """综合分析示例"""
    print("\n" + "=" * 80)
    print("综合分析示例")
    print("=" * 80)
    
    # 加载数据
    df = pd.read_csv('data/tushare/688005.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # MCDX
    mcdx_calc = MCDXCalculator()
    mcdx_result = mcdx_calc.calculate(df, '688005')
    
    # Ichimoku
    ichimoku_calc = IchimokuCalculator()
    ichimoku_result = ichimoku_calc.calculate(df)
    
    # 综合评分
    mcdx_score = 0
    if mcdx_result.profit_chips >= 80:
        mcdx_score += 20
    if mcdx_result.sma_profit_chips >= 85:
        mcdx_score += 15
    if mcdx_result.locked_chips < 15:
        mcdx_score += 5
    
    ichimoku_score = ichimoku_result.ichimoku_score * 0.3
    
    total_score = mcdx_score + ichimoku_score
    
    print(f"\n股票: 688005 (容百科技)")
    print(f"MCDX评分: {mcdx_score}/40")
    print(f"Ichimoku评分: {ichimoku_score:.0f}/30")
    print(f"总分: {total_score:.0f}/70")
    
    if total_score >= 60:
        print("\n评级: 🔥🔥 强烈推荐")
    elif total_score >= 40:
        print("\n评级: 🔥 值得关注")
    else:
        print("\n评级: ❌ 不符合")

if __name__ == '__main__':
    example_mcdx()
    example_ichimoku()
    example_combined()
