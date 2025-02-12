import ccxt
import pandas as pd
from datetime import datetime, timedelta

class CryptoMarketTool:
    """
    Tool to fetch real-time and historical cryptocurrency market data.
    """

    def __init__(self, exchange_name="binance"):
        """
        Initialize the crypto exchange.
        """
        try:
            self.exchange = getattr(ccxt, exchange_name)()
        except AttributeError:
            raise ValueError(f"Exchange '{exchange_name}' not supported by CCXT.")

    def get_crypto_price(self, symbol="BTC/USDT"):
        """
        Fetches real-time cryptocurrency price.
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                "symbol": symbol,
                "latest_price": round(ticker["last"], 2),
                "high": round(ticker["high"], 2),
                "low": round(ticker["low"], 2),
                "volume": round(ticker["quoteVolume"], 2),
                "timestamp": datetime.utcfromtimestamp(ticker["timestamp"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {"error": f"Crypto price retrieval failed: {str(e)}"}

    def get_historical_crypto(self, symbol="BTC/USDT", days=30):
        """
        Fetches historical cryptocurrency data.
        """
        try:
            since = self.exchange.parse8601((datetime.utcnow() - timedelta(days=days)).isoformat())
            candles = self.exchange.fetch_ohlcv(symbol, timeframe="1d", since=since, limit=days)

            if not candles:
                return {"error": f"No historical data found for {symbol}"}

            return [
                {"timestamp": datetime.utcfromtimestamp(c[0] / 1000).strftime('%Y-%m-%d'),
                 "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[5]}
                for c in candles
            ]

        except Exception as e:
            return {"error": f"Historical crypto data retrieval failed: {str(e)}"}
