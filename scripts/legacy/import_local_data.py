"""
导入本地 ZIP 数据文件

将桌面上的 ZIP 文件复制到项目的 data/local 目录
"""

import shutil
from pathlib import Path


def import_zip_files():
    """导入 ZIP 文件"""
    print("=" * 70)
    print("导入本地数据文件")
    print("=" * 70)

    # 源文件路径（桌面）
    desktop = Path(r"C:\Users\BLUEH\OneDrive\桌面")

    # 目标目录
    target_dir = Path("data/local")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 要导入的文件
    zip_files = [
        "20251106.zip",
        "20251107.zip",
        "20251110.zip",
        "20251111.zip",
        "20251112.zip",
        "20251113.zip",
        "20251114.zip",
        "20251117.zip"
    ]

    print(f"\n源目录: {desktop}")
    print(f"目标目录: {target_dir.absolute()}")
    print(f"\n准备导入 {len(zip_files)} 个文件...")

    success_count = 0
    failed_files = []

    for zip_file in zip_files:
        source = desktop / zip_file
        target = target_dir / zip_file

        print(f"\n处理: {zip_file}")

        if not source.exists():
            print(f"  ✗ 源文件不存在: {source}")
            failed_files.append(zip_file)
            continue

        try:
            # 复制文件
            shutil.copy2(source, target)

            # 检查文件大小
            size_mb = target.stat().st_size / (1024 * 1024)
            print(f"  ✓ 复制成功: {size_mb:.2f} MB")
            success_count += 1

        except Exception as e:
            print(f"  ✗ 复制失败: {e}")
            failed_files.append(zip_file)

    # 总结
    print("\n" + "=" * 70)
    print(f"导入完成: {success_count}/{len(zip_files)} 个文件成功")
    print("=" * 70)

    if failed_files:
        print(f"\n失败的文件:")
        for f in failed_files:
            print(f"  - {f}")

    if success_count > 0:
        print(f"\n✓ 数据文件已导入到: {target_dir.absolute()}")
        print(f"\n下一步:")
        print(f"  1. 运行测试: python src/data/local_data_loader.py")
        print(f"  2. 运行分析: python analyze_local_data.py")

    return success_count > 0


if __name__ == '__main__':
    import_zip_files()
