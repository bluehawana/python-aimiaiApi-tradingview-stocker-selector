"""
全自动Shannon扫描 - 一键运行
自动下载数据 + 扫描分析 + 导出结果
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def run_script(script_name, description):
    """运行Python脚本"""
    print(f"正在执行: {description}...")
    print(f"脚本: {script_name}")
    print("-" * 80)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✓ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} 失败")
        print(f"错误: {e}")
        return False
    except Exception as e:
        print(f"\n✗ {description} 失败")
        print(f"错误: {e}")
        return False


def main():
    """主函数"""
    start_time = datetime.now()

    print_header("全自动Shannon扫描系统")
    print("自动执行流程:")
    print("  1. 下载全市场数据 (180天, 5000+ 只股票)")
    print("  2. 扫描Shannon候选 (Shannon + Ichimoku + MCDX)")
    print("  3. 导出结果到 results/ 文件夹")
    print()
    print("预计总时间: 40-60 分钟")
    print()
    input("按 Enter 键开始...")

    # 步骤1: 下载数据
    print_header("步骤 1/2: 下载全市场数据")
    print("预计时间: 30-40 分钟")
    print()

    if not run_script("download_all_stocks.py", "数据下载"):
        print("\n❌ 下载失败！请检查:")
        print("   1. Tushare Token 是否配置")
        print("   2. 网络连接是否正常")
        return False

    # 步骤2: 扫描Shannon
    print_header("步骤 2/2: 扫描Shannon候选")
    print("预计时间: 10-15 分钟")
    print()

    if not run_script("find_all_shannon.py", "Shannon扫描"):
        print("\n❌ 扫描失败！")
        return False

    # 完成
    end_time = datetime.now()
    duration = end_time - start_time

    print_header("🎉 全部完成！")
    print(f"总耗时: {duration}")
    print()
    print("结果文件已保存到 results/ 文件夹:")
    print("  - all_shannon_*.csv      (全部候选)")
    print("  - super_shannon_*.csv    (超级信号, >=80分)")
    print("  - tech_shannon_*.csv     (科技股候选)")
    print()
    print("=" * 80)

    # 打开结果文件夹
    results_dir = Path("results")
    if results_dir.exists():
        import os
        if sys.platform == 'win32':
            os.startfile(results_dir)
        elif sys.platform == 'darwin':
            subprocess.run(['open', results_dir])
        else:
            subprocess.run(['xdg-open', results_dir])

    return True


if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n✓ 扫描成功完成！")
            sys.exit(0)
        else:
            print("\n✗ 扫描失败")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误: {e}")
        sys.exit(1)
