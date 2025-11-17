"""
全市场Shannon扫描 - Shannon + Ichimoku + MCDX
扫描所有A股，找到最强的Shannon候选
"""

import os
from dotenv import load_dotenv
import tushare as ts
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
load_dotenv()

# 科技相关行业关键词
TECH_KEYWORDS = [
    '半导体', '芯片', '集成电路', '电子', '计算机', '软件', '通信',
    '光学', '光电', '新能源', '锂电', '电池', '光伏', '储能',
    '人工智能', 'AI', '机器人', '自动化', '智能', '数据',
    '云计算', '大数据', '物联网', '5G', '通信设备'
]


class AllMarketShannonFinder:
    """全市场Shannon查找器"""

    def __init__(self, data_dir: str = "data/tushare"):
        self.data_dir = Path(data_dir)
        self.mcdx_calc = MCDXCalculator()
        self.ichimoku_calc = IchimokuCalculator()
        self.stock_info = self.load_stock_info()

    def load_stock_info(self):
        """加载股票基本信息"""
        try:
            token = os.getenv('TUSHARE_TOKEN')
            if token:
                ts.set_token(token)
                pro = ts.pro_api()
                stock_list = pro.stock_basic(
                    exchange='',
                    list_status='L',
                    fields='ts_code,symbol,name,area,industry,market'
                )
                return stock_list.set_index('symbol').to_dict('index')
            return {}
        except Exception as e:
            print(f"Warning: 无法加载股票信息: {e}")
            return {}

    def is_tech_stock(self, symbol):
        """判断是否为科技股"""
        if symbol not in self.stock_info:
            return False

        info = self.stock_info[symbol]
        industry = info.get('industry', '')
        name = info.get('name', '')

        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                return True

        return False

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
        if len(df) < 80:
            return None

        try:
            # 1. MCDX分析
            mcdx_result = self.mcdx_calc.calculate(df, symbol)
            if mcdx_result is None:
                return None

            # 检查是否金叉
            sma_pc = mcdx_result.sma_profit_chips
            sma_lc = mcdx_result.sma_locked_chips
            gap = sma_pc - sma_lc

            # 只分析金叉或接近金叉的股票
            if gap < -5:
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
            price_10d_ago = df['close'].iloc[-11] if len(
                df) >= 11 else df['close'].iloc[0]
            gain_5d = ((current_price - price_5d_ago) /
                       price_5d_ago * 100) if price_5d_ago > 0 else 0
            gain_10d = ((current_price - price_10d_ago) /
                        price_10d_ago * 100) if price_10d_ago > 0 else 0

            # 5. 综合评分
            # MCDX评分 (40分)
            mcdx_score = 0
            pc = mcdx_result.profit_chips
            lc = mcdx_result.locked_chips

            if pc >= 90:
                mcdx_score += 20
            elif pc >= 80:
                mcdx_score += 15
            elif pc >= 70:
                mcdx_score += 10

            if sma_pc >= 85:
                mcdx_score += 15
            elif sma_pc >= 80:
                mcdx_score += 10
            elif sma_pc >= 75:
                mcdx_score += 7

            if lc < 10:
                mcdx_score += 5
            elif lc < 15:
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
            if (ichimoku_result.strong_bullish and
                pc >= 80 and
                    volume_ratio >= 2.0):
                total_score = min(100, total_score + 15)

            # 只返回评分>=40的股票
            if total_score < 40:
                return None

            return {
                'symbol': symbol,
                'name': self.stock_info.get(symbol, {}).get('name', ''),
                'industry': self.stock_info.get(symbol, {}).get('industry', ''),
                'market': self.stock_info.get(symbol, {}).get('market', ''),
                'is_tech': self.is_tech_stock(symbol),
                'date': df['date'].iloc[-1].strftime('%Y-%m-%d'),
                'price': current_price,
                'gain_5d': gain_5d,
                'gain_10d': gain_10d,

                # MCDX
                'pc': pc,
                'sma_pc': sma_pc,
                'lc': lc,
                'gap': gap,
                'mcdx_score': mcdx_score,

                # Ichimoku
                'cloud_color': ichimoku_result.cloud_color,
                'price_vs_cloud': ichimoku_result.price_vs_cloud,
                'cloud_breakout': ichimoku_result.cloud_breakout,
                'strong_bullish': ichimoku_result.strong_bullish,
                'ichimoku_score': ichimoku_score,

                # Volume
                'volume_ratio': volume_ratio,
                'volume_score': volume_score,

                # Price
                'price_score': price_score,

                # Total
                'total_score': total_score
            }

        except Exception as e:
            return None

    def scan_all_stocks(self):
        """扫描所有股票"""
        print("=" * 80)
        print("全市场Shannon扫描 - Shannon + Ichimoku + MCDX")
        print("=" * 80)

        # 获取所有CSV文件
        csv_files = list(self.data_dir.glob("*.csv"))
        total = len(csv_files)

        print(f"\n扫描 {total} 只股票...")
        print("筛选条件: 金叉 + 评分>=40")
        print("=" * 80)

        results = []
        processed = 0

        for i, csv_file in enumerate(csv_files, 1):
            symbol = csv_file.stem

            # 显示进度
            if i % 100 == 0:
                print(
                    f"进度: {i}/{total} ({i*100//total}%) | 找到: {len(results)} 只")

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 80:
                continue

            processed += 1
            result = self.analyze_stock(df, symbol)

            if result:
                results.append(result)

                # 实时显示高分股票
                if result['total_score'] >= 60:
                    score_icon = "***" if result['total_score'] >= 80 else "**"
                    tech_icon = "[T]" if result['is_tech'] else "   "
                    ichimoku_icon = "[I]" if result['strong_bullish'] else ""

                    try:
                        print(f"{score_icon} {tech_icon} {result['symbol']} {result['name']:8s} | "
                              f"{result['industry']:12s} | {result['total_score']:.0f}分 {ichimoku_icon}")
                    except UnicodeEncodeError:
                        print(
                            f"{score_icon} {tech_icon} {result['symbol']} | {result['total_score']:.0f}分")

        print(f"\n扫描完成: {processed}/{total} 只有效")
        print("=" * 80)

        if len(results) == 0:
            print("\n没有找到符合条件的股票")
            return pd.DataFrame()

        # 转换为DataFrame
        df = pd.DataFrame(results)

        # 排序: 评分优先，科技股优先
        df = df.sort_values(['total_score', 'is_tech'],
                            ascending=[False, False])

        # 显示结果
        self.display_results(df)

        # 导出
        self.export_results(df)

        return df

    def display_results(self, df):
        """显示结果"""
        tech_count = len(df[df['is_tech'] == True])
        super_signals = len(df[df['total_score'] >= 80])
        strong_signals = len(
            df[(df['total_score'] >= 60) & (df['total_score'] < 80)])

        print(f"\n找到 {len(df)} 只Shannon候选:")
        print(f"  [***] 超级信号 (>=80分): {super_signals} 只")
        print(f"  [**]  强烈推荐 (60-79分): {strong_signals} 只")
        print(f"  [T]   科技股: {tech_count} 只")
        print("=" * 80)

        # 显示超级信号
        super_df = df[df['total_score'] >= 80]
        if len(super_df) > 0:
            print(f"\n【[***] 超级信号 - {len(super_df)} 只】")
            print("-" * 80)
            for i, (_, row) in enumerate(super_df.iterrows(), 1):
                tech_icon = "[T]" if row['is_tech'] else "   "
                ichimoku_icon = "[I]" if row['strong_bullish'] else ""
                print(f"{i:2d}. {tech_icon} {row['symbol']} {row['name']:8s} | "
                      f"{row['industry']:12s} | {row['total_score']:.0f}分 {ichimoku_icon}")
                print(f"    价格: {row['price']:.2f} | 涨幅: {row['gain_5d']:+.1f}% | "
                      f"PC: {row['pc']:.1f}% | 量: {row['volume_ratio']:.2f}x")

        # 显示强烈推荐
        strong_df = df[(df['total_score'] >= 60) & (df['total_score'] < 80)]
        if len(strong_df) > 0:
            print(f"\n【[**] 强烈推荐 - {len(strong_df)} 只】")
            print("-" * 80)
            for i, (_, row) in enumerate(strong_df.head(20).iterrows(), 1):
                tech_icon = "[T]" if row['is_tech'] else "   "
                ichimoku_icon = "[I]" if row['strong_bullish'] else ""
                print(f"{i:2d}. {tech_icon} {row['symbol']} {row['name']:8s} | "
                      f"{row['industry']:12s} | {row['total_score']:.0f}分 {ichimoku_icon}")

            if len(strong_df) > 20:
                print(f"... 还有 {len(strong_df) - 20} 只")

        # 按行业统计
        print(f"\n【行业分布 - TOP 10】")
        print("-" * 80)
        industry_counts = df.groupby('industry').agg({
            'symbol': 'count',
            'total_score': 'mean'
        }).sort_values('symbol', ascending=False).head(10)

        for industry, row in industry_counts.iterrows():
            print(
                f"{industry:15s}: {int(row['symbol']):2d} 只 (平均分: {row['total_score']:.0f})")

        print("\n" + "=" * 80)

    def export_results(self, df):
        """导出结果"""
        if len(df) == 0:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 导出全部
        filename_all = f'results/all_shannon_{timestamp}.csv'
        Path(filename_all).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename_all, index=False, encoding='utf-8-sig')
        print(f"\n✓ 全部结果: {filename_all}")

        # 导出超级信号
        super_df = df[df['total_score'] >= 80]
        if len(super_df) > 0:
            filename_super = f'results/super_shannon_{timestamp}.csv'
            super_df.to_csv(filename_super, index=False, encoding='utf-8-sig')
            print(f"✓ 超级信号: {filename_super}")

        # 导出科技股
        tech_df = df[df['is_tech'] == True]
        if len(tech_df) > 0:
            filename_tech = f'results/tech_shannon_{timestamp}.csv'
            tech_df.to_csv(filename_tech, index=False, encoding='utf-8-sig')
            print(f"✓ 科技股: {filename_tech}")


def main():
    finder = AllMarketShannonFinder("data/tushare")
    finder.scan_all_stocks()


if __name__ == '__main__':
    main()
