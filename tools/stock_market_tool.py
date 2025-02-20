import aiohttp
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Any, Dict
import requests
import json
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys

# Get the absolute path of the finance_agents directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import config

class StockPriceInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")

class HistoricalStockInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")
    days: int = Field(default=30, description="Number of past days for historical data.")

class StockMarketTool(BaseTool):
    name: str = "stock_market"
    description: str = "Fetches real-time and historical stock market data."
    api_key: str = config.FMP_API_KEY
    
    def _fetch_yahoo_finance_price(self, ticker: str) -> Dict[str, Any]:
        """Fetch stock price using Yahoo Finance."""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                return {
                    "ticker": ticker,
                    "latest_price": round(data["Close"].iloc[-1], 2),
                    "high": round(data["High"].iloc[-1], 2),
                    "low": round(data["Low"].iloc[-1], 2),
                    "volume": int(data["Volume"].iloc[-1]),
                    "timestamp": str(datetime.now()),
                }
        except Exception as e:
            return {}
    
    def _fetch_fmp_price(self, ticker: str) -> Dict[str, Any]:
        """Fetch stock price using Financial Modeling Prep API."""
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={self.api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        "ticker": ticker,
                        "latest_price": round(data[0]['price'], 2),
                        "high": round(data[0]['dayHigh'], 2),
                        "low": round(data[0]['dayLow'], 2),
                        "volume": int(data[0]['volume']),
                        "timestamp": str(datetime.now()),
                    }
        except Exception as e:
            return {}
    
    def _run(self, ticker: str) -> Dict[str, Any]:
        """Synchronous method to fetch stock price."""
        result = self._fetch_yahoo_finance_price(ticker)
        return result if result else self._fetch_fmp_price(ticker)
    
    async def _arun(self, ticker: str) -> Dict[str, Any]:
        """Asynchronous method to fetch stock price."""
        result = self._fetch_yahoo_finance_price(ticker)
        return result if result else self._fetch_fmp_price(ticker)

class HistoricalStockMarketTool(BaseTool):
    name: str = "historical_stock_market"
    description: str = "Fetches historical stock market data."
    api_key: str = config.FMP_API_KEY
    
    def _fetch_yahoo_finance_historical(self, ticker: str, days: int) -> Dict[str, Any]:
        """Fetch historical stock data using Yahoo Finance."""
        try:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            if not data.empty:
                return {
                    "ticker": ticker,
                    "historical_data": data[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records"),
                }
        except Exception as e:
            return {}
    
    def _fetch_fmp_historical(self, ticker: str, days: int) -> Dict[str, Any]:
        """Fetch historical stock data using Financial Modeling Prep API."""
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?timeseries={days}&apikey={self.api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "historical" in data:
                    return {
                        "ticker": ticker,
                        "historical_data": [
                            {
                                "date": record["date"],
                                "open": record["open"],
                                "high": record["high"],
                                "low": record["low"],
                                "close": record["close"],
                                "volume": record["volume"]
                            } for record in data["historical"]
                        ],
                    }
        except Exception as e:
            return {}
    
    def _run(self, ticker: str, days: int = 30) -> Dict[str, Any]:
        """Synchronous method to fetch historical stock data."""
        result = self._fetch_yahoo_finance_historical(ticker, days)
        return result if result else self._fetch_fmp_historical(ticker, days)
    
    async def _arun(self, ticker: str, days: int = 30) -> Dict[str, Any]:
        """Asynchronous method to fetch historical stock data."""
        result = self._fetch_yahoo_finance_historical(ticker, days)
        return result if result else self._fetch_fmp_historical(ticker, days)




# stock_tool = StockMarketTool()
# historical_stock_tool = HistoricalStockMarketTool()


# ticker = "AAPL"
# print("Fetching real-time stock price for:", ticker)
# stock_price_result = stock_tool._run(ticker)
# print(stock_price_result)