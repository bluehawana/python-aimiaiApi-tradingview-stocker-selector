"""
简单的 API 连接测试
"""
import json
from dotenv import load_dotenv
import requests
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


load_dotenv()


def test_connection():
    """测试 API 连接"""
    print("=" * 70)
    print("API 连接测试")
    print("=" * 70)

    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')
    token = os.getenv('token')

    print(f"\n配置信息:")
    print(f"  AppId: {app_id}")
    print(f"  AppKey: {app_key[:10]}..." if app_key else "  AppKey: None")
    print(f"  Token: {token[:30]}..." if token else "  Token: None")

    # 测试 1: 获取新 token
    print(f"\n[测试 1] 获取新 token")
    print(f"  POST https://aimiai.com/api/token/get")

    try:
        response = requests.post(
            "https://aimiai.com/api/token/get",
            json={"appId": app_id, "appKey": app_key},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            new_token = result.get('data') or result.get('token')
            if new_token:
                print(f"  ✓ 获取 token 成功")
                token = new_token
            else:
                print(f"  ✗ 响应中没有 token")
                print(f"\n请检查:")
                print(f"  1. AppId 和 AppKey 是否正确")
                print(f"  2. aimiai.com 账号是否有效")
                print(f"  3. API 端点是否正确")
                return
        else:
            print(f"  ✗ 获取 token 失败")
            return

    except Exception as e:
        print(f"  ✗ 请求失败: {e}")
        return

    # 测试 2: 使用 token 获取数据
    print(f"\n[测试 2] 使用 token 获取股票数据")
    print(f"  POST https://aimiai.com/api/stock/kline")
    print(f"  Authorization: Bearer {token[:20]}...")

    try:
        response = requests.post(
            "https://aimiai.com/api/stock/kline",
            json={
                "code": "600036",
                "startDate": "20241101",
                "endDate": "20241117",
                "klt": "101",
                "fqt": "1"
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            },
            timeout=10
        )

        print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"  Response code: {result.get('code')}")
            print(
                f"  Response message: {result.get('message') or result.get('msg')}")

            if result.get('code') == 200:
                data = result.get('data', [])
                print(f"  ✓ 获取数据成功，共 {len(data)} 条记录")
                if len(data) > 0:
                    print(f"  示例数据: {data[0]}")
            else:
                print(f"  ✗ API 返回错误")
                print(
                    f"  完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"  ✗ HTTP 错误: {response.status_code}")
            print(f"  Response: {response.text[:300]}")

    except Exception as e:
        print(f"  ✗ 请求失败: {e}")
        return

    print(f"\n" + "=" * 70)
    print(f"✓ 测试完成")
    print(f"=" * 70)


if __name__ == '__main__':
    test_connection()
