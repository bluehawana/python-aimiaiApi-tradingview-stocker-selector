"""
使用文件夹数据分析股票 - 4大严格标准

从 D:\projects\TW\src\data\20251117 读取数据

严格筛选标准:
1. 近2-3个月接近金叉（Golden Cross）
2. 成交量是正常日的3倍以上
3. MCDX 红色柱状图接近100，深红色线在80以上
4. 当天股价上涨至少5-8%
"""

from analyze_local_data import LocalBreakoutFinder
from src.data.folder_data_loader import FolderDataLoader
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# 使用文件夹加载器

# 继承并修改加载器


class FolderBreakoutFinder(LocalBreakoutFinder):
    """使用文件夹数据查找突破股票"""

    def __init__(self, data_dir: str = r"D:\projects\TW\src\data"):
        """初始化 - 使用文件夹加载器"""
        self.loader = FolderDataLoader(data_dir)

        from src.mcdx.calculator import MCDXCalculator
        from src.mcdx.volume_analyzer import VolumeAnalyzer

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


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='使用文件夹数据查找突破股票'
    )
    parser.add_argument('--data-dir',
                        default=r'D:\projects\TW\src\data',
                        help='数据目录')
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

    print("=" * 80)
    print("文件夹数据突破股票筛选器")
    print("=" * 80)
    print(f"\n数据目录: {args.data_dir}")

    # 创建筛选器
    finder = FolderBreakoutFinder(args.data_dir)
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
