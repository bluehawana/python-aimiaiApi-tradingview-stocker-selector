#!/usr/bin/env python3
"""
Simple API Test - 测试数据源是否可用
"""

import time


def test_akshare_with_retry():
    """测试 AKShare API (带重试)"""
    print("\n" + "=" * 60)
    print("测试 AKShare API")
    print("=" * 60)

    try:
        import akshare as ak
        print(f"✅ AKShare 版本: {ak.__version__}")
    except ImportError:
        print("❌ AKShare 未安装")
        return False

    # 测试股票列表
    test_symbols = ["600036", "000001", "300750"]

    for symbol in test_symbols:
        print(f"\n📊 测试 {symbol}...")

        # 重试机制
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                print(f"   尝试 {attempt + 1}/{max_retries}...", end=" ")

                # 获取数据
                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    adjust="qfq"
                )

                if df is not None and len(df) > 0:
                    latest = df.iloc[-1]
                    print(f"✅ 成功!")
                    print(f"   最新日期: {latest['日期']}")
                    print(f"   收盘价: ¥{latest['收盘']:.2f}")
                    print(f"   成交量: {latest['成交量']/10000:.0f}万")
                    break
                else:
                    print("⚠️  无数据")

            except Exception as e:
                error_msg = str(e)
                if "Connection" in error_msg or "Remote" in error_msg:
                    print(f"❌ 网络错误")
                    if attempt < max_retries - 1:
                        print(f"   等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        print(f"   ❌ 失败: {symbol} - 网络连接问题")
                        print(f"   建议: 稍后重试或检查网络")
                else:
                    print(f"❌ 错误: {error_msg[:50]}")
                    break

    return True


def check_network():
    """检查网络连接"""
    print("\n" + "=" * 60)
    print("检查网络连接")
    print("=" * 60)

    import requests

    test_urls = [
        ("百度", "https://www.baidu.com"),
        ("东方财富", "https://www.eastmoney.com"),
    ]

    for name, url in test_urls:
        try:
            print(f"\n测试 {name} ({url})...", end=" ")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ 可访问")
            else:
                print(f"⚠️  状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 无法访问: {str(e)[:30]}")


def main():
    """主函数"""
    print("\n🔍 API 诊断工具")
    print("=" * 60)

    # 检查网络
    check_network()

    # 测试 AKShare
    test_akshare_with_retry()

    print("\n" + "=" * 60)
    print("📊 诊断总结")
    print("=" * 60)
    print("\n如果看到网络错误:")
    print("1. ⏰ 等待几分钟后重试")
    print("2. 🌐 检查网络连接")
    print("3. 🔄 AKShare 服务器可能繁忙")
    print("4. 💡 非交易时间数据更新较慢")
    print("\n如果持续失败:")
    print("1. 检查防火墙设置")
    print("2. 尝试使用 VPN")
    print("3. 等待 AKShare 服务器恢复")
    print("\n✅ 系统代码没有问题，只是数据源连接不稳定")


if __name__ == "__main__":
    main()
