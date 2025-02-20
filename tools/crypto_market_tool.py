import ccxt
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Any, Dict, List
from datetime import datetime, timedelta

class CryptoPriceInput(BaseModel):
    symbol: str = Field(default="BTC/USDT", description="Cryptocurrency symbol in exchange format (e.g., BTC/USDT).")

class HistoricalCryptoInput(BaseModel):
    symbol: str = Field(default="BTC/USDT", description="Cryptocurrency symbol in exchange format (e.g., BTC/USDT).")
    days: int = Field(default=30, description="Number of past days for historical data.")

class CryptoMarketTool(BaseTool):
    name: str = "crypto_market"
    description: str = "Fetches real-time cryptocurrency market data."
    exchange_name: str = "binance"
    
    def __init__(self, exchange_name: str = "binance", **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "exchange", self.initialize_exchange(exchange_name))
    
    def initialize_exchange(self, exchange_name):
        """Initialize the crypto exchange."""
        try:
            return getattr(ccxt, exchange_name)()
        except AttributeError:
            raise ValueError(f"Exchange '{exchange_name}' not supported by CCXT.")

    def _fetch_crypto_price(self, symbol: str) -> Dict[str, Any]:
        """Fetches real-time cryptocurrency price."""
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
    
    def _run(self, symbol: str = "BTC/USDT") -> Dict[str, Any]:
        """Synchronous method to fetch crypto price."""
        return self._fetch_crypto_price(symbol)
    
    async def _arun(self, symbol: str = "BTC/USDT") -> Dict[str, Any]:
        """Asynchronous method to fetch crypto price."""
        return self._fetch_crypto_price(symbol)

class HistoricalCryptoMarketTool(BaseTool):
    name: str = "historical_crypto_market"
    description: str = "Fetches historical cryptocurrency market data."
    exchange_name: str = "binance"
    
    def __init__(self, exchange_name: str = "binance", **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "exchange", self.initialize_exchange(exchange_name))
    
    def initialize_exchange(self, exchange_name):
        """Initialize the crypto exchange."""
        try:
            return getattr(ccxt, exchange_name)()
        except AttributeError:
            raise ValueError(f"Exchange '{exchange_name}' not supported by CCXT.")
    
    def _fetch_historical_crypto(self, symbol: str, days: int) -> List[Dict[str, Any]]:
        """Fetches historical cryptocurrency data."""
        try:
            since = self.exchange.parse8601((datetime.utcnow() - timedelta(days=days)).isoformat())
            candles = self.exchange.fetch_ohlcv(symbol, timeframe="1d", since=since, limit=days)

            if not candles:
                return [{"error": f"No historical data found for {symbol}"}]

            return [
                {
                    "timestamp": datetime.utcfromtimestamp(c[0] / 1000).strftime('%Y-%m-%d'),
                    "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[5]
                } for c in candles
            ]
        except Exception as e:
            return [{"error": f"Historical crypto data retrieval failed: {str(e)}"}]
    
    def _run(self, symbol: str = "BTC/USDT", days: int = 30) -> List[Dict[str, Any]]:
        """Synchronous method to fetch historical crypto data."""
        return self._fetch_historical_crypto(symbol, days)
    
    async def _arun(self, symbol: str = "BTC/USDT", days: int = 30) -> List[Dict[str, Any]]:
        """Asynchronous method to fetch historical crypto data."""
        return self._fetch_historical_crypto(symbol, days)



# # **Test the Fix**
# if __name__ == "__main__":
#     crypto_tool = CryptoMarketTool()

#     # Test real-time crypto retrieval
#     crypto_data = crypto_tool._run("BTC/USDT")
#     print("Live Crypto Data:", crypto_data)

#     # Test historical crypto retrieval
#     historical_crypto_tool = HistoricalCryptoMarketTool()
#     historical_crypto_data = historical_crypto_tool._run("BTC/USDT", 30)




