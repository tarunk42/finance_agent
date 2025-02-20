import requests
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Any, Dict, List
from datetime import datetime, timedelta
import config

class NewsAPIInput(BaseModel):
    query: str = Field(default="stocks", description="Keywords to search for (e.g., Tesla, Bitcoin).")
    language: str = Field(default="en", description="Language of the articles.")
    from_date: str = Field(default=None, description="Date filter (defaults to yesterday for free tier).")
    sort_by: str = Field(default="publishedAt", description="Sorting method (relevancy, popularity, publishedAt).")
    max_results: int = Field(default=5, description="Number of articles to return.")

class NewsAPITool(BaseTool):
    name: str = "news_api"
    description: str = "Fetches financial news from NewsAPI.org."
    api_key: str = config.NEWS_API_KEY
    
    BASE_URL: str = "https://newsapi.org/v2/everything"
    
    def _fetch_news(self, query: str, language: str, from_date: str, sort_by: str, max_results: int) -> List[Dict[str, Any]]:
        """Fetch financial news related to a given query."""
        if from_date is None:
            from_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

        params = {
            "q": query,
            "language": language,
            "from": from_date,
            "sortBy": sort_by,
            "apiKey": self.api_key
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()

            if data.get("status") != "ok":
                return [{"error": f"News API error: {data.get('message', 'Unknown error')}"}]

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
            return [{"error": f"Failed to retrieve news: {str(e)}"}]
    
    def _run(self, query: str = "stocks", language: str = "en", from_date: str = None, sort_by: str = "publishedAt", max_results: int = 5) -> List[Dict[str, Any]]:
        """Synchronous method to fetch news."""
        return self._fetch_news(query, language, from_date, sort_by, max_results)
    
    async def _arun(self, query: str = "stocks", language: str = "en", from_date: str = None, sort_by: str = "publishedAt", max_results: int = 5) -> List[Dict[str, Any]]:
        """Asynchronous method to fetch news."""
        return self._fetch_news(query, language, from_date, sort_by, max_results)

class StockNewsTool(BaseTool):
    name: str = "stock_news"
    description: str = "Fetches stock-related news from NewsAPI.org."
    api_key: str = config.NEWS_API_KEY
    
    def _run(self, ticker: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Fetch stock-related news by searching the stock symbol."""
        news_tool = NewsAPITool(api_key=self.api_key)
        return news_tool._fetch_news(query=ticker, language="en", from_date=None, sort_by="publishedAt", max_results=max_results)

class CryptoNewsTool(BaseTool):
    name: str = "crypto_news"
    description: str = "Fetches cryptocurrency-related news from NewsAPI.org."
    api_key: str = config.NEWS_API_KEY
    
    def _run(self, crypto_name: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Fetch cryptocurrency-related news."""
        news_tool = NewsAPITool(api_key=self.api_key)
        return news_tool._fetch_news(query=crypto_name, language="en", from_date=None, sort_by="publishedAt", max_results=max_results)
