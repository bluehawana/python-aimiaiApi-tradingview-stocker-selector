"""
Test Yahoo Finance API integration
"""
from src.data.yahoo_finance_api import YahooFinanceAPI, test_yahoo_finance_api

if __name__ == '__main__':
    print("=" * 60)
    print("Yahoo Finance API Test")
    print("=" * 60)

    success = test_yahoo_finance_api()

    if success:
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ Tests failed - check your RAPIDAPI_KEY in .env")
        print("=" * 60)
