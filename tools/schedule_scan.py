"""
定时扫描调度器
在指定时间自动运行Shannon扫描
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_scan():
    """运行扫描"""
    print("\n" + "=" * 80)
    print(f"开始扫描 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    try:
        # 步骤1: 下载数据
        print("\n步骤 1/2: 下载数据...")
        result1 = subprocess.run(
            [sys.executable, "scripts/download/download_all_stocks.py"],
            check=True
        )

        # 步骤2: 扫描Shannon
        print("\n步骤 2/2: 扫描Shannon...")
        result2 = subprocess.run(
            [sys.executable, "scripts/find_all_shannon.py"],
            check=True
        )

        print("\n" + "=" * 80)
        print(f"✓ 扫描完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n✗ 扫描失败: {e}")
        return False
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        return False


def schedule_for_today_22pm():
    """安排今晚22:00运行"""
    # 安排今晚22:00运行
    schedule.every().day.at("22:00").do(run_scan)

    print("=" * 80)
    print("Shannon扫描定时任务")
    print("=" * 80)
    print()
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"计划时间: 今晚 22:00")
    print()
    print("任务已设置，等待执行...")
    print("按 Ctrl+C 取消")
    print("=" * 80)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

            # 显示倒计时
            now = datetime.now()
            if now.hour < 22:
                hours_left = 22 - now.hour - 1
                minutes_left = 60 - now.minute
                print(
                    f"\r距离执行还有: {hours_left}小时 {minutes_left}分钟", end='', flush=True)
            elif now.hour == 22 and now.minute == 0:
                print("\n\n开始执行...")

    except KeyboardInterrupt:
        print("\n\n任务已取消")


def schedule_custom_time(hour, minute):
    """安排自定义时间运行"""
    time_str = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(time_str).do(run_scan)

    print("=" * 80)
    print("Shannon扫描定时任务")
    print("=" * 80)
    print()
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"计划时间: 每天 {time_str}")
    print()
    print("任务已设置，等待执行...")
    print("按 Ctrl+C 取消")
    print("=" * 80)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n\n任务已取消")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Shannon扫描定时任务')
    parser.add_argument('--time', type=str,
                        help='执行时间 (HH:MM)', default='22:00')
    parser.add_argument('--now', action='store_true', help='立即执行')

    args = parser.parse_args()

    if args.now:
        # 立即执行
        print("立即执行扫描...")
        run_scan()
    else:
        # 定时执行
        hour, minute = map(int, args.time.split(':'))

        if args.time == '22:00':
            schedule_for_today_22pm()
        else:
            schedule_custom_time(hour, minute)


if __name__ == '__main__':
    main()
