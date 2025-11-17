"""
下载24只金叉股票的扩展数据 (120天)
确保有足够数据用于Ichimoku分析
"""

from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import tushare as ts
import sys
from pathlib import Path

load_dotenv()

# 24只金叉股票
GOLDEN_CROSS_STOCKS = {
    '002074': '国轩高科', '002129': '中环股份', '002371': '北方华创',
    '002459': '晶澳科技', '002460': '赣锋锂业', '002466': '天齐锂业',
    '002812': '恩捷股份', '300014': '亿纬锂能', '300274': '阳光电源',
    '300308': '中际旭创', '300316': '晶盛机电', '300450': '先导智能',
    '300502': '新易盛', '300750': '宁德时代', '300763': '锦浪科技',
    '601012': '隆基绿能', '601865': '唯捷创芯', '603986': '兆易创新',
    '688005': '容百科技', '688008': '澜起科技', '688256': '寒武纪',
    '688390': '固德威', '688599': '天合光能', '688981': '中芯国际'
}

# 获取 Tushare token
token = os.getenv('TUSHARE_TOKEN')

if not token:
    print("="*80)
    print("⚠️  需要 Tushare Token")
    print("="*80)
    print("\n请在 .env 文件中配置: TUSHARE_TOKEN=your_token_here")
    sys.exit(1)

# 设置 token
ts.set_token(token)
pro = ts.pro_api()

print("="*80)
print("下载24只金叉股票扩展数据 (120天)")
print("="*80)
print(f"\n股票数量: {len(GOLDEN_CROSS_STOCKS)} 只")

# 计算日期范围 (最近120天)
end_date = datetime.now()
start_date = end_date - timedelta(days=120)

print(
    f"日期范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")
print(f"目标天数: 至少80天 (用于Ichimoku: 52+26=78)")

# 创建输出目录
output_dir = Path("data/tushare")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n开始下载...")
print("="*80)

success_count = 0
failed_symbols = []

for i, (symbol, name) in enumerate(GOLDEN_CROSS_STOCKS.items(), 1):
    print(f"[{i}/{len(GOLDEN_CROSS_STOCKS)}] {name} ({symbol})...",
          end=' ', flush=True)

    # 转换股票代码格式
    if symbol.startswith('6'):
        ts_code = f"{symbol}.SH"
    elif symbol.startswith('0') or symbol.startswith('3'):
        ts_code = f"{symbol}.SZ"
    else:
        print(f"✗ 无效代码")
        failed_symbols.append((symbol, name, "无效代码"))
        continue

    try:
        # 使用 Tushare pro_bar 下载数据
        df = ts.pro_bar(
            ts_code=ts_code,
            adj='qfq',  # 前复权
            start_date=start_date.strftime('%Y%m%d'),
            end_date=end_date.strftime('%Y%m%d')
        )

        if df is not None and len(df) > 0:
            # 标准化列名
            df = df.rename(columns={
                'trade_date': 'date',
                'vol': 'volume',
                'pct_chg': 'change_pct'
            })

            # 转换日期格式
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

            # 成交量单位转换 (手 -> 股)
            df['volume'] = df['volume'] * 100

            # 按日期排序
            df = df.sort_values('date')

            # 保存到 CSV
            output_file = output_dir / f"{symbol}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            # 检查是否有足够数据
            if len(df) >= 78:
                status = "✓"
            else:
                status = "⚠"

            print(f"{status} {len(df)} 天")
            success_count += 1

        else:
            print(f"✗ 无数据")
            failed_symbols.append((symbol, name, "无数据"))

        # 延迟
        time.sleep(0.3)

    except Exception as e:
        error_msg = str(e)[:40]
        print(f"✗ {error_msg}")
        failed_symbols.append((symbol, name, error_msg))
        time.sleep(1)

# 总结
print("\n" + "="*80)
print(f"下载完成: {success_count}/{len(GOLDEN_CROSS_STOCKS)} 成功")
print("="*80)

if failed_symbols:
    print(f"\n失败的股票 ({len(failed_symbols)}):")
    for sym, name, reason in failed_symbols:
        print(f"  - {sym} ({name}): {reason}")

if success_count > 0:
    print(f"\n✓ 数据已保存到: {output_dir.absolute()}")
    print(f"\n下一步:")
    print(f"  python find_shannon_with_ichimoku.py")
else:
    print(f"\n⚠️  没有成功下载任何数据")

print("\n" + "="*80)
