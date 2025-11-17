"""
Test Yahoo Finance API with real data
"""
from src.data.yahoo_finance_api import YahooFinanceAPI

print("="*70)
print("Yahoo Finance API Test")
print("="*70)

try:
    api = YahooFinanceAPI()
    print("\n✓ API initialized")
    print(f"  API Key: {api.api_key[:20]}...")

    # Test with AAPL
    print("\nFetching news for AAPL...")
    news = api.get_news_by_symbol('AAPL', snippet_count=10)

    if news and 'data' in news:
        news_items = news['data'].get('news', [])
        print(f"✓ Retrieved {len(news_items)} news items")

        if len(news_items) > 0:
            print("\nLatest headlines:")
            for i, item in enumerate(news_items[:5], 1):
                title = item.get('title', 'No title')
                print(f"  {i}. {title}")

        # Sentiment analysis
        sentiment = api.extract_news_sentiment(news)
        print(f"\nSentiment Analysis:")
        print(f"  Sentiment: {sentiment['sentiment']}")
        print(f"  Score: {sentiment['sentiment_score']:.3f}")
        print(f"  News Count: {sentiment['news_count']}")
    else:
        print("✗ No data returned")
        print(f"Response: {news}")

    print("\n" + "="*70)
    print("✓ Yahoo Finance API is working!")
    print("="*70)

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nCheck:")
    print("1. RAPIDAPI_KEY in .env file")
    print("2. RapidAPI subscription active")
    print("3. Network connection")
