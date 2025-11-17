"""
全市场金叉扫描 - 所有A股
覆盖科技、银行、券商、大宗商品、基建等所有板块
优先级: 科技 > 其他
"""

import os
from dotenv import load_dotenv
import tushare as ts
import logging
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


class GoldenCrossFinder:
    """全市场金叉查找器"""

    def __init__(self, data_dir: str = "data/tushare"):
        self.data_dir = Path(data_dir)
        self.mcdx_calc = MCDXCalculator()
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
                # 转换为字典，方便查询
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

        # 检查行业或名称是否包含科技关键词
        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                return True

        return False

    def get_stock_info_str(self, symbol):
        """获取股票信息字符串"""
        if symbol not in self.stock_info:
            return ""

        info = self.stock_info[symbol]
        name = info.get('name', '')
        industry = info.get('industry', '')
        market = info.get('market', '')

        return f"{name} | {industry} | {market}"

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

    def check_golden_cross(self, df, symbol):
        """检查是否金叉"""
        if len(df) < 50:
            return None

        try:
            # 计算MCDX
            result = self.mcdx_calc.calculate(df, symbol)
            if result is None:
                return None

            pc = result.profit_chips
            lc = result.locked_chips
            sma_pc = result.sma_profit_chips
            sma_lc = result.sma_locked_chips

            # 计算gap
            gap = sma_pc - sma_lc

            # 判断金叉状态
            if gap > 0:
                status = "已金叉"
                sort_key = 0.0
            elif gap > -5:
                status = "接近金叉"
                sort_key = abs(gap)
            else:
                return None

            # 获取最新数据
            latest = df.iloc[-1]

            return {
                'symbol': symbol,
                'name': self.stock_info.get(symbol, {}).get('name', ''),
                'industry': self.stock_info.get(symbol, {}).get('industry', ''),
                'market': self.stock_info.get(symbol, {}).get('market', ''),
                'is_tech': self.is_tech_stock(symbol),
                'date': latest['date'].strftime('%Y-%m-%d'),
                'close': latest['close'],
                'sma_pc': sma_pc,
                'sma_lc': sma_lc,
                'gap': gap,
                'status': status,
                'pc': pc,
                'lc': lc,
                'behavior': result.behavior,
                'recommendation': result.recommendation,
                'sort_key': sort_key
            }

        except Exception as e:
            return None

    def scan_all_stocks(self):
        """扫描所有股票"""
        print("=" * 80)
        print("全市场金叉扫描 - 所有A股")
        print("=" * 80)

        # 获取所有CSV文件
        csv_files = list(self.data_dir.glob("*.csv"))
        total = len(csv_files)

        print(f"\n扫描 {total} 只股票...")
        print("=" * 80)

        results = []
        tech_count = 0
        non_tech_count = 0

        for i, csv_file in enumerate(csv_files, 1):
            symbol = csv_file.stem

            # 显示进度
            if i % 100 == 0:
                print(f"进度: {i}/{total} ({i*100//total}%)")

            df = self.load_stock_data(symbol)
            if df is None or len(df) < 50:
                continue

            result = self.check_golden_cross(df, symbol)
            if result:
                results.append(result)
                if result['is_tech']:
                    tech_count += 1
                else:
                    non_tech_count += 1

                # 实时显示找到的金叉
                status_icon = "✨" if result['status'] == "已金叉" else "🔸"
                tech_icon = "🔥" if result['is_tech'] else "  "
                print(f"{status_icon} {tech_icon} {result['symbol']} {result['name']} | "
                      f"{result['industry']} | Gap: {result['gap']:.1f}%")

        print(f"\n扫描完成: {total} 只")
        print("=" * 80)

        if len(results) == 0:
            print("\n没有找到金叉股票")
            return pd.DataFrame()

        # 转换为DataFrame
        df = pd.DataFrame(results)

        # 排序: 科技股优先，然后按gap排序
        df = df.sort_values(['is_tech', 'sort_key'], ascending=[False, True])

        # 显示结果
        self.display_results(df, tech_count, non_tech_count)

        # 导出
        self.export_results(df)

        return df

    def display_results(self, df, tech_count, non_tech_count):
        """显示结果"""
        print(f"\n找到 {len(df)} 只金叉股票:")
        print(f"  🔥 科技股: {tech_count} 只")
        print(f"     其他: {non_tech_count} 只")
        print("=" * 80)

        # 显示科技股
        tech_stocks = df[df['is_tech'] == True]
        if len(tech_stocks) > 0:
            print(f"\n【🔥 科技股金叉 - {len(tech_stocks)} 只】")
            print("-" * 80)
            for i, (_, row) in enumerate(tech_stocks.head(30).iterrows(), 1):
                status_icon = "✨" if row['status'] == "已金叉" else "🔸"
                print(f"{i:2d}. {status_icon} {row['symbol']} {row['name']:8s} | "
                      f"{row['industry']:12s} | Gap: {row['gap']:>6.1f}% | "
                      f"PC: {row['pc']:>5.1f}% | {row['recommendation']}")

            if len(tech_stocks) > 30:
                print(f"... 还有 {len(tech_stocks) - 30} 只科技股")

        # 显示其他行业
        non_tech_stocks = df[df['is_tech'] == False]
        if len(non_tech_stocks) > 0:
            print(f"\n【其他行业金叉 - {len(non_tech_stocks)} 只】")
            print("-" * 80)

            # 按行业分组显示
            industry_groups = non_tech_stocks.groupby('industry')
            for industry, group in list(industry_groups)[:10]:
                print(f"\n{industry} ({len(group)} 只):")
                for _, row in group.head(5).iterrows():
                    status_icon = "✨" if row['status'] == "已金叉" else "🔸"
                    print(f"  {status_icon} {row['symbol']} {row['name']:8s} | "
                          f"Gap: {row['gap']:>6.1f}% | PC: {row['pc']:>5.1f}%")

        print("\n" + "=" * 80)
        print("🎯 优先关注科技股金叉")
        print("💡 其他行业也可能有机会")
        print("=" * 80)

    def export_results(self, df):
        """导出结果"""
        if len(df) == 0:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 导出全部
        filename_all = f'results/golden_cross_all_{timestamp}.csv'
        Path(filename_all).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filename_all, index=False, encoding='utf-8-sig')
        print(f"\n✓ 全部结果: {filename_all}")

        # 导出科技股
        tech_stocks = df[df['is_tech'] == True]
        if len(tech_stocks) > 0:
            filename_tech = f'results/golden_cross_tech_{timestamp}.csv'
            tech_stocks.to_csv(filename_tech, index=False,
                               encoding='utf-8-sig')
            print(f"✓ 科技股: {filename_tech}")


def main():
    finder = GoldenCrossFinder("data/tushare")
    finder.scan_all_stocks()


if __name__ == '__main__':
    main()
