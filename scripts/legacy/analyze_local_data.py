"""
使用本地数据分析股票 - 4大严格标准

不需要任何 API，直接使用本地 ZIP 文件中的数据

严格筛选标准:
1. 近2-3个月接近金叉（Golden Cross）
2. 成交量是正常日的3倍以上
3. MCDX 红色柱状图接近100，深红色线在80以上
4. 当天股价上涨至少5-8%
"""

import logging
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.local_data_loader import LocalDataLoader
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LocalBreakoutFinder:
    """使用本地数据查找突破股票"""

    def __init__(self, data_dir: str = "data/local"):
        """初始化"""
        self.loader = LocalDataLoader(data_dir)
        self.mcdx_calc = MCDXCalculator()
        self.volume_analyzer = VolumeAnalyzer(
            breakout_threshold=2.0,
            surge_threshold=3.0
        )

        # 筛选标准
        self.min_volume_ratio = 3.0  # 3x 成交量
        self.min_profit_chips = 95.0  # PC >= 95
        self.min_sma_profit_chips = 80.0  # SMA PC >= 80
        self.min_price_gain = 5.0  # 涨幅 >= 5%
        self.max_price_gain = 20.0  # 涨幅上限

    def analyze_stock(self, symbol: str, dates: List[str]) -> Optional[Dict]:
        """
        分析单只股票

        Args:
            symbol: 股票代码
            dates: 日期列表

        Returns:
            分析结果
        """
        try:
            # 获取股票数据
            df = self.loader.get_stock_data(symbol, dates)

            if df is None or len(df) < 30:
                return None

            # 查找突破日
            breakout_days = self.find_breakout_days(df, symbol)

            if len(breakout_days) == 0:
                return None

            # 获取最新数据
            latest = df.iloc[-1]
            latest_mcdx = self.mcdx_calc.calculate(df, symbol)

            return {
                'symbol': symbol,
                'latest_date': latest['date'].strftime('%Y-%m-%d'),
                'latest_close': latest['close'],
                'latest_pc': latest_mcdx.profit_chips,
                'latest_lc': latest_mcdx.locked_chips,
                'latest_sma_pc': latest_mcdx.sma_profit_chips,
                'breakout_count': len(breakout_days),
                'breakout_days': breakout_days
            }

        except Exception as e:
            logger.error(f"{symbol} 分析失败: {e}")
            return None

    def find_breakout_days(self, df: pd.DataFrame, symbol: str) -> List[Dict]:
        """查找符合4个条件的突破日"""
        if len(df) < 30:
            return []

        breakout_days = []

        # 计算30日平均成交量
        df['volume_ma30'] = df['volume'].rolling(
            window=30, min_periods=20).mean()

        # 计算每日涨跌幅
        df['price_change_pct'] = df['close'].pct_change() * 100

        # 遍历数据，查找突破日
        for i in range(30, len(df)):
            row = df.iloc[i]

            # 条件4: 当天涨幅 >= 5%
            if pd.isna(row['price_change_pct']) or row['price_change_pct'] < self.min_price_gain:
                continue

            if row['price_change_pct'] > self.max_price_gain:
                continue

            # 条件2: 成交量 >= 3x 正常日均量
            if pd.isna(row['volume_ma30']) or row['volume'] < row['volume_ma30'] * self.min_volume_ratio:
                continue

            # 计算当天的 MCDX
            df_up_to_day = df.iloc[:i+1]
            try:
                mcdx_result = self.mcdx_calc.calculate(df_up_to_day, symbol)
            except:
                continue

            # 条件3: MCDX PC >= 95, SMA PC >= 80
            if mcdx_result.profit_chips < self.min_profit_chips:
                continue

            if mcdx_result.sma_profit_chips < self.min_sma_profit_chips:
                continue

            # 条件1: 检查金叉状态
            is_near_gc, gc_status = self.check_golden_cross(
                df_up_to_day, mcdx_result)

            if not is_near_gc:
                continue

            # 所有条件满足！
            volume_ratio = row['volume'] / row['volume_ma30']

            breakout_days.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'close': row['close'],
                'price_change_pct': row['price_change_pct'],
                'volume': row['volume'],
                'volume_ratio': volume_ratio,
                'profit_chips': mcdx_result.profit_chips,
                'locked_chips': mcdx_result.locked_chips,
                'sma_profit_chips': mcdx_result.sma_profit_chips,
                'sma_locked_chips': mcdx_result.sma_locked_chips,
                'golden_cross_status': gc_status,
                'behavior': mcdx_result.behavior
            })

        return breakout_days

    def check_golden_cross(self, df: pd.DataFrame, mcdx_result) -> tuple:
        """检查是否接近金叉"""
        current_pc = mcdx_result.sma_profit_chips
        current_lc = mcdx_result.sma_locked_chips

        # 已经金叉
        if current_pc > current_lc:
            return True, "已金叉"

        # 接近金叉（差距 < 10%）
        gap = current_lc - current_pc
        if 0 < gap < 10:
            return True, f"接近金叉(差距{gap:.1f}%)"

        return False, f"未接近金叉(差距{gap:.1f}%)"

    def scan_all_stocks(self, symbols: List[str] = None) -> pd.DataFrame:
        """
        扫描所有股票

        Args:
            symbols: 股票代码列表，如果为 None 则扫描所有股票
        """
        print("=" * 80)
        print("本地数据突破股票筛选器 - 4大严格标准")
        print("=" * 80)

        # 获取可用日期
        dates = self.loader.list_available_dates()
        print(f"\n数据日期: {len(dates)} 天")
        print(f"  从 {dates[0]} 到 {dates[-1]}")

        # 获取股票列表
        if symbols is None:
            print(f"\n获取所有股票代码...")
            symbols = self.loader.get_all_symbols()
            print(f"  找到 {len(symbols)} 只股票")

        print(f"\n筛选标准:")
        print(f"  1. 近期接近或已发生金叉")
        print(f"  2. 成交量 >= {self.min_volume_ratio}x 正常日均量")
        print(
            f"  3. MCDX: PC >= {self.min_profit_chips}%, SMA PC >= {self.min_sma_profit_chips}%")
        print(f"  4. 当天涨幅 >= {self.min_price_gain}%")
        print("=" * 80)

        results = []

        for i, symbol in enumerate(symbols, 1):
            print(f"\n[{i}/{len(symbols)}] {symbol}...", end=' ')

            result = self.analyze_stock(symbol, dates)
            if result:
                results.append(result)
                print(f"✓ 找到 {result['breakout_count']} 个突破日")
            else:
                print("✗")

        if len(results) == 0:
            print("\n⚠️  没有找到符合条件的股票")
            return pd.DataFrame()

        # 展开突破日数据
        expanded_results = []
        for result in results:
            for breakout in result['breakout_days']:
                expanded_results.append({
                    'symbol': result['symbol'],
                    'breakout_date': breakout['date'],
                    'close': breakout['close'],
                    'price_gain': breakout['price_change_pct'],
                    'volume': breakout['volume'],
                    'volume_ratio': breakout['volume_ratio'],
                    'profit_chips': breakout['profit_chips'],
                    'locked_chips': breakout['locked_chips'],
                    'sma_profit_chips': breakout['sma_profit_chips'],
                    'sma_locked_chips': breakout['sma_locked_chips'],
                    'golden_cross_status': breakout['golden_cross_status'],
                    'behavior': breakout['behavior'],
                    'latest_date': result['latest_date'],
                    'latest_close': result['latest_close'],
                    'latest_pc': result['latest_pc']
                })

        df = pd.DataFrame(expanded_results)
        df = df.sort_values('breakout_date', ascending=False)

        # 显示结果
        self._display_results(df, results)

        return df

    def _display_results(self, df: pd.DataFrame, results: List[Dict]):
        """显示结果"""
        print("\n" + "=" * 80)
        print(f"找到 {len(results)} 只股票，共 {len(df)} 个突破日")
        print("=" * 80)

        for result in results:
            print(f"\n{'='*80}")
            print(f"🚀 {result['symbol']}")
            print(f"{'='*80}")
            print(f"突破次数: {result['breakout_count']} 次")
            print(f"最新日期: {result['latest_date']}")
            print(f"最新价格: ¥{result['latest_close']:.2f}")
            print(
                f"最新 MCDX: PC={result['latest_pc']:.1f}%, SMA PC={result['latest_sma_pc']:.1f}%")

            print(f"\n突破日详情:")
            for i, breakout in enumerate(result['breakout_days'], 1):
                print(f"\n  [{i}] {breakout['date']}")
                print(
                    f"      ✅ 价格: ¥{breakout['close']:.2f} (涨幅 +{breakout['price_change_pct']:.2f}%)")
                print(
                    f"      ✅ 成交量: {breakout['volume']/1e6:.1f}M ({breakout['volume_ratio']:.2f}x)")
                print(
                    f"      ✅ MCDX: PC={breakout['profit_chips']:.1f}%, SMA PC={breakout['sma_profit_chips']:.1f}%")
                print(f"      ✅ 金叉: {breakout['golden_cross_status']}")

        print("\n" + "=" * 80)
        print(f"✓ 筛选完成")
        print("=" * 80)

    def export_results(self, df: pd.DataFrame, filename: str = None):
        """导出结果"""
        if len(df) == 0:
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results/local_breakout_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已导出: {filename}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='使用本地数据查找突破股票'
    )
    parser.add_argument('--data-dir', default='data/local',
                        help='数据目录 (default: data/local)')
    parser.add_argument('--symbols', nargs='+',
                        help='指定股票代码列表')
    parser.add_argument('--export', '-e',
                        help='导出结果到 CSV 文件')
    parser.add_argument('--min-volume', type=float, default=3.0,
                        help='最小成交量比率 (default: 3.0x)')
    parser.add_argument('--min-pc', type=float, default=95.0,
                        help='最小 Profit Chips (default: 95)')
    parser.add_argument('--min-sma-pc', type=float, default=80.0,
                        help='最小 SMA Profit Chips (default: 80)')
    parser.add_argument('--min-gain', type=float, default=5.0,
                        help='最小涨幅百分比 (default: 5.0%)')

    args = parser.parse_args()

    # 创建筛选器
    finder = LocalBreakoutFinder(args.data_dir)
    finder.min_volume_ratio = args.min_volume
    finder.min_profit_chips = args.min_pc
    finder.min_sma_profit_chips = args.min_sma_pc
    finder.min_price_gain = args.min_gain

    # 扫描股票
    results = finder.scan_all_stocks(args.symbols)

    # 导出结果
    if len(results) > 0:
        if args.export:
            finder.export_results(results, args.export)
        else:
            finder.export_results(results)


if __name__ == '__main__':
    main()
