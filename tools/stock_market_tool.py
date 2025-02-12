import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockMarketTool:
    """
    Tool to fetch real-time and historical stock market data.
    """

    @staticmethod
    def get_stock_price(ticker):
        """
        Fetches real-time stock price.
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if data.empty:
                return {"error": f"No data found for {ticker}"}

            return {
                "ticker": ticker,
                "latest_price": round(data["Close"].iloc[-1], 2),
                "high": round(data["High"].iloc[-1], 2),
                "low": round(data["Low"].iloc[-1], 2),
                "volume": int(data["Volume"].iloc[-1]),
                "timestamp": str(datetime.now())
            }

        except Exception as e:
            return {"error": f"Stock price retrieval failed: {str(e)}"}

    @staticmethod
    def get_historical_stock(ticker, days=30):
        """
        Fetches historical stock data for trend analysis.
        """
        try:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            if data.empty:
                return {"error": f"No historical data found for {ticker}"}

            return data[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records")

        except Exception as e:
            return {"error": f"Historical stock data retrieval failed: {str(e)}"}
