"""
解析通达信 .cod 和 .mdt 文件
"""
import struct
from pathlib import Path
import pandas as pd


def parse_cod_file(cod_path):
    """
    解析 .cod 文件（股票代码文件）

    Returns:
        List of (code, name) tuples
    """
    stocks = []

    with open(cod_path, 'rb') as f:
        while True:
            # 读取一条记录
            data = f.read(50)  # 每条记录约50字节
            if len(data) < 50:
                break

            try:
                # 尝试解析代码和名称
                code = data[:6].decode('gbk', errors='ignore').strip('\x00')
                name = data[6:20].decode('gbk', errors='ignore').strip('\x00')

                if code and code.isdigit():
                    stocks.append((code, name))
            except:
                continue

    return stocks


def parse_mdt_file(mdt_path):
    """
    解析 .mdt 文件（市场数据文件）

    Returns:
        DataFrame with stock data
    """
    data_list = []

    with open(mdt_path, 'rb') as f:
        while True:
            # 每条记录32字节
            data = f.read(32)
            if len(data) < 32:
                break

            try:
                # 解析数据结构
                # 这是一个简化的解析，实际格式可能不同
                values = struct.unpack('8i', data)

                data_list.append({
                    'open': values[0] / 100.0,
                    'high': values[1] / 100.0,
                    'low': values[2] / 100.0,
                    'close': values[3] / 100.0,
                    'volume': values[4],
                    'amount': values[5]
                })
            except:
                continue

    return pd.DataFrame(data_list)


def list_tdx_files():
    """列出所有通达信文件"""
    print("="*70)
    print("通达信数据文件检查")
    print("="*70)

    data_dir = Path(r"D:\projects\TW\src\data")

    # 查找所有日期文件夹
    date_folders = [d for d in data_dir.iterdir() if d.is_dir()
                    and d.name.isdigit()]
    date_folders = sorted(date_folders)

    print(f"\n找到 {len(date_folders)} 个日期文件夹:")

    for folder in date_folders:
        print(f"\n{folder.name}:")

        # 列出文件
        files = list(folder.glob("*"))
        for f in files:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")

        # 尝试解析 .cod 文件
        cod_files = list(folder.glob("*.cod"))
        if cod_files:
            print(f"\n  解析 {cod_files[0].name}...")
            try:
                stocks = parse_cod_file(cod_files[0])
                print(f"  找到 {len(stocks)} 只股票")
                if stocks:
                    print(f"  示例: {stocks[:5]}")
            except Exception as e:
                print(f"  解析失败: {e}")

    print("\n" + "="*70)
    print("⚠️  这些是通达信二进制文件，需要专门的解析器")
    print("="*70)
    print("\n建议:")
    print("1. 使用通达信软件导出为 CSV 格式")
    print("2. 或提供 CSV/Excel 格式的数据文件")
    print("3. 或使用 pytdx 库解析这些文件")


if __name__ == '__main__':
    list_tdx_files()
