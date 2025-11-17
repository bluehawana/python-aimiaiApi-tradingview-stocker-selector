"""
显示24只金叉股票列表（带中文名称）
"""
import pandas as pd


def display_stocks():
    """显示金叉股票"""
    df = pd.read_csv('results/golden_cross_with_names.csv')

    print("=" * 80)
    print("24只金叉股票列表 (Golden Cross Stocks)")
    print("=" * 80)
    print()

    # 按状态分组
    golden = df[df['status'] == '已金叉'].copy()
    near_golden = df[df['status'] == '接近金叉'].copy()

    print(f"【已金叉】 {len(golden)} 只")
    print("-" * 80)
    for i, (_, row) in enumerate(golden.iterrows(), 1):
        print(f"{i:2d}. {row['name']:6s} ({row['symbol']}) - "
              f"价格: ¥{row['close']:>8.2f} | "
              f"Gap: {row['gap']:>6.2f}% | "
              f"PC: {row['pc']:>5.1f}% | "
              f"{row['recommendation']}")

    print()
    print(f"【接近金叉】 {len(near_golden)} 只")
    print("-" * 80)
    for i, (_, row) in enumerate(near_golden.iterrows(), 1):
        print(f"{i:2d}. {row['name']:6s} ({row['symbol']}) - "
              f"价格: ¥{row['close']:>8.2f} | "
              f"Gap: {row['gap']:>6.2f}% | "
              f"PC: {row['pc']:>5.1f}% | "
              f"{row['recommendation']}")

    print()
    print("=" * 80)
    print("🎯 重点关注 (Strong Hold, PC > 90%):")
    print("-" * 80)
    strong = golden[golden['behavior'] == 'Strong Hold']
    for _, row in strong.iterrows():
        print(
            f"⭐ {row['name']} ({row['symbol']}) - PC: {row['pc']:.1f}%, Gap: {row['gap']:.1f}%")

    print()
    print("=" * 80)


if __name__ == '__main__':
    display_stocks()
