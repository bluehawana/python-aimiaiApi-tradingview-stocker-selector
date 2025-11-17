"""
在24只金叉股票中寻找下一个Shannon
分析标准2-4：成交量暴增、价格突破、综合评分
"""

import logging
from src.mcdx.calculator import MCDXCalculator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(level=logging.WARNING)

# 24只金叉股票的中文名称
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


class ShannonFinder:
    """Shannon模式查找器"""

    def __init__(self, data_dir: str = "data/tushare"):
        self.data_dir = Path(data_dir)
        self.mcdx_calc = MCDXCalculator()

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
            print(f"Error loading {symbol}: {e}")
            return None

    def analyze_criteria_2_volume(self, df, symbol):
        """
        标准2: 成交量暴增分析
        - 成交量比率 >= 2.5x (Shannon是3.0x)
        - 持续2天以上
        - 相对30日均量
        """
        if len(df) < 30:
            return None

        try:
            # 计算30日平均成交量
            df['volume_ma30'] = df['volume'].rolling(
                window=30, min_periods=20).mean()

            # 最近5天数据
            recent = df.tail(5)
            if len(recent) < 2:
                return None

            current_volume = recent['volume'].iloc[-1]
            avg_volume_30d = recent['volume_ma30'].iloc[-1]

            # 成交量比率
            volume_ratio = current_volume / avg_volume_30d if avg_volume_30d > 0 else 0

            # 暴量天数（>= 2.5x）
            surge_days = sum(1 for i in range(len(recent))
                             if recent['volume'].iloc[i] > recent['volume_ma30'].iloc[i] * 2.5)

            # 最近2天平均成交量比率
            if len(recent) >= 2:
                recent_2d_avg = recent['volume'].tail(2).mean()
                recent_2d_ratio = recent_2d_avg / avg_volume_30d if avg_volume_30d > 0 else 0
            else:
                recent_2d_ratio = volume_ratio

            # 成交量评分 (0-40分)
            volume_score = 0

            # 当前成交量比率
            if volume_ratio >= 3.0:
                volume_score += 20
            elif volume_ratio >= 2.5:
                volume_score += 15
            elif volume_ratio >= 2.0:
                volume_score += 10
            elif volume_ratio >= 1.5:
                volume_score += 5

            # 持续天数
            if surge_days >= 2:
                volume_score += 15
            elif surge_days >= 1:
                volume_score += 10

            # 2天平均
            if recent_2d_ratio >= 2.5:
                volume_score += 5

            return {
                'volume_ratio': volume_ratio,
                'surge_days': surge_days,
                'recent_2d_ratio': recent_2d_ratio,
                'volume_score': volume_score,
                'current_volume': current_volume,
                'avg_volume_30d': avg_volume_30d
            }

        except Exception as e:
            print(f"Error in volume analysis for {symbol}: {e}")
            return None

    def analyze_criteria_3_price(self, df, symbol):
        """
        标准3: 价格突破分析
        - 价格趋势向上
        - 突破关键阻力位
        - 涨幅合理
        """
        if len(df) < 30:
            return None

        try:
            recent = df.tail(30)

            # 价格变化
            current_price = recent['close'].iloc[-1]
            price_5d_ago = recent['close'].iloc[-6] if len(
                recent) >= 6 else recent['close'].iloc[0]
            price_10d_ago = recent['close'].iloc[-11] if len(
                recent) >= 11 else recent['close'].iloc[0]

            # 涨幅
            gain_5d = ((current_price - price_5d_ago) /
                       price_5d_ago * 100) if price_5d_ago > 0 else 0
            gain_10d = ((current_price - price_10d_ago) /
                        price_10d_ago * 100) if price_10d_ago > 0 else 0

            # 计算MA5, MA10, MA20
            recent = recent.copy()
            recent['ma5'] = recent['close'].rolling(window=5).mean()
            recent['ma10'] = recent['close'].rolling(window=10).mean()
            recent['ma20'] = recent['close'].rolling(window=20).mean()

            ma5 = recent['ma5'].iloc[-1]
            ma10 = recent['ma10'].iloc[-1]
            ma20 = recent['ma20'].iloc[-1]

            # 价格位置
            above_ma5 = current_price > ma5
            above_ma10 = current_price > ma10
            above_ma20 = current_price > ma20

            # 均线排列（多头排列）
            bullish_alignment = ma5 > ma10 > ma20

            # 价格评分 (0-30分)
            price_score = 0

            # 5日涨幅
            if gain_5d >= 10:
                price_score += 10
            elif gain_5d >= 5:
                price_score += 7
            elif gain_5d >= 3:
                price_score += 5
            elif gain_5d > 0:
                price_score += 2

            # 10日涨幅
            if gain_10d >= 15:
                price_score += 10
            elif gain_10d >= 10:
                price_score += 7
            elif gain_10d >= 5:
                price_score += 5
            elif gain_10d > 0:
                price_score += 2

            # 均线位置
            if above_ma5 and above_ma10 and above_ma20:
                price_score += 5
            elif above_ma5 and above_ma10:
                price_score += 3

            # 多头排列
            if bullish_alignment:
                price_score += 5

            return {
                'current_price': current_price,
                'gain_5d': gain_5d,
                'gain_10d': gain_10d,
                'above_ma5': above_ma5,
                'above_ma10': above_ma10,
                'above_ma20': above_ma20,
                'bullish_alignment': bullish_alignment,
                'price_score': price_score
            }

        except Exception as e:
            print(f"Error in price analysis for {symbol}: {e}")
            return None

    def analyze_criteria_4_mcdx(self, df, symbol):
        """
        标准4: MCDX指标分析
        - Profit Chips >= 80%
        - SMA Profit Chips >= 85%
        - Locked Chips < 15%
        """
        if len(df) < 50:
            return None

        try:
            # 计算MCDX
            result = self.mcdx_calc.calculate(df, symbol)
            if result is None:
                return None

            pc = result.profit_chips
            sma_pc = result.sma_profit_chips
            lc = result.locked_chips

            # MCDX评分 (0-30分)
            mcdx_score = 0

            # Profit Chips
            if pc >= 90:
                mcdx_score += 12
            elif pc >= 85:
                mcdx_score += 10
            elif pc >= 80:
                mcdx_score += 8
            elif pc >= 70:
                mcdx_score += 5

            # SMA Profit Chips
            if sma_pc >= 85:
                mcdx_score += 12
            elif sma_pc >= 80:
                mcdx_score += 10
            elif sma_pc >= 75:
                mcdx_score += 7
            elif sma_pc >= 70:
                mcdx_score += 4

            # Locked Chips
            if lc < 10:
                mcdx_score += 6
            elif lc < 15:
                mcdx_score += 4
            elif lc < 20:
                mcdx_score += 2

            return {
                'pc': pc,
                'sma_pc': sma_pc,
                'lc': lc,
                'mcdx_score': mcdx_score
            }

        except Exception as e:
            print(f"Error in MCDX analysis for {symbol}: {e}")
            return None

    def calculate_shannon_score(self, volume_result, price_result, mcdx_result):
        """
        计算Shannon综合评分 (0-100)
        - 成交量: 40分
        - 价格: 30分
        - MCDX: 30分
        """
        total_score = 0

        if volume_result:
            total_score += volume_result['volume_score']

        if price_result:
            total_score += price_result['price_score']

        if mcdx_result:
            total_score += mcdx_result['mcdx_score']

        return total_score

    def find_next_shannon(self):
        """在24只金叉股票中寻找下一个Shannon"""
        print("=" * 80)
        print("在24只金叉股票中寻找下一个Shannon")
        print("=" * 80)
        print()

        golden_stocks = list(STOCK_NAMES.keys())
        print(f"分析 {len(golden_stocks)} 只金叉股票...")
        print("=" * 80)

        results = []

        for i, symbol in enumerate(golden_stocks, 1):
            name = STOCK_NAMES[symbol]
            print(f"[{i}/{len(golden_stocks)}] {name} ({symbol})...",
                  end=' ', flush=True)

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 50:
                print("X (insufficient data)")
                continue

            # 分析三个标准
            volume_result = self.analyze_criteria_2_volume(df, symbol)
            price_result = self.analyze_criteria_3_price(df, symbol)
            mcdx_result = self.analyze_criteria_4_mcdx(df, symbol)

            if not all([volume_result, price_result, mcdx_result]):
                print("X (analysis failed)")
                continue

            # 计算综合评分
            shannon_score = self.calculate_shannon_score(
                volume_result, price_result, mcdx_result)

            result = {
                'symbol': symbol,
                'name': name,
                'shannon_score': shannon_score,
                'latest_date': df['date'].iloc[-1].strftime('%Y-%m-%d'),
                **volume_result,
                **price_result,
                **mcdx_result
            }

            results.append(result)
            print(f"OK - Score: {shannon_score:.0f}/100")

        if len(results) == 0:
            print("\n没有找到符合条件的股票")
            return pd.DataFrame()

        # 转换为DataFrame并排序
        df = pd.DataFrame(results)
        df = df.sort_values('shannon_score', ascending=False)

        # 显示结果
        self.display_results(df)

        # 导出
        self.export_results(df)

        return df

    def display_results(self, df):
        """显示分析结果"""
        print("\n" + "=" * 80)
        print(f"Shannon分析结果 - 共 {len(df)} 只股票")
        print("=" * 80)

        # 显示TOP 10
        top_10 = df.head(10)

        print(f"\n【TOP 10 - 最接近Shannon模式】")
        print("-" * 80)

        for i, (_, row) in enumerate(top_10.iterrows(), 1):
            # 评级
            if row['shannon_score'] >= 80:
                rating = "🔥🔥🔥"
            elif row['shannon_score'] >= 60:
                rating = "🔥🔥"
            elif row['shannon_score'] >= 40:
                rating = "🔥"
            else:
                rating = "❌"

            print(f"\n{i}. {rating} {row['name']} ({row['symbol']})")
            print(f"   Shannon评分: {row['shannon_score']:.0f}/100")
            print(f"   日期: {row['latest_date']}")
            print(f"   价格: ¥{row['current_price']:.2f}")
            print(f"   ")
            print(f"   【成交量】 评分: {row['volume_score']:.0f}/40")
            print(f"   - 成交量比率: {row['volume_ratio']:.2f}x (目标: >=2.5x)")
            print(f"   - 暴量天数: {row['surge_days']} 天 (目标: >=2天)")
            print(f"   - 2天平均: {row['recent_2d_ratio']:.2f}x")
            print(f"   ")
            print(f"   【价格】 评分: {row['price_score']:.0f}/30")
            print(f"   - 5日涨幅: {row['gain_5d']:+.2f}%")
            print(f"   - 10日涨幅: {row['gain_10d']:+.2f}%")
            print(f"   - 多头排列: {'是' if row['bullish_alignment'] else '否'}")
            print(f"   ")
            print(f"   【MCDX】 评分: {row['mcdx_score']:.0f}/30")
            print(f"   - Profit Chips: {row['pc']:.1f}% (目标: >=80%)")
            print(f"   - SMA PC: {row['sma_pc']:.1f}% (目标: >=85%)")
            print(f"   - Locked Chips: {row['lc']:.1f}% (目标: <15%)")

        # 显示符合Shannon标准的股票
        shannon_candidates = df[df['shannon_score'] >= 60]
        if len(shannon_candidates) > 0:
            print(f"\n【🎯 Shannon候选股票 (评分>=60)】")
            print("-" * 80)
            for _, row in shannon_candidates.iterrows():
                print(
                    f"⭐ {row['name']} ({row['symbol']}) - {row['shannon_score']:.0f}分")

        print("\n" + "=" * 80)
        print("评分说明:")
        print("  80-100分 🔥🔥🔥 - 强烈推荐，极度接近Shannon模式")
        print("  60-79分  🔥🔥   - 值得关注，具有明显特征")
        print("  40-59分  🔥     - 观察，有潜力但需确认")
        print("  0-39分   ❌     - 不符合Shannon模式")
        print("=" * 80)

    def export_results(self, df):
        """导出结果"""
        if len(df) == 0:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'results/shannon_analysis_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n结果已导出: {filename}")


def main():
    finder = ShannonFinder("data/tushare")
    finder.find_next_shannon()


if __name__ == '__main__':
    main()
