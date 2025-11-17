"""
Breakout Stock Finder - 突破股票筛选器

严格的4大筛选标准:
1. 近2-3个月接近金叉（Golden Cross）
2. 成交量是正常日的3倍以上
3. MCDX 红色柱状图接近100，深红色线在80以上
4. 当天股价上涨至少5-8%

覆盖10大热门板块，50+只股票
"""

import logging
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.aimiai_stock_api import AimiaiStockAPI
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yaml
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BreakoutStockFinder:
    """
    突破股票筛选器

    严格筛选标准:
    1. Golden Cross: 近2-3个月接近或已发生金叉
    2. Volume: 成交量 >= 3x 正常日均量
    3. MCDX: PC 接近100 (>=95), SMA PC >= 80
    4. Price: 当天涨幅 >= 5%
    """

    def __init__(self, config_file: str = 'config_multi_sector.yaml'):
        """初始化筛选器"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.api = AimiaiStockAPI()
        self.mcdx_calc = MCDXCalculator()
        self.volume_analyzer = VolumeAnalyzer(
            breakout_threshold=2.0,
            surge_threshold=3.0
        )

        # 筛选标准
        self.lookback_days = 90  # 2-3个月数据
        self.min_volume_ratio = 3.0  # 3x 成交量
        self.min_profit_chips = 95.0  # PC >= 95
        self.min_sma_profit_chips = 80.0  # SMA PC >= 80
        self.min_price_gain = 5.0  # 涨幅 >= 5%
        self.max_price_gain = 20.0  # 涨幅上限（过滤异常）

    def get_sector_stocks(self) -> Dict[str, List[str]]:
        """获取所有板块的股票列表"""
        return self.config['stocks']['sectors']

    def check_golden_cross_proximity(self, df: pd.DataFrame,
                                     mcdx_result) -> Tuple[bool, str, int]:
        """
        检查是否接近金叉（近2-3个月）

        Returns:
            (is_near_golden_cross, status, days_to_cross)
        """
        if len(df) < 30:
            return False, "数据不足", -1

        # 计算整个时间段的 MCDX
        pc_values = []
        lc_values = []
        dates = []

        # 每10天计算一次，观察趋势
        for i in range(30, len(df), 5):
            df_slice = df.iloc[:i]
            try:
                mcdx_temp = self.mcdx_calc.calculate(df_slice, "temp")
                pc_values.append(mcdx_temp.sma_profit_chips)
                lc_values.append(mcdx_temp.sma_locked_chips)
                dates.append(df_slice['date'].iloc[-1])
            except:
                continue

        if len(pc_values) < 3:
            return False, "数据不足", -1

        # 检查当前状态
        current_pc = mcdx_result.sma_profit_chips
        current_lc = mcdx_result.sma_locked_chips

        # 已经金叉
        if current_pc > current_lc:
            # 检查金叉发生时间（最近何时交叉）
            for i in range(len(pc_values) - 1, 0, -1):
                if pc_values[i] > lc_values[i] and pc_values[i-1] <= lc_values[i-1]:
                    days_ago = (df['date'].iloc[-1] - dates[i]).days
                    if days_ago <= 90:  # 3个月内
                        return True, f"已金叉({days_ago}天前)", 0
            return True, "已金叉(较早)", 0

        # 接近金叉（差距 < 10%）
        gap = current_lc - current_pc
        if 0 < gap < 10:
            # 检查趋势：PC 是否在上升
            if len(pc_values) >= 3:
                recent_trend = pc_values[-1] - pc_values[-3]
                if recent_trend > 0:
                    return True, f"接近金叉(差距{gap:.1f}%)", int(gap * 2)

        # 检查历史是否有接近金叉的情况
        min_gap = float('inf')
        for i in range(len(pc_values)):
            gap = abs(pc_values[i] - lc_values[i])
            if gap < min_gap:
                min_gap = gap

        if min_gap < 5:
            return True, f"曾接近金叉(最小差距{min_gap:.1f}%)", -1

        return False, f"未接近金叉(当前差距{gap:.1f}%)", -1

    def find_breakout_days(self, df: pd.DataFrame,
                           symbol: str) -> List[Dict]:
        """
        查找符合所有4个条件的突破日

        Returns:
            List of breakout days with details
        """
        if len(df) < 30:
            return []

        breakout_days = []

        # 计算30日平均成交量（用于判断3x）
        df['volume_ma30'] = df['volume'].rolling(
            window=30, min_periods=20).mean()

        # 计算每日涨跌幅
        df['price_change_pct'] = df['close'].pct_change() * 100

        # 遍历最近60天，查找突破日
        start_idx = max(30, len(df) - 60)

        for i in range(start_idx, len(df)):
            row = df.iloc[i]

            # 条件4: 当天涨幅 >= 5%
            if pd.isna(row['price_change_pct']) or row['price_change_pct'] < self.min_price_gain:
                continue

            if row['price_change_pct'] > self.max_price_gain:  # 过滤异常涨幅
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

            # 条件3: MCDX PC 接近100 (>=95), SMA PC >= 80
            if mcdx_result.profit_chips < self.min_profit_chips:
                continue

            if mcdx_result.sma_profit_chips < self.min_sma_profit_chips:
                continue

            # 条件1: 检查是否接近金叉（使用当天之前的数据）
            is_near_gc, gc_status, days_to_gc = self.check_golden_cross_proximity(
                df_up_to_day, mcdx_result
            )

            if not is_near_gc:
                continue

            # 所有条件满足！
            volume_ratio = row['volume'] / row['volume_ma30']

            breakout_days.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'close': row['close'],
                'price_change_pct': row['price_change_pct'],
                'volume': row['volume'],
                'volume_ma30': row['volume_ma30'],
                'volume_ratio': volume_ratio,
                'profit_chips': mcdx_result.profit_chips,
                'locked_chips': mcdx_result.locked_chips,
                'sma_profit_chips': mcdx_result.sma_profit_chips,
                'sma_locked_chips': mcdx_result.sma_locked_chips,
                'golden_cross_status': gc_status,
                'golden_cross': mcdx_result.golden_cross,
                'behavior': mcdx_result.behavior
            })

        return breakout_days

    def analyze_stock(self, symbol: str, sector: str) -> Optional[Dict]:
        """
        分析单只股票，查找突破日

        Returns:
            分析结果，如果有突破日则返回详情
        """
        try:
            # 获取2-3个月数据
            df = self.api.get_stock_data(symbol, days=self.lookback_days)
            if df is None or len(df) < 30:
                logger.warning(f"{symbol}: 数据不足")
                return None

            # 查找突破日
            breakout_days = self.find_breakout_days(df, symbol)

            if len(breakout_days) == 0:
                return None

            # 获取最新数据
            latest = df.iloc[-1]
            latest_mcdx = self.mcdx_calc.calculate(df, symbol)

            # 返回结果
            result = {
                'symbol': symbol,
                'sector': sector,
                'latest_date': latest['date'].strftime('%Y-%m-%d'),
                'latest_close': latest['close'],
                'latest_pc': latest_mcdx.profit_chips,
                'latest_lc': latest_mcdx.locked_chips,
                'latest_sma_pc': latest_mcdx.sma_profit_chips,
                'breakout_count': len(breakout_days),
                'breakout_days': breakout_days,
                'most_recent_breakout': breakout_days[-1] if breakout_days else None
            }

            return result

        except Exception as e:
            logger.error(f"{symbol} 分析失败: {e}")
            return None

    def scan_all_sectors(self) -> pd.DataFrame:
        """
        扫描所有板块，查找符合条件的突破股票
        """
        print("=" * 80)
        print("突破股票筛选器 - 4大严格标准")
        print("=" * 80)
        print(f"\n筛选标准:")
        print(f"  1. 近2-3个月接近或已发生金叉")
        print(f"  2. 成交量 >= {self.min_volume_ratio}x 正常日均量")
        print(
            f"  3. MCDX: PC >= {self.min_profit_chips}%, SMA PC >= {self.min_sma_profit_chips}%")
        print(f"  4. 当天涨幅 >= {self.min_price_gain}%")
        print(f"\n分析时间范围: 最近 {self.lookback_days} 天")
        print("=" * 80)

        all_sectors = self.get_sector_stocks()
        results = []

        total_stocks = sum(len(symbols) for symbols in all_sectors.values())
        current = 0

        for sector, symbols in all_sectors.items():
            print(f"\n📊 扫描 {sector} ({len(symbols)} 只股票)...")

            for symbol in symbols:
                current += 1
                print(f"  [{current}/{total_stocks}] {symbol}...", end=' ')

                result = self.analyze_stock(symbol, sector)
                if result:
                    results.append(result)
                    print(f"✓ 找到 {result['breakout_count']} 个突破日")
                else:
                    print("✗")

        # 转换为 DataFrame
        if len(results) == 0:
            print("\n⚠️  没有找到符合条件的股票")
            return pd.DataFrame()

        # 展开突破日数据
        expanded_results = []
        for result in results:
            for breakout in result['breakout_days']:
                expanded_results.append({
                    'symbol': result['symbol'],
                    'sector': result['sector'],
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
        """显示筛选结果"""
        print("\n" + "=" * 80)
        print(f"找到 {len(results)} 只股票，共 {len(df)} 个突破日")
        print("=" * 80)

        # 按股票分组显示
        for result in results:
            print(f"\n{'='*80}")
            print(f"🚀 {result['symbol']} - {result['sector']}")
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
                    f"      ✅ 成交量: {breakout['volume']/1e6:.1f}M ({breakout['volume_ratio']:.2f}x 正常)")
                print(
                    f"      ✅ MCDX: PC={breakout['profit_chips']:.1f}%, SMA PC={breakout['sma_profit_chips']:.1f}%")
                print(f"      ✅ 金叉状态: {breakout['golden_cross_status']}")
                print(f"      ✅ 行为模式: {breakout['behavior']}")

        print("\n" + "=" * 80)
        print(f"✓ 筛选完成")
        print("=" * 80)

    def export_results(self, df: pd.DataFrame, filename: str = None):
        """导出结果到 CSV"""
        if len(df) == 0:
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results/breakout_stocks_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已导出: {filename}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='突破股票筛选器 - 4大严格标准'
    )
    parser.add_argument('--config', '-c', default='config_multi_sector.yaml',
                        help='配置文件')
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
    finder = BreakoutStockFinder(args.config)
    finder.min_volume_ratio = args.min_volume
    finder.min_profit_chips = args.min_pc
    finder.min_sma_profit_chips = args.min_sma_pc
    finder.min_price_gain = args.min_gain

    # 扫描所有板块
    results = finder.scan_all_sectors()

    # 导出结果
    if len(results) > 0:
        if args.export:
            finder.export_results(results, args.export)
        else:
            finder.export_results(results)


if __name__ == '__main__':
    main()
