import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta

fmp_api_key = "kU2hUzzdfrgjUILx7siQiCCdGGXAWOvc"


import yfinance as yf
import requests
from datetime import datetime, timedelta

# Financial Modeling Prep API Key
FMP_API_KEY = fmp_api_key

class StockMarketTool:
    """
    Tool to fetch real-time and historical stock market data with fallback.
    """
    
    @staticmethod
    def get_stock_price(ticker):
        """
        Fetches real-time stock price, first attempting Yahoo Finance, then Financial Modeling Prep API as fallback.
        """
        try:
            # Attempt to fetch data from Yahoo Finance
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
                    # "provider": "Yahoo Finance"
                }
        except Exception as e:
            error_msg = str(e).lower()
            # if "too many requests" in error_msg or "rate limit" in error_msg:
            #     print("Yahoo Finance API rate limit hit. Switching to fallback API...")
            # else:
            #     print(f"Yahoo Finance retrieval failed: {str(e)}")
        
        # Ensure fallback execution if Yahoo Finance fails
        # print("Falling back to Financial Modeling Prep API...")
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
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
                        # "provider": "Financial Modeling Prep"
                    }
        except Exception as e:
            # print(f"FMP API retrieval failed: {str(e)}")
            return {}

        
        # return {"error": f"No stock data available for {ticker} from any source."}

    @staticmethod
    def get_historical_stock(ticker, days=30):
        """
        Fetches historical stock data for trend analysis, attempting Yahoo Finance first and FMP as fallback.
        """
        try:
            end_date = datetime.today().strftime("%Y-%m-%d")
            start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            if not data.empty:
                return {
                    "ticker": ticker,
                    "historical_data": data[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records"),
                    "provider": "Yahoo Finance"
                }
        except Exception as e:
            error_msg = str(e).lower()
            # if "too many requests" in error_msg or "rate limit" in error_msg:
            #     print("Yahoo Finance API rate limit hit. Switching to fallback API...")
            # else:
            #     print(f"Yahoo Finance historical retrieval failed: {str(e)}")
        
        # Ensure fallback execution if Yahoo Finance fails
        # print("Falling back to Financial Modeling Prep API for historical data...")
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?timeseries={days}&apikey={FMP_API_KEY}"
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
                        # "provider": "Financial Modeling Prep"
                    }
        except Exception as e:
            return {}
        #     print(f"FMP API historical retrieval failed: {str(e)}")
        
        # return {"error": f"No historical stock data available for {ticker} from any source."}







# class StockMarketTool:
#     """
#     Tool to fetch real-time and historical stock market data.
#     """

#     @staticmethod
#     def get_stock_price(ticker):
#         """
#         Fetches real-time stock price.
#         """
#         try:
#             stock = yf.Ticker(ticker)
#             data = stock.history(period="1d")
#             if data.empty:
#                 return {"error": f"No data found for {ticker}"}

#             return {
#                 "ticker": ticker,
#                 "latest_price": round(data["Close"].iloc[-1], 2),
#                 "high": round(data["High"].iloc[-1], 2),
#                 "low": round(data["Low"].iloc[-1], 2),
#                 "volume": int(data["Volume"].iloc[-1]),
#                 "timestamp": str(datetime.now())
#             }

#         except Exception as e:
#             return {"error": f"Stock price retrieval failed: {str(e)}"}

#     @staticmethod
#     def get_historical_stock(ticker, days=30):
#         """
#         Fetches historical stock data for trend analysis.
#         """
#         try:
#             end_date = datetime.today().strftime("%Y-%m-%d")
#             start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

#             stock = yf.Ticker(ticker)
#             data = stock.history(start=start_date, end=end_date)
#             if data.empty:
#                 return {"error": f"No historical data found for {ticker}"}

#             return data[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records")

#         except Exception as e:
#             return {"error": f"Historical stock data retrieval failed: {str(e)}"}
