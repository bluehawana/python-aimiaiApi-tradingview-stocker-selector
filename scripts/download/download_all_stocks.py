"""
下载所有A股股票数据 (全市场扫描)
覆盖: 科技、银行、券商、大宗商品、基建等所有板块
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

# 获取 Tushare token
token = os.getenv('TUSHARE_TOKEN')

if not token:
    print("="*80)
    print("⚠️  需要 Tushare Token")
    print("="*80)
    print("\n请按以下步骤操作:")
    print("1. 注册 Tushare: https://tushare.pro/register")
    print("2. 获取 token: https://tushare.pro/user/token")
    print("3. 将 token 添加到 .env 文件:")
    print("   TUSHARE_TOKEN=your_token_here")
    print("\n" + "="*80)
    sys.exit(1)

# 设置 token
ts.set_token(token)
pro = ts.pro_api()

print("="*80)
print("下载全市场A股数据 - 寻找所有潜在Shannon")
print("="*80)

# 获取所有A股列表
print("\n正在获取A股列表...")
try:
    # 获取所有上市股票
    stock_list = pro.stock_basic(
        exchange='',
        list_status='L',  # L=上市 D=退市 P=暂停上市
        fields='ts_code,symbol,name,area,industry,market,list_date'
    )

    print(f"✓ 获取到 {len(stock_list)} 只股票")

    # 按市场分类统计
    market_counts = stock_list['market'].value_counts()
    print(f"\n市场分布:")
    for market, count in market_counts.items():
        market_name = {
            '主板': '主板',
            '创业板': '创业板',
            '科创板': '科创板',
            '北交所': '北交所'
        }.get(market, market)
        print(f"  {market_name}: {count} 只")

    # 行业分类统计
    print(f"\n行业分布 (TOP 10):")
    industry_counts = stock_list['industry'].value_counts().head(10)
    for industry, count in industry_counts.items():
        print(f"  {industry}: {count} 只")

except Exception as e:
    print(f"✗ 获取股票列表失败: {e}")
    sys.exit(1)

# 计算日期范围 (最近6个月 = 180天，确保有足够数据用于Ichimoku和更好的分析)
end_date = datetime.now()
start_date = end_date - timedelta(days=180)

print(
    f"\n日期范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")

# 创建输出目录
output_dir = Path("data/tushare")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n开始下载...")
print("="*80)

success_count = 0
failed_symbols = []
skipped_count = 0

for i, row in stock_list.iterrows():
    ts_code = row['ts_code']
    symbol = row['symbol']
    name = row['name']

    # 检查是否已存在且数据较新
    output_file = output_dir / f"{symbol}.csv"
    if output_file.exists():
        try:
            existing_df = pd.read_csv(output_file)
            if len(existing_df) > 0:
                existing_df['date'] = pd.to_datetime(existing_df['date'])
                latest_date = existing_df['date'].max()
                days_old = (datetime.now() - latest_date).days

                # 如果数据不超过2天，跳过
                if days_old <= 2:
                    print(f"[{i+1}/{len(stock_list)}] {symbol} ({name})... ⊙ 已存在")
                    skipped_count += 1
                    continue
        except:
            pass

    print(f"[{i+1}/{len(stock_list)}] {symbol} ({name})...", end=' ', flush=True)

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
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            print(f"✓ {len(df)} 天")
            success_count += 1

        else:
            print(f"✗ 无数据")
            failed_symbols.append((symbol, name, "无数据"))

        # 延迟，避免请求过快
        time.sleep(0.25)

    except Exception as e:
        error_msg = str(e)[:40]
        print(f"✗ {error_msg}")
        failed_symbols.append((symbol, name, error_msg))
        time.sleep(1)

# 总结
print("\n" + "="*80)
print(f"下载完成:")
print(f"  成功: {success_count}")
print(f"  跳过: {skipped_count} (数据已是最新)")
print(f"  失败: {len(failed_symbols)}")
print(f"  总计: {len(stock_list)}")
print("="*80)

if failed_symbols:
    print(f"\n失败的股票 ({len(failed_symbols)}):")
    for sym, name, reason in failed_symbols[:10]:
        print(f"  - {sym} ({name}): {reason}")
    if len(failed_symbols) > 10:
        print(f"  ... 还有 {len(failed_symbols) - 10} 个")

if success_count > 0 or skipped_count > 0:
    total_files = success_count + skipped_count
    print(f"\n✓ 共有 {total_files} 只股票数据可用")
    print(f"✓ 数据已保存到: {output_dir.absolute()}")
    print(f"\n下一步 - 全市场金叉扫描:")
    print(f"  python find_golden_cross_all.py")
else:
    print(f"\n⚠️  没有可用数据")

print("\n" + "="*80)
