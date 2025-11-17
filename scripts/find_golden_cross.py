"""
寻找金叉股票 - 第一步筛选

只使用 MCDX 金叉标准，找出所有接近或已发生金叉的股票
"""

import logging
from src.mcdx.calculator import MCDXCalculator
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


logging.basicConfig(level=logging.WARNING)  # 减少日志输出


class GoldenCrossFinder:
    """寻找金叉股票"""

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

    def check_golden_cross(self, df, symbol):
        """检查金叉状态"""
        if len(df) < 30:
            return None

        try:
            # 计算 MCDX
            mcdx_result = self.mcdx_calc.calculate(df, symbol)

            pc = mcdx_result.sma_profit_chips
            lc = mcdx_result.sma_locked_chips

            # 判断金叉状态
            if pc > lc:
                status = "已金叉"
                gap = pc - lc
            else:
                gap = lc - pc
                if gap < 10:
                    status = "接近金叉"
                elif gap < 20:
                    status = "较远"
                else:
                    return None  # 太远，不显示

            return {
                'symbol': symbol,
                'date': df['date'].iloc[-1].strftime('%Y-%m-%d'),
                'close': df['close'].iloc[-1],
                'sma_pc': pc,
                'sma_lc': lc,
                'gap': gap,
                'status': status,
                'pc': mcdx_result.profit_chips,
                'lc_raw': mcdx_result.locked_chips,
                'behavior': mcdx_result.behavior,
                'recommendation': mcdx_result.recommendation
            }
        except Exception as e:
            print(f"Error calculating MCDX for {symbol}: {e}")
            return None

    def scan_all(self):
        """扫描所有股票"""
        print("="*80)
        print("金叉股票筛选器")
        print("="*80)

        csv_files = list(self.data_dir.glob("*.csv"))

        if len(csv_files) == 0:
            print("\nNo data files found!")
            print("Please run: python download_tushare.py")
            return pd.DataFrame()

        print(f"\n找到 {len(csv_files)} 只股票")
        print("\n开始分析...")
        print("="*80)

        results = []

        for i, csv_file in enumerate(csv_files, 1):
            symbol = csv_file.stem
            print(f"[{i}/{len(csv_files)}] {symbol}...", end=' ', flush=True)

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 30:
                print("X (insufficient data)")
                continue

            result = self.check_golden_cross(df, symbol)
            if result:
                results.append(result)
                print(f"OK - {result['status']} (Gap: {result['gap']:.1f}%)")
            else:
                print("X (too far)")

        if len(results) == 0:
            print("\n没有找到金叉股票")
            return pd.DataFrame()

        # 转换为 DataFrame 并排序
        df = pd.DataFrame(results)

        # 按状态和gap排序
        df['sort_key'] = df.apply(
            lambda x: 0 if x['status'] == '已金叉' else x['gap'], axis=1)
        df = df.sort_values('sort_key')

        # 显示结果
        self.display_results(df)

        # 导出
        self.export_results(df)

        return df

    def display_results(self, df):
        """显示结果"""
        print("\n" + "="*80)
        print(f"找到 {len(df)} 只金叉股票")
        print("="*80)

        # 已金叉的股票
        golden = df[df['status'] == '已金叉']
        if len(golden) > 0:
            print(f"\n【已金叉】({len(golden)} 只)")
            print("-"*80)
            for _, row in golden.iterrows():
                print(f"\n{row['symbol']}")
                print(f"  日期: {row['date']}")
                print(f"  价格: {row['close']:.2f}")
                print(
                    f"  SMA PC: {row['sma_pc']:.1f}%  SMA LC: {row['sma_lc']:.1f}%")
                print(f"  PC: {row['pc']:.1f}%  LC: {row['lc_raw']:.1f}%")
                print(f"  差距: +{row['gap']:.1f}% (PC > LC)")
                print(f"  行为: {row['behavior']}")
                print(f"  建议: {row['recommendation']}")

        # 接近金叉的股票
        near = df[df['status'] == '接近金叉']
        if len(near) > 0:
            print(f"\n【接近金叉】({len(near)} 只)")
            print("-"*80)
            for _, row in near.iterrows():
                print(f"\n{row['symbol']}")
                print(f"  日期: {row['date']}")
                print(f"  价格: {row['close']:.2f}")
                print(
                    f"  SMA PC: {row['sma_pc']:.1f}%  SMA LC: {row['sma_lc']:.1f}%")
                print(f"  PC: {row['pc']:.1f}%  LC: {row['lc_raw']:.1f}%")
                print(f"  差距: {row['gap']:.1f}% (LC > PC)")
                print(f"  行为: {row['behavior']}")
                print(f"  建议: {row['recommendation']}")

        print("\n" + "="*80)

    def export_results(self, df):
        """导出结果"""
        if len(df) == 0:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'results/golden_cross_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n结果已导出: {filename}")


def main():
    finder = GoldenCrossFinder("data/tushare")
    finder.scan_all()


if __name__ == '__main__':
    main()
