"""
Shannon + Ichimoku 综合分析
结合MCDX和Ichimoku Cloud，找到最强的突破信号
"""

import logging
from src.indicators.ichimoku import IchimokuCalculator
from src.mcdx.calculator import MCDXCalculator
from datetime import datetime
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(level=logging.WARNING)

# 股票名称映射
STOCK_NAMES = {
    '002074': '国轩高科', '002129': '中环股份', '002371': '北方华创',
    '002459': '晶澳科技', '002460': '赣锋锂业', '002466': '天齐锂业',
    '002812': '恩捷股份', '300014': '亿纬锂能', '300274': '阳光电源',
    '300308': '中际旭创', '300316': '晶盛机电', '300450': '先导智能',
    '300502': '新易盛', '300750': '宁德时代', '300763': '锦浪科技',
    '601012': '隆基绿能', '601865': '唯捷创芯', '603986': '兆易创新',
    '688005': '容百科技', '688008': '澜起科技', '688256': '寒武纪',
    '688390': '固德威', '688599': '天合光能', '688981': '中芯国际'
}


class ShannonIchimokuFinder:
    """Shannon + Ichimoku 综合分析器"""

    def __init__(self, data_dir: str = "data/tushare"):
        self.data_dir = Path(data_dir)
        self.mcdx_calc = MCDXCalculator()
        self.ichimoku_calc = IchimokuCalculator()

    def load_stock_data(self, symbol: str):
        """加载股票数据"""
        csv_file = self.data_dir / f"{symbol}.csv"
        if not csv_file.exists():
            return None

        try:
            df = pd.read_csv(csv_file)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        except Exception as e:
            return None

    def analyze_stock(self, df, symbol):
        """综合分析股票"""
        if len(df) < 55:
            return None

        try:
            # 1. MCDX分析
            mcdx_result = self.mcdx_calc.calculate(df, symbol)
            if mcdx_result is None:
                return None

            # 2. Ichimoku分析
            ichimoku_result = self.ichimoku_calc.calculate(df)
            if ichimoku_result is None:
                return None

            # 3. 成交量分析
            df['volume_ma30'] = df['volume'].rolling(
                window=30, min_periods=20).mean()
            recent = df.tail(5)

            current_volume = recent['volume'].iloc[-1]
            avg_volume_30d = recent['volume_ma30'].iloc[-1]
            volume_ratio = current_volume / avg_volume_30d if avg_volume_30d > 0 else 0

            # 4. 价格分析
            current_price = df['close'].iloc[-1]
            price_5d_ago = df['close'].iloc[-6] if len(
                df) >= 6 else df['close'].iloc[0]
            gain_5d = ((current_price - price_5d_ago) /
                       price_5d_ago * 100) if price_5d_ago > 0 else 0

            # 5. 综合评分
            # MCDX评分 (40分)
            mcdx_score = 0
            if mcdx_result.profit_chips >= 90:
                mcdx_score += 20
            elif mcdx_result.profit_chips >= 80:
                mcdx_score += 15
            elif mcdx_result.profit_chips >= 70:
                mcdx_score += 10

            if mcdx_result.sma_profit_chips >= 85:
                mcdx_score += 15
            elif mcdx_result.sma_profit_chips >= 80:
                mcdx_score += 10
            elif mcdx_result.sma_profit_chips >= 75:
                mcdx_score += 7

            if mcdx_result.locked_chips < 10:
                mcdx_score += 5
            elif mcdx_result.locked_chips < 15:
                mcdx_score += 3

            # Ichimoku评分 (30分)
            ichimoku_score = ichimoku_result.ichimoku_score * 0.3

            # 成交量评分 (20分)
            volume_score = 0
            if volume_ratio >= 3.0:
                volume_score = 20
            elif volume_ratio >= 2.5:
                volume_score = 15
            elif volume_ratio >= 2.0:
                volume_score = 10
            elif volume_ratio >= 1.5:
                volume_score = 5

            # 价格评分 (10分)
            price_score = 0
            if gain_5d >= 10:
                price_score = 10
            elif gain_5d >= 5:
                price_score = 7
            elif gain_5d >= 3:
                price_score = 5
            elif gain_5d > 0:
                price_score = 2

            # 总分
            total_score = mcdx_score + ichimoku_score + volume_score + price_score

            # 特殊加分
            # 如果Ichimoku强烈看涨 + MCDX金叉 + 成交量放大
            if (ichimoku_result.strong_bullish and
                mcdx_result.profit_chips >= 80 and
                    volume_ratio >= 2.0):
                total_score = min(100, total_score + 15)

            return {
                'symbol': symbol,
                'name': STOCK_NAMES.get(symbol, ''),
                'date': df['date'].iloc[-1].strftime('%Y-%m-%d'),
                'price': current_price,
                'gain_5d': gain_5d,

                # MCDX
                'pc': mcdx_result.profit_chips,
                'sma_pc': mcdx_result.sma_profit_chips,
                'lc': mcdx_result.locked_chips,
                'mcdx_score': mcdx_score,

                # Ichimoku
                'cloud_color': ichimoku_result.cloud_color,
                'price_vs_cloud': ichimoku_result.price_vs_cloud,
                'cloud_breakout': ichimoku_result.cloud_breakout,
                'strong_bullish': ichimoku_result.strong_bullish,
                'ichimoku_score': ichimoku_score,
                'ichimoku_signal': self.ichimoku_calc.get_signal_description(ichimoku_result),

                # Volume
                'volume_ratio': volume_ratio,
                'volume_score': volume_score,

                # Price
                'price_score': price_score,

                # Total
                'total_score': total_score
            }

        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None

    def scan_stocks(self, symbols=None):
        """扫描股票"""
        if symbols is None:
            symbols = list(STOCK_NAMES.keys())

        print("=" * 80)
        print("Shannon + Ichimoku 综合分析")
        print("=" * 80)
        print(f"\n分析 {len(symbols)} 只股票...")
        print("=" * 80)

        results = []

        for i, symbol in enumerate(symbols, 1):
            name = STOCK_NAMES.get(symbol, symbol)
            print(f"[{i}/{len(symbols)}] {name} ({symbol})...",
                  end=' ', flush=True)

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 55:
                print("X (insufficient data)")
                continue

            result = self.analyze_stock(df, symbol)
            if result:
                results.append(result)

                # 显示评分和关键信号
                score_icon = "🔥🔥🔥" if result['total_score'] >= 80 else \
                    "🔥🔥" if result['total_score'] >= 60 else \
                    "🔥" if result['total_score'] >= 40 else "❌"

                signals = []
                if result['strong_bullish']:
                    signals.append("💎Ichimoku强势")
                if result['cloud_breakout']:
                    signals.append("⬆️云层突破")
                if result['volume_ratio'] >= 2.5:
                    signals.append(f"📊量{result['volume_ratio']:.1f}x")

                signal_str = " ".join(signals) if signals else ""

                print(
                    f"OK - {score_icon} {result['total_score']:.0f}分 {signal_str}")
            else:
                print("X (analysis failed)")

        if len(results) == 0:
            print("\n没有找到符合条件的股票")
            return pd.DataFrame()

        # 转换为DataFrame并排序
        df = pd.DataFrame(results)
        df = df.sort_values('total_score', ascending=False)

        # 显示结果
        self.display_results(df)

        # 导出
        self.export_results(df)

        return df

    def display_results(self, df):
        """显示结果"""
        print("\n" + "=" * 80)
        print(f"分析结果 - 共 {len(df)} 只股票")
        print("=" * 80)

        # TOP 10
        top_10 = df.head(10)

        print(f"\n【TOP 10 - 最强信号】")
        print("-" * 80)

        for i, (_, row) in enumerate(top_10.iterrows(), 1):
            # 评级
            if row['total_score'] >= 80:
                rating = "🔥🔥🔥"
            elif row['total_score'] >= 60:
                rating = "🔥🔥"
            elif row['total_score'] >= 40:
                rating = "🔥"
            else:
                rating = "❌"

            print(f"\n{i}. {rating} {row['name']} ({row['symbol']})")
            print(f"   综合评分: {row['total_score']:.0f}/100")
            print(
                f"   日期: {row['date']} | 价格: ¥{row['price']:.2f} | 5日涨幅: {row['gain_5d']:+.2f}%")
            print(f"   ")
            print(f"   【Ichimoku】 {row['ichimoku_score']:.0f}/30")
            print(f"   {row['ichimoku_signal']}")
            print(
                f"   - 云层: {row['cloud_color']} | 价格位置: {row['price_vs_cloud']}")
            if row['cloud_breakout']:
                print(f"   - ⬆️ 云层突破!")
            if row['strong_bullish']:
                print(f"   - 💎 强烈看涨信号!")
            print(f"   ")
            print(f"   【MCDX】 {row['mcdx_score']:.0f}/40")
            print(
                f"   - PC: {row['pc']:.1f}% | SMA PC: {row['sma_pc']:.1f}% | LC: {row['lc']:.1f}%")
            print(f"   ")
            print(f"   【成交量】 {row['volume_score']:.0f}/20")
            print(f"   - 成交量比率: {row['volume_ratio']:.2f}x")
            print(f"   ")
            print(f"   【价格】 {row['price_score']:.0f}/10")

        # 显示超级信号
        super_signals = df[
            (df['strong_bullish'] == True) &
            (df['pc'] >= 80) &
            (df['volume_ratio'] >= 2.0)
        ]

        if len(super_signals) > 0:
            print(f"\n【💎 超级信号 - Ichimoku强势 + MCDX金叉 + 成交量放大】")
            print("-" * 80)
            for _, row in super_signals.iterrows():
                print(
                    f"⭐ {row['name']} ({row['symbol']}) - {row['total_score']:.0f}分")
                print(f"   {row['ichimoku_signal']}")
                print(
                    f"   PC: {row['pc']:.1f}% | 成交量: {row['volume_ratio']:.2f}x")

        print("\n" + "=" * 80)
        print("评分说明:")
        print("  MCDX: 40分 | Ichimoku: 30分 | 成交量: 20分 | 价格: 10分")
        print("  80-100分 🔥🔥🔥 - 超级信号")
        print("  60-79分  🔥🔥   - 强烈推荐")
        print("  40-59分  🔥     - 值得关注")
        print("=" * 80)

    def export_results(self, df):
        """导出结果"""
        if len(df) == 0:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'results/shannon_ichimoku_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✓ 结果已导出: {filename}")


def main():
    finder = ShannonIchimokuFinder("data/tushare")
    finder.scan_stocks()


if __name__ == '__main__':
    main()
