"""
Quick test to verify Shannon Pattern Finder setup
"""
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


load_dotenv()


def test_setup():
    """Test the setup"""
    print("=" * 70)
    print("Shannon Pattern Finder - Setup Test")
    print("=" * 70)

    # Test 1: Check .env file
    print("\n[1/4] Checking .env configuration...")
    app_id = os.getenv('AppId')
    app_key = os.getenv('AppKey')
    rapidapi_key = os.getenv('RAPIDAPI_KEY')

    if app_id and app_key:
        print(f"  ✓ aimiai.com credentials found")
        print(f"    AppId: {app_id[:10]}...")
        print(f"    AppKey: {app_key[:10]}...")
    else:
        print(f"  ✗ aimiai.com credentials missing!")
        print(f"    Please add AppId and AppKey to .env file")
        return False

    if rapidapi_key:
        print(f"  ✓ RapidAPI key found (Yahoo Finance)")
        print(f"    Key: {rapidapi_key[:10]}...")
    else:
        print(f"  ⚠ RapidAPI key not found (optional)")

    # Test 2: Check config file
    print("\n[2/4] Checking configuration file...")
    config_file = Path('config_multi_sector.yaml')
    if config_file.exists():
        print(f"  ✓ config_multi_sector.yaml found")

        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        sectors = config.get('stocks', {}).get('sectors', {})
        total_stocks = sum(len(symbols) for symbols in sectors.values())
        print(f"  ✓ {len(sectors)} sectors configured")
        print(f"  ✓ {total_stocks} stocks to scan")
    else:
        print(f"  ✗ config_multi_sector.yaml not found!")
        return False

    # Test 3: Check modules
    print("\n[3/4] Checking Python modules...")
    try:
        from src.data.aimiai_stock_api import AimiaiStockAPI
        print(f"  ✓ aimiai_stock_api module loaded")

        from src.mcdx.calculator import MCDXCalculator
        print(f"  ✓ MCDX calculator module loaded")

        from src.mcdx.volume_analyzer import VolumeAnalyzer
        print(f"  ✓ Volume analyzer module loaded")

    except ImportError as e:
        print(f"  ✗ Module import failed: {e}")
        return False

    # Test 4: Test API connection
    print("\n[4/4] Testing aimiai.com API connection...")
    try:
        api = AimiaiStockAPI()
        print(f"  ✓ API client initialized")

        print(f"  → Requesting token...")
        token = api.get_token()
        if token:
            print(f"  ✓ Token obtained: {token[:20]}...")
        else:
            print(f"  ✗ Failed to get token")
            return False

    except Exception as e:
        print(f"  ✗ API test failed: {e}")
        print(f"\n  Troubleshooting:")
        print(f"  1. Check your AppId and AppKey in .env")
        print(f"  2. Verify network connection")
        print(f"  3. Confirm aimiai.com API is accessible")
        return False

    # All tests passed
    print("\n" + "=" * 70)
    print("✓ All tests passed! Ready to find Shannon patterns!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run: python find_shannon_pattern.py")
    print("  2. Or: python find_shannon_pattern.py --min-score 70")
    print("  3. Read: SHANNON_PATTERN_GUIDE.md for details")
    print("=" * 70)

    return True


if __name__ == '__main__':
    success = test_shannon_setup()
    sys.exit(0 if success else 1)
