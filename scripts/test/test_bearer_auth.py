"""
Test Bearer Token Authentication with aimiai.com API
"""
from src.data.aimiai_stock_api import AimiaiStockAPI
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


load_dotenv()


def test_bearer_auth():
    """Test Bearer token authentication"""
    print("=" * 70)
    print("Bearer Token Authentication Test")
    print("=" * 70)

    # Check token in .env
    token = os.getenv('token')
    if token:
        print(f"\n✓ Token found in .env:")
        print(f"  {token[:30]}...")
    else:
        print(f"\n✗ No token found in .env")
        print(f"  Will request new token from API")

    # Initialize API
    print(f"\n[1/3] Initializing API client...")
    try:
        api = AimiaiStockAPI()
        print(f"✓ API client initialized")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return False

    # Get token (will use .env token or request new one)
    print(f"\n[2/3] Getting token...")
    try:
        token = api.get_token()
        print(f"✓ Token ready: {token[:30]}...")
    except Exception as e:
        print(f"✗ Failed to get token: {e}")
        return False

    # Test API call with Bearer token
    print(f"\n[3/3] Testing API call with Bearer token...")
    print(f"  Authorization: Bearer {token[:20]}...")

    try:
        # Test with a simple stock query
        df = api.get_stock_data("600036", days=5)

        if df is not None and len(df) > 0:
            print(f"✓ API call successful!")
            print(f"\n  Stock: 600036 (招商银行)")
            print(f"  Data points: {len(df)}")
            print(f"  Latest date: {df['date'].iloc[-1]}")
            print(f"  Latest close: ¥{df['close'].iloc[-1]:.2f}")
            print(f"  Latest volume: {df['volume'].iloc[-1]/1e6:.1f}M")

            print(f"\n" + "=" * 70)
            print(f"✓ Bearer token authentication working!")
            print(f"=" * 70)
            return True
        else:
            print(f"✗ No data returned")
            return False

    except Exception as e:
        print(f"✗ API call failed: {e}")
        print(f"\nTroubleshooting:")
        print(f"  1. Check if token is valid")
        print(f"  2. Verify API endpoint is correct")
        print(f"  3. Ensure Authorization header format: 'Bearer {{token}}'")
        return False


if __name__ == '__main__':
    success = test_bearer_auth()

    if success:
        print(f"\n🎉 Ready to use Shannon Pattern Finder!")
        print(f"   Run: python find_shannon_pattern.py")
    else:
        print(f"\n⚠️  Please fix the issues above before proceeding")

    sys.exit(0 if success else 1)
