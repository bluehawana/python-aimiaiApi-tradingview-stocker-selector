"""
Enhanced stock analysis with Yahoo Finance news sentiment
Combines technical analysis with news sentiment for better insights
"""
import yaml
from typing import List, Dict
from src.data.yahoo_finance_api import YahooFinanceAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def load_config(config_file: str = 'config.yaml') -> Dict:
    """Load configuration from YAML file"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def analyze_stocks_with_news(symbols: List[str], config_file: str = 'config.yaml'):
    """
    Analyze stocks with news sentiment integration

    Args:
        symbols: List of stock symbols to analyze
        config_file: Path to configuration file
    """
    print("=" * 70)
    print("AI Stock Analyzer with News Sentiment")
    print("=" * 70)

    try:
        # Initialize Yahoo Finance API
        print("\n[1/3] Initializing Yahoo Finance API...")
        yf_api = YahooFinanceAPI()
        print("✓ Yahoo Finance API ready")

        # Fetch news for all symbols
        print(f"\n[2/3] Fetching news for {len(symbols)} symbols...")
        news_data = yf_api.get_news_by_symbols(symbols, snippet_count=100)
        print("✓ News data retrieved")

        # Analyze sentiment
        print("\n[3/3] Analyzing news sentiment...")
        sentiment = yf_api.extract_news_sentiment(news_data)

        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"\nSymbols Analyzed: {', '.join(symbols)}")
        print(f"\nNews Sentiment: {sentiment['sentiment'].upper()}")
        print(f"Sentiment Score: {sentiment['sentiment_score']:.3f}")
        print(f"News Articles: {sentiment['news_count']}")
        print(f"Raw Score: {sentiment['raw_score']}")

        # Display recent news headlines
        if news_data and 'data' in news_data:
            news_items = news_data.get('data', {}).get('news', [])[:5]
            if news_items:
                print("\n" + "-" * 70)
                print("Recent Headlines:")
                print("-" * 70)
                for i, item in enumerate(news_items, 1):
                    title = item.get('title', 'No title')
                    print(f"{i}. {title}")

        print("\n" + "=" * 70)
        print("✓ Analysis complete!")
        print("=" * 70)

        return sentiment

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your RAPIDAPI_KEY in .env file")
        print("2. Verify you have an active RapidAPI subscription")
        print("3. Ensure the symbols are valid US stock tickers")
        return None


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Analyze stocks with news sentiment')
    parser.add_argument('--symbols', '-s', nargs='+',
                        default=['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'NVDA'],
                        help='Stock symbols to analyze (default: AAPL GOOGL TSLA MSFT NVDA)')
    parser.add_argument('--config', '-c', default='config.yaml',
                        help='Configuration file (default: config.yaml)')

    args = parser.parse_args()

    analyze_stocks_with_news(args.symbols, args.config)


if __name__ == '__main__':
    main()
