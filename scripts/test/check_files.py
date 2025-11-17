"""
简单检查文件是否存在
"""
from pathlib import Path

print("="*70)
print("检查文件")
print("="*70)

# 检查桌面文件
desktop = Path(r"C:\Users\BLUEH\OneDrive\桌面")
print(f"\n1. 检查桌面: {desktop}")

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

desktop_found = 0
for zf in zip_files:
    path = desktop / zf
    if path.exists():
        size = path.stat().st_size / (1024*1024)
        print(f"  ✓ {zf} ({size:.1f} MB)")
        desktop_found += 1
    else:
        print(f"  ✗ {zf} (不存在)")

print(f"\n桌面找到: {desktop_found}/{len(zip_files)} 个文件")

# 检查 data/local 目录
data_dir = Path("data/local")
print(f"\n2. 检查 data/local: {data_dir.absolute()}")

if not data_dir.exists():
    print(f"  ✗ 目录不存在")
    print(f"\n请运行: 1_IMPORT_DATA.bat")
else:
    local_zips = list(data_dir.glob("*.zip"))
    print(f"  找到 {len(local_zips)} 个 ZIP 文件:")
    for zf in local_zips:
        size = zf.stat().st_size / (1024*1024)
        print(f"    - {zf.name} ({size:.1f} MB)")

print("\n" + "="*70)

# 如果桌面有文件但 data/local 没有
if desktop_found > 0 and (not data_dir.exists() or len(list(data_dir.glob("*.zip"))) == 0):
    print("\n下一步: 运行 1_IMPORT_DATA.bat 导入文件")
elif data_dir.exists() and len(list(data_dir.glob("*.zip"))) > 0:
    print("\n✓ 文件已导入，可以运行分析")
    print("下一步: 运行 INSPECT_ZIP.bat 查看数据格式")
else:
    print("\n✗ 未找到 ZIP 文件")
    print("请确认文件在桌面上")

print("="*70)
