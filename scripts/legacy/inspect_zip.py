"""
检查 ZIP 文件内容
"""
import zipfile
from pathlib import Path
import pandas as pd


def inspect_zip_file(zip_path):
    """检查单个 ZIP 文件"""
    print(f"\n{'='*70}")
    print(f"检查文件: {zip_path.name}")
    print(f"{'='*70}")

    if not zip_path.exists():
        print(f"✗ 文件不存在: {zip_path}")
        return

    # 文件大小
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"文件大小: {size_mb:.2f} MB")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 列出所有文件
            file_list = zip_ref.namelist()
            print(f"\nZIP 包含 {len(file_list)} 个文件:")

            for i, file_name in enumerate(file_list[:10], 1):  # 只显示前10个
                file_info = zip_ref.getinfo(file_name)
                file_size = file_info.file_size / 1024  # KB
                print(f"  {i}. {file_name} ({file_size:.1f} KB)")

            if len(file_list) > 10:
                print(f"  ... 还有 {len(file_list) - 10} 个文件")

            # 尝试读取第一个文件
            print(f"\n尝试读取第一个文件...")
            first_file = None
            for file_name in file_list:
                if not file_name.endswith('/') and not file_name.startswith('.'):
                    first_file = file_name
                    break

            if first_file:
                print(f"读取: {first_file}")

                try:
                    with zip_ref.open(first_file) as f:
                        # 尝试不同的读取方式
                        if first_file.endswith('.csv'):
                            # 尝试不同的编码
                            for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']:
                                try:
                                    df = pd.read_csv(
                                        f, encoding=encoding, nrows=5)
                                    print(f"✓ 成功读取 (编码: {encoding})")
                                    print(f"\n数据预览:")
                                    print(f"  行数: {len(df)}")
                                    print(f"  列数: {len(df.columns)}")
                                    print(f"  列名: {list(df.columns)}")
                                    print(f"\n前3行:")
                                    print(df.head(3).to_string())
                                    break
                                except Exception as e:
                                    if encoding == 'utf-8-sig':
                                        print(f"✗ 无法读取 CSV: {e}")
                                    continue

                        elif first_file.endswith(('.xls', '.xlsx')):
                            df = pd.read_excel(f, nrows=5)
                            print(f"✓ 成功读取 Excel")
                            print(f"\n数据预览:")
                            print(f"  行数: {len(df)}")
                            print(f"  列数: {len(df.columns)}")
                            print(f"  列名: {list(df.columns)}")
                            print(f"\n前3行:")
                            print(df.head(3).to_string())

                        else:
                            print(f"⚠ 未知文件类型: {first_file}")

                except Exception as e:
                    print(f"✗ 读取失败: {e}")

    except Exception as e:
        print(f"✗ 无法打开 ZIP 文件: {e}")


def main():
    """主函数"""
    print("="*70)
    print("ZIP 文件内容检查工具")
    print("="*70)

    # 检查 data/local 目录
    data_dir = Path("data/local")

    if not data_dir.exists():
        print(f"\n✗ 目录不存在: {data_dir}")
        print(f"请先运行: 1_IMPORT_DATA.bat")
        return

    # 查找所有 ZIP 文件
    zip_files = list(data_dir.glob("*.zip"))

    if len(zip_files) == 0:
        print(f"\n✗ 没有找到 ZIP 文件")
        print(f"请先运行: 1_IMPORT_DATA.bat")
        return

    print(f"\n找到 {len(zip_files)} 个 ZIP 文件")

    # 检查第一个文件（详细）
    if len(zip_files) > 0:
        inspect_zip_file(zip_files[0])

    # 列出其他文件
    if len(zip_files) > 1:
        print(f"\n{'='*70}")
        print(f"其他文件:")
        print(f"{'='*70}")
        for zip_file in zip_files[1:]:
            size_mb = zip_file.stat().st_size / (1024 * 1024)
            print(f"  - {zip_file.name} ({size_mb:.2f} MB)")

    print(f"\n{'='*70}")
    print(f"检查完成")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
