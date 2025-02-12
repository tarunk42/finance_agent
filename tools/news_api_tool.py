import requests
from datetime import datetime, timedelta

class NewsAPITool:
    """
    Tool to fetch financial news from NewsAPI.org.
    """

    BASE_URL = "https://newsapi.org/v2/everything"
    API_KEY = "5ae6adf1cd5b49a48d64dd51fbec18c5"

    @staticmethod
    def fetch_news(query="stocks", language="en", from_date=None, sort_by="publishedAt", max_results=5):
        """
        Fetch financial news related to a given query.
        :param query: Keywords to search for (e.g., "Tesla", "Bitcoin").
        :param language: Language of the articles.
        :param from_date: Date filter (defaults to yesterday for free tier).
        :param sort_by: Sorting method ("relevancy", "popularity", "publishedAt").
        :param max_results: Number of articles to return.
        :return: List of news articles.
        """
        if from_date is None:
            from_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")  # Default: Yesterday's news

        params = {
            "q": query,
            "language": language,
            "from": from_date,
            "sortBy": sort_by,
            "apiKey": NewsAPITool.API_KEY
        }

        try:
            response = requests.get(NewsAPITool.BASE_URL, params=params)
            data = response.json()

            if data.get("status") != "ok":
                return {"error": f"News API error: {data.get('message', 'Unknown error')}"}

            articles = data.get("articles", [])[:max_results]
            return [
                {
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "published_at": article["publishedAt"],
                    "url": article["url"]
                } for article in articles
            ]

        except Exception as e:
            return {"error": f"Failed to retrieve news: {str(e)}"}

    @staticmethod
    def fetch_stock_news(ticker, max_results=5):
        """
        Fetch stock-related news by searching the stock symbol.
        :param ticker: Stock ticker (e.g., "AAPL", "TSLA").
        :param max_results: Number of articles to return.
        :return: List of news articles.
        """
        return NewsAPITool.fetch_news(query=ticker, max_results=max_results)

    @staticmethod
    def fetch_crypto_news(crypto_name, max_results=5):
        """
        Fetch cryptocurrency-related news.
        :param crypto_name: Cryptocurrency name (e.g., "Bitcoin", "Ethereum").
        :param max_results: Number of articles to return.
        :return: List of news articles.
        """
        return NewsAPITool.fetch_news(query=crypto_name, max_results=max_results)
