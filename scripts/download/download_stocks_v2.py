"""
下载中国A股数据 - 使用 akshare (免费) - 改进版

覆盖板块:
- 芯片半导体、存储芯片、CPO光学
- 固态电池、六氟磷酸锂、储能
- 光伏、智能电网、机器人、新能源汽车
"""

import time
import yaml
from datetime import datetime, timedelta
import pandas as pd
import akshare as ak
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


# 加载配置
with open('config_multi_sector.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 获取所有股票代码
all_symbols = []
sectors_dict = config['stocks']['sectors']

print("="*80)
print("下载中国A股数据 - 最近3个月 (改进版)")
print("="*80)

print(f"\n板块列表:")
for sector, symbols in sectors_dict.items():
    print(f"  {sector}: {len(symbols)} 只股票")
    all_symbols.extend(symbols)

print(f"\n总计: {len(all_symbols)} 只股票")

# 计算日期范围 (最近3个月)
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

print(
    f"\n日期范围: {start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")

# 创建输出目录
output_dir = Path("data/akshare")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n开始下载...")
print("="*80)

success_count = 0
failed_symbols = []

for i, symbol in enumerate(all_symbols, 1):
    print(f"[{i}/{len(all_symbols)}] {symbol}...", end=' ', flush=True)

    # 重试机制
    max_retries = 3
    df = None

    for retry in range(max_retries):
        try:
            # 使用 akshare 下载数据
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d'),
                adjust="qfq"  # 前复权
            )

            if df is not None and len(df) > 0:
                break  # 成功
            else:
                df = None
                if retry < max_retries - 1:
                    time.sleep(1)

        except Exception as e:
            if retry < max_retries - 1:
                print(f"重试{retry+1}...", end=' ', flush=True)
                time.sleep(2)
            else:
                error_msg = str(e)[:50]
                print(f"✗ {error_msg}")
                failed_symbols.append((symbol, error_msg))
                df = None

    # 保存数据
    if df is not None and len(df) > 0:
        try:
            # 标准化列名
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume',
                '成交额': 'amount',
                '涨跌幅': 'change_pct',
                '涨跌额': 'change',
                '换手率': 'turnover'
            })

            # 保存到 CSV
            output_file = output_dir / f"{symbol}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            print(f"✓ {len(df)} 天")
            success_count += 1

        except Exception as e:
            print(f"✗ 保存失败: {str(e)[:30]}")
            failed_symbols.append((symbol, f"保存失败: {e}"))
    else:
        if (symbol, ) not in [(s, m) for s, m in failed_symbols]:
            print(f"✗ 无数据")
            failed_symbols.append((symbol, "无数据"))

    # 延迟，避免请求过快
    time.sleep(0.5)

# 总结
print("\n" + "="*80)
print(f"下载完成: {success_count}/{len(all_symbols)} 成功")
print("="*80)

if failed_symbols:
    print(f"\n失败的股票 ({len(failed_symbols)}):")
    for sym, reason in failed_symbols[:10]:  # 只显示前10个
        print(f"  - {sym}: {reason}")
    if len(failed_symbols) > 10:
        print(f"  ... 还有 {len(failed_symbols) - 10} 个")

if success_count > 0:
    print(f"\n✓ 数据已保存到: {output_dir.absolute()}")
    print(f"\n下一步:")
    print(f"  python analyze_akshare_data.py")
else:
    print(f"\n⚠️  没有成功下载任何数据")
    print(f"\n可能的原因:")
    print(f"  1. 网络连接问题")
    print(f"  2. akshare 服务暂时不可用")
    print(f"  3. 股票代码不正确")
    print(f"\n建议:")
    print(f"  1. 检查网络连接")
    print(f"  2. 稍后重试")
    print(f"  3. 或使用通达信导出 CSV (见 FINAL_SOLUTION.md)")

print("\n" + "="*80)
