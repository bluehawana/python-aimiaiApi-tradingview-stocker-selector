#!/usr/bin/env python3
"""
测试 AIMIAI API - 使用你自己的 API 权限
"""

import os
from dotenv import load_dotenv
import json
import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


# 加载环境变量
load_dotenv()


def test_token_api():
    """测试 Token 获取"""
    print("\n" + "=" * 60)
    print("1. 测试 Token API")
    print("=" * 60)

    app_id = os.getenv('AIMIAI_APP_ID')
    app_key = os.getenv('AIMIAI_APP_KEY')

    print(f"\nAppId: {app_id}")
    print(f"AppKey: {app_key[:10]}..." if app_key and len(
        app_key) > 10 else f"AppKey: {app_key}")

    if not app_id or not app_key or 'your_app' in app_id:
        print("\n❌ 错误: API 凭证未配置")
        print("\n请编辑 .env 文件，填入你的真实凭证:")
        print("AIMIAI_APP_ID=你的真实appId")
        print("AIMIAI_APP_KEY=你的真实appKey")
        print("\n从这里获取: https://aimiai.com/console")
        return None

    # 请求 token
    url = "https://aimiai.com/api/token/get"

    payload = {
        "appId": app_id,
        "appKey": app_key
    }

    headers = {
        'Content-Type': 'application/json'
    }

    print(f"\n📡 请求 URL: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")

    try:
        print("\n⏳ 发送请求...")
        response = requests.post(
            url, json=payload, headers=headers, timeout=10)

        print(f"📊 状态码: {response.status_code}")
        print(f"📄 响应: {response.text[:200]}")

        if response.status_code == 200:
            result = response.json()

            if result.get('code') == 0:
                token = result.get('data')
                print(f"\n✅ Token 获取成功!")
                print(f"🔑 Token: {token[:30]}...")
                return token
            else:
                print(f"\n❌ API 返回错误:")
                print(f"   Code: {result.get('code')}")
                print(f"   Message: {result.get('message')}")
                return None
        else:
            print(f"\n❌ HTTP 错误: {response.status_code}")
            print(f"   响应: {response.text}")
            return None

    except Exception as e:
        print(f"\n❌ 请求失败: {e}")
        return None


def test_stock_data_api(token: str):
    """测试股票数据 API"""
    print("\n" + "=" * 60)
    print("2. 测试股票数据 API")
    print("=" * 60)

    if not token:
        print("⚠️  跳过 (没有有效 token)")
        return

    # 尝试不同的可能端点
    possible_endpoints = [
        "/stock/history",
        "/stock/data",
        "/stock/kline",
        "/market/stock/history",
        "/data/stock/history"
    ]

    test_symbol = "600036"  # 招商银行

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "symbol": test_symbol,
        "days": 10
    }

    for endpoint in possible_endpoints:
        url = f"https://aimiai.com/api{endpoint}"
        print(f"\n📡 尝试: {url}")

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=10)
            print(f"   状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(
                    f"   响应: {json.dumps(result, ensure_ascii=False)[:100]}...")

                if result.get('code') == 0:
                    print(f"   ✅ 此端点可用!")
                    return endpoint
            elif response.status_code == 404:
                print(f"   ⚠️  端点不存在")
            else:
                print(f"   ❌ 错误: {response.text[:100]}")

        except Exception as e:
            print(f"   ❌ 请求失败: {str(e)[:50]}")

    print("\n⚠️  未找到可用的股票数据端点")
    return None


def check_api_documentation():
    """检查 API 文档"""
    print("\n" + "=" * 60)
    print("3. API 文档检查")
    print("=" * 60)

    print("\n💡 请提供以下信息:")
    print("\n1. aimiai.com API 文档地址")
    print("2. 股票数据接口的端点 (endpoint)")
    print("3. 请求格式示例")
    print("4. 响应格式示例")

    print("\n📝 示例:")
    print("   端点: https://aimiai.com/api/stock/history")
    print("   请求: {\"symbol\": \"600036\", \"days\": 100}")
    print("   响应: {\"code\": 0, \"data\": [{\"date\": \"2025-11-17\", ...}]}")


def main():
    """主函数"""
    print("\n🔍 AIMIAI API 测试工具")
    print("=" * 60)
    print("目标: 使用你自己的 aimiai.com API 获取股票数据")
    print("=" * 60)

    # 测试 Token API
    token = test_token_api()

    # 测试股票数据 API
    if token:
        endpoint = test_stock_data_api(token)

        if not endpoint:
            check_api_documentation()

    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)

    if token:
        print("\n✅ Token API 工作正常")
        print("⏳ 需要确认股票数据 API 端点")
        print("\n💡 下一步:")
        print("1. 查看 aimiai.com API 文档")
        print("2. 找到股票数据接口的正确端点")
        print("3. 更新 src/data/aimiai_stock_api.py 中的 URL")
        print("4. 重新运行此测试")
    else:
        print("\n❌ Token API 失败")
        print("\n💡 请检查:")
        print("1. .env 文件中的凭证是否正确")
        print("2. 凭证是否已激活")
        print("3. 网络连接是否正常")
        print("4. aimiai.com 服务是否正常")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
