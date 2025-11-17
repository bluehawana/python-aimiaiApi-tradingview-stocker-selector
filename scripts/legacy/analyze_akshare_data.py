"""
分析 akshare 下载的数据 - 4大严格标准
"""

import yaml
import logging
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AkshareBreakoutFinder:
    """使用 akshare 数据查找突破股票"""

    def __init__(self, data_dir: str = "data/akshare"):
        """初始化"""
        self.data_dir = Path(data_dir)
        self.mcdx_calc = MCDXCalculator()
        self.volume_analyzer = VolumeAnalyzer(
            breakout_threshold=2.0,
            surge_threshold=3.0
        )

        # 筛选标准
        self.min_volume_ratio = 3.0
        self.min_profit_chips = 95.0
        self.min_sma_profit_chips = 80.0
        self.min_price_gain = 5.0
        self.max_price_gain = 20.0

    def load_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """加载股票数据"""
        csv_file = self.data_dir / f"{symbol}.csv"

        if not csv_file.exists():
            return None

        try:
            df = pd.read_csv(csv_file)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            logger.error(f"加载 {symbol} 失败: {e}")
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

        # 遍历数据
        for i in range(30, len(df)):
            row = df.iloc[i]

            # 条件4: 涨幅 >= 5%
            if pd.isna(row['price_change_pct']) or row['price_change_pct'] < self.min_price_gain:
                continue

            if row['price_change_pct'] > self.max_price_gain:
                continue

            # 条件2: 成交量 >= 3x
            if pd.isna(row['volume_ma30']) or row['volume'] < row['volume_ma30'] * self.min_volume_ratio:
                continue

            # 计算 MCDX
            df_up_to_day = df.iloc[:i+1]
            try:
                mcdx_result = self.mcdx_calc.calculate(df_up_to_day, symbol)
            except:
                continue

            # 条件3: MCDX
            if mcdx_result.profit_chips < self.min_profit_chips:
                continue

            if mcdx_result.sma_profit_chips < self.min_sma_profit_chips:
                continue

            # 条件1: 金叉
            is_near_gc, gc_status = self.check_golden_cross(mcdx_result)

            if not is_near_gc:
                continue

            # 所有条件满足
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
                'golden_cross_status': gc_status,
                'behavior': mcdx_result.behavior
            })

        return breakout_days

    def check_golden_cross(self, mcdx_result) -> tuple:
        """检查金叉"""
        current_pc = mcdx_result.sma_profit_chips
        current_lc = mcdx_result.sma_locked_chips

        if current_pc > current_lc:
            return True, "已金叉"

        gap = current_lc - current_pc
        if 0 < gap < 10:
            return True, f"接近金叉(差距{gap:.1f}%)"

        return False, f"未接近金叉"

    def scan_all_stocks(self) -> pd.DataFrame:
        """扫描所有股票"""
        print("="*80)
        print("Akshare 数据分析 - 4大严格标准")
        print("="*80)

        # 获取所有 CSV 文件
        csv_files = list(self.data_dir.glob("*.csv"))

        if len(csv_files) == 0:
            print("\nX No data files found")
            print("Please run: python download_tushare.py")
            return pd.DataFrame()

        print(f"\n找到 {len(csv_files)} 只股票")
        print(f"\n筛选标准:")
        print(f"  1. 近期接近或已发生金叉")
        print(f"  2. 成交量 >= {self.min_volume_ratio}x")
        print(
            f"  3. MCDX: PC >= {self.min_profit_chips}%, SMA PC >= {self.min_sma_profit_chips}%")
        print(f"  4. 当天涨幅 >= {self.min_price_gain}%")
        print("="*80)

        results = []

        for i, csv_file in enumerate(csv_files, 1):
            symbol = csv_file.stem
            print(f"\n[{i}/{len(csv_files)}] {symbol}...", end=' ')

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 30:
                print("✗ 数据不足")
                continue

            breakout_days = self.find_breakout_days(df, symbol)

            if len(breakout_days) > 0:
                print(f"✓ 找到 {len(breakout_days)} 个突破日")

                latest = df.iloc[-1]
                latest_mcdx = self.mcdx_calc.calculate(df, symbol)

                for breakout in breakout_days:
                    results.append({
                        'symbol': symbol,
                        'breakout_date': breakout['date'],
                        'close': breakout['close'],
                        'price_gain': breakout['price_change_pct'],
                        'volume': breakout['volume'],
                        'volume_ratio': breakout['volume_ratio'],
                        'profit_chips': breakout['profit_chips'],
                        'locked_chips': breakout['locked_chips'],
                        'sma_profit_chips': breakout['sma_profit_chips'],
                        'golden_cross_status': breakout['golden_cross_status'],
                        'behavior': breakout['behavior'],
                        'latest_date': latest['date'].strftime('%Y-%m-%d'),
                        'latest_close': latest['close']
                    })
            else:
                print("✗")

        if len(results) == 0:
            print("\n⚠️  没有找到符合条件的股票")
            return pd.DataFrame()

        df = pd.DataFrame(results)
        df = df.sort_values('breakout_date', ascending=False)

        # 显示结果
        self._display_results(df)

        return df

    def _display_results(self, df: pd.DataFrame):
        """显示结果"""
        print("\n" + "="*80)
        print(f"找到 {len(df)} 个突破日")
        print("="*80)

        # 按股票分组
        for symbol in df['symbol'].unique():
            symbol_df = df[df['symbol'] == symbol]

            print(f"\n{'='*80}")
            print(f"🚀 {symbol}")
            print(f"{'='*80}")
            print(f"突破次数: {len(symbol_df)} 次")
            print(f"最新日期: {symbol_df.iloc[0]['latest_date']}")
            print(f"最新价格: ¥{symbol_df.iloc[0]['latest_close']:.2f}")

            print(f"\n突破日详情:")
            for i, row in symbol_df.iterrows():
                print(f"\n  {row['breakout_date']}")
                print(
                    f"    ✅ 价格: ¥{row['close']:.2f} (涨幅 +{row['price_gain']:.2f}%)")
                print(
                    f"    ✅ 成交量: {row['volume']/1e8:.2f}亿 ({row['volume_ratio']:.2f}x)")
                print(
                    f"    ✅ MCDX: PC={row['profit_chips']:.1f}%, SMA PC={row['sma_profit_chips']:.1f}%)")
                print(f"    ✅ 金叉: {row['golden_cross_status']}")

        print("\n" + "="*80)
        print("✓ 分析完成")
        print("="*80)

    def export_results(self, df: pd.DataFrame, filename: str = None):
        """导出结果"""
        if len(df) == 0:
            return

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results/akshare_breakout_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已导出: {filename}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze stock data')
    parser.add_argument('--data-dir', default='data/akshare',
                        help='Data directory')
    parser.add_argument('--min-volume', type=float,
                        default=3.0, help='Min volume ratio')
    parser.add_argument('--min-pc', type=float,
                        default=95.0, help='Min Profit Chips')
    parser.add_argument('--min-sma-pc', type=float,
                        default=80.0, help='Min SMA Profit Chips')
    parser.add_argument('--min-gain', type=float,
                        default=5.0, help='Min price gain %')

    args = parser.parse_args()

    finder = AkshareBreakoutFinder(args.data_dir)
    finder.min_volume_ratio = args.min_volume
    finder.min_profit_chips = args.min_pc
    finder.min_sma_profit_chips = args.min_sma_pc
    finder.min_price_gain = args.min_gain

    results = finder.scan_all_stocks()

    if len(results) > 0:
        finder.export_results(results)


if __name__ == '__main__':
    main()
