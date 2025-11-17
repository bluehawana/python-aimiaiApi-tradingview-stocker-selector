"""
API 诊断工具 - 检查 aimiai.com API 连接问题
"""
import json
from dotenv import load_dotenv
import requests
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


load_dotenv()


def diagnose_api():
    """诊断 API 连接问题"""
    print("=" * 80)
    print("aimiai.com API 诊断工具")
    print("=" * 80)

    # 步骤 1: 检查环境变量
    print("\n[1/5] 检查环境变量...")
    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')
    token = os.getenv('token')

    if not app_id or not app_key:
        print("  ✗ AppId 或 AppKey 未配置")
        return False

    print(f"  ✓ AppId: {app_id[:20]}...")
    print(f"  ✓ AppKey: {app_key[:20]}...")

    if token:
        print(f"  ✓ Token: {token[:30]}...")
        # 检查 token 是否过期
        try:
            import jwt
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp', 0)
            from datetime import datetime
            exp_date = datetime.fromtimestamp(exp)
            print(f"  ℹ Token 过期时间: {exp_date}")
            if datetime.now().timestamp() > exp:
                print(f"  ⚠ Token 已过期！")
        except:
            print(f"  ℹ 无法解析 token 过期时间")
    else:
        print(f"  ⚠ 没有预设 token，将请求新 token")

    # 步骤 2: 测试获取 token
    print("\n[2/5] 测试获取 token...")
    token_url = "https://aimiai.com/api/token/get"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "appId": app_id,
        "appKey": app_key
    }

    print(f"  → POST {token_url}")
    print(f"  → Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            token_url,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(f"  ← Status: {response.status_code}")
        print(f"  ← Response: {response.text[:200]}...")

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200 or result.get('success'):
                new_token = result.get('data') or result.get('token')
                if new_token:
                    print(f"  ✓ 成功获取 token: {new_token[:30]}...")
                    token = new_token
                else:
                    print(f"  ✗ 响应中没有 token")
                    print(
                        f"  完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return False
            else:
                print(f"  ✗ API 返回错误")
                print(
                    f"  完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return False
        else:
            print(f"  ✗ HTTP 错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"  ✗ 请求失败: {e}")
        return False

    # 步骤 3: 测试业务 API（获取股票数据）
    print("\n[3/5] 测试业务 API（获取股票数据）...")

    # 尝试不同的 API 端点
    test_endpoints = [
        {
            'name': '获取K线数据',
            'url': 'https://aimiai.com/api/stock/kline',
            'method': 'POST',
            'body': {
                "code": "600036",
                "startDate": "20241001",
                "endDate": "20241117",
                "klt": "101",
                "fqt": "1"
            }
        },
        {
            'name': '获取股票列表',
            'url': 'https://aimiai.com/api/stock/list',
            'method': 'POST',
            'body': {}
        },
        {
            'name': '获取实时行情',
            'url': 'https://aimiai.com/api/stock/quote',
            'method': 'POST',
            'body': {
                "code": "600036"
            }
        }
    ]

    for endpoint in test_endpoints:
        print(f"\n  测试: {endpoint['name']}")
        print(f"  → {endpoint['method']} {endpoint['url']}")

        # 尝试 Bearer token 格式
        headers_bearer = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        print(f"  → Authorization: Bearer {token[:20]}...")

        try:
            response = requests.post(
                endpoint['url'],
                json=endpoint['body'],
                headers=headers_bearer,
                timeout=10
            )

            print(f"  ← Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    result = response.json()
                    print(
                        f"  ← Response: {json.dumps(result, indent=2, ensure_ascii=False)[:300]}...")

                    if result.get('code') == 200 or result.get('success'):
                        print(f"  ✓ {endpoint['name']} 成功")
                    else:
                        print(
                            f"  ✗ API 返回错误: {result.get('message') or result.get('msg')}")
                except:
                    print(f"  ← Response (text): {response.text[:200]}...")
            else:
                print(f"  ✗ HTTP 错误: {response.status_code}")
                print(f"  ← Response: {response.text[:200]}...")

        except Exception as e:
            print(f"  ✗ 请求失败: {e}")

    # 步骤 4: 检查网络连接
    print("\n[4/5] 检查网络连接...")
    try:
        response = requests.get("https://aimiai.com", timeout=5)
        print(f"  ✓ 可以访问 aimiai.com (Status: {response.status_code})")
    except Exception as e:
        print(f"  ✗ 无法访问 aimiai.com: {e}")
        return False

    # 步骤 5: 总结
    print("\n[5/5] 诊断总结")
    print("=" * 80)
    print("\n可能的问题:")
    print("1. Token 已过期 - 需要重新获取")
    print("2. API 端点不正确 - 需要确认正确的 API 地址")
    print("3. 认证格式不对 - 需要确认 Header 格式")
    print("4. API 权限问题 - 需要确认账号权限")

    print("\n建议操作:")
    print("1. 删除 .env 中的 token 行，让系统重新获取")
    print("2. 联系 aimiai.com 确认 API 文档和端点")
    print("3. 检查账号是否有 API 调用权限")
    print("4. 查看 aimiai.com 控制台的 API 使用情况")

    print("\n" + "=" * 80)

    return True


if __name__ == '__main__':
    try:
        diagnose_api()
    except Exception as e:
        print(f"\n诊断过程出错: {e}")
        import traceback
        traceback.print_exc()
