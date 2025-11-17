"""
Recent 2 Weeks Multi-Sector Analyzer
实时分析最近2周的成交量和MCDX指标

覆盖板块:
- 芯片半导体 (Chips)
- 存储芯片 (Memory)
- CPO 共封装光学
- 固态电池 (Solid State Battery)
- 六氟磷酸锂 (Lithium Hexafluorophosphate)
- 储能 (Energy Storage)
- 光伏 (Solar Energy)
- 智能电网 (Smart Grid)
- 机器人 (Robotics)
- 新能源汽车 (New Energy Vehicles)
"""

import logging
from src.mcdx.volume_analyzer import VolumeAnalyzer
from src.mcdx.calculator import MCDXCalculator
from src.data.aimiai_stock_api import AimiaiStockAPI
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
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


class Recent2WeeksAnalyzer:
    """分析最近2周的股票数据"""

    def __init__(self, config_file: str = 'config_multi_sector.yaml'):
        """初始化分析器"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.api = AimiaiStockAPI()
        self.mcdx_calc = MCDXCalculator()
        self.volume_analyzer = VolumeAnalyzer(
            breakout_threshold=2.0,
            surge_threshold=3.0
        )

        # 分析时间范围：最近2周
        self.analysis_days = 14
        self.lookback_days = 60  # 获取60天数据用于计算30日均量

    def get_sector_stocks(self) -> Dict[str, List[str]]:
        """获取所有板块的股票列表"""
        return self.config['stocks']['sectors']

    def analyze_stock_recent(self, symbol: str, sector: str) -> Dict:
        """
        分析单只股票最近2周的表现

        重点关注:
        1. 最近2周的成交量变化
        2. MCDX 指标变化趋势
        3. 是否出现突破信号
        """
        try:
            # 获取数据（60天用于计算基准）
            df = self.api.get_stock_data(symbol, days=self.lookback_days)
            if df is None or len(df) < 30:
                logger.warning(f"{symbol}: 数据不足")
                return None

            # 分离最近2周数据
            recent_2weeks = df.tail(self.analysis_days).copy()
            if len(recent_2weeks) < 5:
                logger.warning(f"{symbol}: 最近2周数据不足")
                return None

            # 计算 MCDX（使用全部数据）
            mcdx_result = self.mcdx_calc.calculate(df, symbol)

            # 分析成交量（使用全部数据）
            volume_result = self.volume_analyzer.analyze(df, symbol)

            # 分析最近2周的变化
            recent_analysis = self._analyze_recent_changes(
                df, recent_2weeks, mcdx_result, volume_result
            )

            # 获取最新数据
            latest = df.iloc[-1]
            prev_week = df.iloc[-5] if len(df) >= 5 else df.iloc[0]

            result = {
                'symbol': symbol,
                'sector': sector,
                'latest_date': latest['date'].strftime('%Y-%m-%d'),
                'latest_close': latest['close'],
                'latest_volume': latest['volume'],

                # 价格变化
                'price_change_2w': ((latest['close'] - prev_week['close']) / prev_week['close'] * 100),

                # MCDX 当前值
                'profit_chips': mcdx_result.profit_chips,
                'locked_chips': mcdx_result.locked_chips,
                'sma_profit_chips': mcdx_result.sma_profit_chips,
                'sma_locked_chips': mcdx_result.sma_locked_chips,
                'behavior': mcdx_result.behavior,
                'recommendation': mcdx_result.recommendation,

                # 成交量分析
                'avg_volume_30d': volume_result.avg_volume_30d,
                'volume_ratio': volume_result.volume_ratio,
                'volume_surge': volume_result.volume_surge,
                'volume_trend': volume_result.volume_trend,
                'volume_score': volume_result.volume_score,

                # 最近2周变化
                'mcdx_trend_2w': recent_analysis['mcdx_trend'],
                'volume_trend_2w': recent_analysis['volume_trend'],
                'pc_change_2w': recent_analysis['pc_change'],
                'lc_change_2w': recent_analysis['lc_change'],
                'avg_volume_2w': recent_analysis['avg_volume_2w'],
                'max_volume_2w': recent_analysis['max_volume_2w'],
                'volume_spike_days': recent_analysis['volume_spike_days'],

                # 信号
                'golden_cross': mcdx_result.golden_cross,
                'double_dragon': mcdx_result.double_dragon,
                'bottom_catch': mcdx_result.bottom_catch,

                # 综合评分
                'hot_score': self._calculate_hot_score(
                    mcdx_result, volume_result, recent_analysis
                )
            }

            return result

        except Exception as e:
            logger.error(f"{symbol} 分析失败: {e}")
            return None

    def _analyze_recent_changes(self, df_full: pd.DataFrame,
                                df_recent: pd.DataFrame,
                                mcdx_result, volume_result) -> Dict:
        """分析最近2周的变化趋势"""

        # MCDX 变化
        if len(df_full) >= self.analysis_days + 1:
            # 计算2周前的 MCDX
            df_2weeks_ago = df_full.iloc[:-self.analysis_days]
            mcdx_2weeks_ago = self.mcdx_calc.calculate(df_2weeks_ago, "temp")

            pc_change = mcdx_result.profit_chips - mcdx_2weeks_ago.profit_chips
            lc_change = mcdx_result.locked_chips - mcdx_2weeks_ago.locked_chips

            # MCDX 趋势
            if pc_change > 10:
                mcdx_trend = "强势上升"
            elif pc_change > 5:
                mcdx_trend = "上升"
            elif pc_change < -10:
                mcdx_trend = "下降"
            elif pc_change < -5:
                mcdx_trend = "弱势"
            else:
                mcdx_trend = "稳定"
        else:
            pc_change = 0
            lc_change = 0
            mcdx_trend = "数据不足"

        # 成交量分析（最近2周）
        avg_volume_2w = df_recent['volume'].mean()
        max_volume_2w = df_recent['volume'].max()

        # 计算2周前的平均成交量
        if len(df_full) >= self.analysis_days * 2:
            prev_2weeks = df_full.iloc[-self.analysis_days *
                                       2:-self.analysis_days]
            avg_volume_prev = prev_2weeks['volume'].mean()

            volume_change_ratio = avg_volume_2w / \
                avg_volume_prev if avg_volume_prev > 0 else 1

            if volume_change_ratio > 1.5:
                volume_trend = "显著放量"
            elif volume_change_ratio > 1.2:
                volume_trend = "温和放量"
            elif volume_change_ratio < 0.8:
                volume_trend = "缩量"
            else:
                volume_trend = "平稳"
        else:
            volume_trend = "数据不足"

        # 统计最近2周成交量暴增天数（> 2x 30日均量）
        volume_spike_days = sum(
            1 for v in df_recent['volume']
            if v > volume_result.avg_volume_30d * 2.0
        )

        return {
            'mcdx_trend': mcdx_trend,
            'volume_trend': volume_trend,
            'pc_change': pc_change,
            'lc_change': lc_change,
            'avg_volume_2w': avg_volume_2w,
            'max_volume_2w': max_volume_2w,
            'volume_spike_days': volume_spike_days
        }

    def _calculate_hot_score(self, mcdx_result, volume_result,
                             recent_analysis: Dict) -> float:
        """
        计算热度评分 (0-100)
        重点关注最近2周的表现
        """
        score = 0.0

        # MCDX 指标 (30分)
        if mcdx_result.profit_chips >= 90:
            score += 15
        elif mcdx_result.profit_chips >= 80:
            score += 10
        elif mcdx_result.profit_chips >= 70:
            score += 5

        if mcdx_result.locked_chips < 10:
            score += 10
        elif mcdx_result.locked_chips < 20:
            score += 5

        if mcdx_result.sma_profit_chips > mcdx_result.sma_locked_chips:
            score += 5

        # 最近2周 MCDX 趋势 (20分)
        if recent_analysis['mcdx_trend'] == "强势上升":
            score += 20
        elif recent_analysis['mcdx_trend'] == "上升":
            score += 15
        elif recent_analysis['mcdx_trend'] == "稳定":
            score += 5

        # 最近2周成交量 (30分)
        if recent_analysis['volume_trend'] == "显著放量":
            score += 20
        elif recent_analysis['volume_trend'] == "温和放量":
            score += 15
        elif recent_analysis['volume_trend'] == "平稳":
            score += 5

        if recent_analysis['volume_spike_days'] >= 3:
            score += 10
        elif recent_analysis['volume_spike_days'] >= 2:
            score += 5

        # 技术信号 (20分)
        if mcdx_result.golden_cross:
            score += 10
        if mcdx_result.double_dragon:
            score += 5
        if mcdx_result.bottom_catch:
            score += 5

        return min(100.0, score)

    def scan_all_sectors(self, min_hot_score: float = 50) -> pd.DataFrame:
        """
        扫描所有板块，找出最近2周表现突出的股票

        Args:
            min_hot_score: 最低热度评分
        """
        print("=" * 80)
        print("最近2周多板块热点分析")
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"分析周期: 最近 {self.analysis_days} 天")
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

                result = self.analyze_stock_recent(symbol, sector)
                if result:
                    results.append(result)
                    print(f"✓ 热度: {result['hot_score']:.1f}")
                else:
                    print("✗")

        # 转换为 DataFrame
        df = pd.DataFrame(results)

        if len(df) == 0:
            print("\n⚠️  没有找到数据")
            return df

        # 按热度评分排序
        df = df.sort_values('hot_score', ascending=False)

        # 筛选高热度股票
        hot_stocks = df[df['hot_score'] >= min_hot_score].copy()

        # 显示结果
        self._display_results(hot_stocks, min_hot_score)

        return hot_stocks

    def _display_results(self, df: pd.DataFrame, min_score: float):
        """显示分析结果"""
        print("\n" + "=" * 80)
        print(f"最近2周热点股票 (热度 >= {min_score})")
        print("=" * 80)

        if len(df) == 0:
            print(f"\n⚠️  没有找到热度 >= {min_score} 的股票")
            print(f"   建议降低阈值或查看所有结果")
            return

        for idx, row in df.iterrows():
            print(f"\n{'='*80}")
            print(f"🔥 {row['symbol']} - {row['sector']}")
            print(f"{'='*80}")
            print(f"热度评分: {row['hot_score']:.1f}/100")
            print(f"日期: {row['latest_date']}")
            print(
                f"价格: ¥{row['latest_close']:.2f} ({row['price_change_2w']:+.2f}% 近2周)")

            print(f"\n📈 MCDX 指标:")
            print(
                f"  Profit Chips: {row['profit_chips']:.1f}% (SMA: {row['sma_profit_chips']:.1f}%)")
            print(
                f"  Locked Chips: {row['locked_chips']:.1f}% (SMA: {row['sma_locked_chips']:.1f}%)")
            print(f"  行为模式: {row['behavior']}")
            print(f"  建议: {row['recommendation']}")
            print(
                f"  最近2周趋势: {row['mcdx_trend_2w']} (PC变化: {row['pc_change_2w']:+.1f}%)")

            print(f"\n📊 成交量分析:")
            print(f"  最新成交量: {row['latest_volume']/1e6:.1f}M")
            print(f"  30日平均: {row['avg_volume_30d']/1e6:.1f}M")
            print(f"  成交量比率: {row['volume_ratio']:.2f}x")
            print(f"  最近2周趋势: {row['volume_trend_2w']}")
            print(f"  2周平均成交量: {row['avg_volume_2w']/1e6:.1f}M")
            print(f"  2周最大成交量: {row['max_volume_2w']/1e6:.1f}M")
            print(f"  暴量天数(>2x): {row['volume_spike_days']} 天")

            print(f"\n🎯 技术信号:")
            signals = []
            if row['golden_cross']:
                signals.append("✨ Golden Cross")
            if row['double_dragon']:
                signals.append("🐉 Double Dragon")
            if row['bottom_catch']:
                signals.append("🎣 Bottom Catch")
            if row['volume_surge']:
                signals.append("🔥 Volume Surge")
            print(f"  {', '.join(signals) if signals else '无特殊信号'}")

        print("\n" + "=" * 80)
        print(f"✓ 找到 {len(df)} 只热点股票")
        print("=" * 80)

    def export_results(self, df: pd.DataFrame, filename: str = None):
        """导出结果到 CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'results/recent_2weeks_{timestamp}.csv'

        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已导出: {filename}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='分析最近2周多板块热点股票'
    )
    parser.add_argument('--config', '-c', default='config_multi_sector.yaml',
                        help='配置文件')
    parser.add_argument('--min-score', '-s', type=float, default=50,
                        help='最低热度评分 (default: 50)')
    parser.add_argument('--export', '-e',
                        help='导出结果到 CSV 文件')
    parser.add_argument('--days', '-d', type=int, default=14,
                        help='分析天数 (default: 14)')

    args = parser.parse_args()

    # 创建分析器
    analyzer = Recent2WeeksAnalyzer(args.config)
    analyzer.analysis_days = args.days

    # 扫描所有板块
    results = analyzer.scan_all_sectors(args.min_score)

    # 导出结果
    if len(results) > 0:
        if args.export:
            analyzer.export_results(results, args.export)
        else:
            # 自动导出
            analyzer.export_results(results)


if __name__ == '__main__':
    main()
