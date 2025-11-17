"""
使用 Tushare 下载中国A股数据 (更稳定)

需要: 
1. 注册 Tushare: https://tushare.pro/register
2. 获取 token: https://tushare.pro/user/token
3. 将 token 添加到 .env 文件: TUSHARE_TOKEN=your_token_here
"""

from dotenv import load_dotenv
import os
import time
import yaml
from datetime import datetime, timedelta
import pandas as pd
import tushare as ts
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


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

# 加载配置
with open('config_multi_sector.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 获取所有股票代码
all_symbols = []
sectors_dict = config['stocks']['sectors']

print("="*80)
print("使用 Tushare 下载中国A股数据 - 最近3个月")
print("="*80)

print(f"\n板块列表:")
for sector, symbols in sectors_dict.items():
    print(f"  {sector}: {len(symbols)} 只股票")
    all_symbols.extend(symbols)

print(f"\n总计: {len(all_symbols)} 只股票")

# 计算日期范围 (最近4个月 = 120天，确保有足够数据用于Ichimoku)
end_date = datetime.now()
start_date = end_date - timedelta(days=120)

print(
    f"\n日期范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")

# 创建输出目录
output_dir = Path("data/tushare")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n开始下载...")
print("="*80)

success_count = 0
failed_symbols = []

for i, symbol in enumerate(all_symbols, 1):
    print(f"[{i}/{len(all_symbols)}] {symbol}...", end=' ', flush=True)

    # 转换股票代码格式 (600036 -> 600036.SH, 000001 -> 000001.SZ)
    if symbol.startswith('6'):
        ts_code = f"{symbol}.SH"
    elif symbol.startswith('0') or symbol.startswith('3'):
        ts_code = f"{symbol}.SZ"
    else:
        print(f"✗ 无效代码")
        failed_symbols.append((symbol, "无效代码"))
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
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'vol': 'volume',  # Tushare 的 vol 是成交量(手)
                'amount': 'amount',  # 成交额(千元)
                'pct_chg': 'change_pct'
            })

            # 转换日期格式
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

            # 成交量单位转换 (手 -> 股，1手=100股)
            df['volume'] = df['volume'] * 100

            # 按日期排序
            df = df.sort_values('date')

            # 保存到 CSV
            output_file = output_dir / f"{symbol}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            print(f"✓ {len(df)} 天")
            success_count += 1

        else:
            print(f"✗ 无数据")
            failed_symbols.append((symbol, "无数据"))

        # 延迟，避免请求过快 (Tushare 有频率限制)
        time.sleep(0.3)

    except Exception as e:
        error_msg = str(e)[:50]
        print(f"✗ {error_msg}")
        failed_symbols.append((symbol, error_msg))
        time.sleep(1)

# 总结
print("\n" + "="*80)
print(f"下载完成: {success_count}/{len(all_symbols)} 成功")
print("="*80)

if failed_symbols:
    print(f"\n失败的股票 ({len(failed_symbols)}):")
    for sym, reason in failed_symbols[:10]:
        print(f"  - {sym}: {reason}")
    if len(failed_symbols) > 10:
        print(f"  ... 还有 {len(failed_symbols) - 10} 个")

if success_count > 0:
    print(f"\n✓ 数据已保存到: {output_dir.absolute()}")
    print(f"\n下一步:")
    print(f"  python analyze_akshare_data.py --data-dir data/tushare")
else:
    print(f"\n⚠️  没有成功下载任何数据")
    print(f"\n可能的原因:")
    print(f"  1. Token 无效或过期")
    print(f"  2. 网络连接问题")
    print(f"  3. Tushare 积分不足")
    print(f"\n建议:")
    print(f"  1. 检查 .env 中的 TUSHARE_TOKEN")
    print(f"  2. 访问 https://tushare.pro/user/token 确认 token")
    print(f"  3. 查看积分: https://tushare.pro/user/vip")

print("\n" + "="*80)
