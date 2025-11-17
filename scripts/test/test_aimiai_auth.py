"""
测试 aimiai.com API 认证和数据获取
Test aimiai.com API authentication and data fetching
"""

import os
import sys
from dotenv import load_dotenv
import requests
import json

# 加载环境变量
load_dotenv()


def test_authentication():
    """测试认证流程"""
    print("\n" + "=" * 60)
    print("测试 aimiai.com API 认证")
    print("=" * 60)

    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')

    if not app_id or not app_key:
        print("❌ 错误: 未找到 AppId 或 AppKey")
        print("请在 .env 文件中配置:")
        print("AppId=你的_app_id")
        print("AppKey=你的_app_key")
        return None

    print(f"✅ AppId: {app_id[:10]}...")
    print(f"✅ AppKey: {app_key[:10]}...")

    # 测试获取 token
    print("\n📝 步骤 1: 获取访问令牌...")

    token_url = "https://aimiai.com/api/auth/token"

    headers = {
        'Content-Type': 'application/json',
        'AppId': app_id,
        'AppKey': app_key
    }

    try:
        response = requests.post(token_url, headers=headers, timeout=10)
        print(f"   状态码: {response.status_code}")

        result = response.json()
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if response.status_code == 200:
            token = result.get('data') or result.get('token')
            if token:
                print(f"✅ Token 获取成功: {token[:20]}...")
                return token
            else:
                print("⚠️  响应中未找到 token")
                return None
        else:
            print(f"❌ 认证失败: {result.get('message', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def test_stock_data(token):
    """测试获取股票数据"""
    if not token:
        print("\n⚠️  跳过股票数据测试 (无有效 token)")
        return

    print("\n" + "=" * 60)
    print("测试获取股票数据")
    print("=" * 60)

    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')

    # 测试股票代码
    test_symbol = "600036"  # 招商银行

    print(f"\n📊 获取 {test_symbol} 的K线数据...")

    url = "https://aimiai.com/api/stock/kline"

    headers = {
        'Content-Type': 'application/json',
        'AppId': app_id,
        'AppKey': app_key,
        'Token': token
    }

    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)

    payload = {
        "code": test_symbol,
        "startDate": start_date.strftime('%Y%m%d'),
        "endDate": end_date.strftime('%Y%m%d'),
        "klt": "101",  # 日K线
        "fqt": "1"     # 前复权
    }

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=30)
        print(f"   状态码: {response.status_code}")

        result = response.json()
        print(
            f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")

        if response.status_code == 200:
            data = result.get('data') or result.get('result', [])
            if data:
                print(f"✅ 成功获取 {len(data)} 条数据")
                if len(data) > 0:
                    print(f"   示例数据: {data[0]}")
            else:
                print("⚠️  响应中无数据")
        else:
            print(f"❌ 获取数据失败: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")


def test_api_endpoints():
    """测试不同的 API endpoints"""
    print("\n" + "=" * 60)
    print("测试 API Endpoints")
    print("=" * 60)

    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')

    # 可能的 token endpoints
    token_endpoints = [
        "https://aimiai.com/api/auth/token",
        "https://aimiai.com/api/token/get",
        "https://aimiai.com/api/v1/auth/token",
    ]

    headers = {
        'Content-Type': 'application/json',
        'AppId': app_id,
        'AppKey': app_key
    }

    for endpoint in token_endpoints:
        print(f"\n测试: {endpoint}")
        try:
            response = requests.post(endpoint, headers=headers, timeout=5)
            print(f"   状态码: {response.status_code}")
            if response.status_code != 404:
                result = response.json()
                print(
                    f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
        except Exception as e:
            print(f"   错误: {e}")


if __name__ == "__main__":
    print("\n🚀 开始测试 aimiai.com API")
    print("参考文档: https://aimiai.com/doc/authentication")

    # 测试认证
    token = test_authentication()

    # 测试获取数据
    if token:
        test_stock_data(token)
    else:
        # 如果认证失败，尝试测试不同的 endpoints
        print("\n尝试其他 API endpoints...")
        test_api_endpoints()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
