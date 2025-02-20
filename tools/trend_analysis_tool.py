import numpy as np
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Any, Dict, List
from tools.stock_market_tool import HistoricalStockMarketTool

class TrendAnalysisInput(BaseModel):
    ticker: str = Field(description="Stock ticker symbol (e.g., AAPL for Apple).")
    days: int = Field(default=90, description="Number of past days for trend analysis.")
    indicators: List[str] = Field(default=["SMA", "EMA", "RSI", "MACD"], description="List of indicators to compute.")

class TrendAnalysisTool(BaseTool):
    name: str = "trend_analysis"
    description: str = "Analyzes financial trends using SMA, EMA, RSI, and MACD."
    
    def _fetch_stock_data(self, ticker: str, days: int) -> List[Dict[str, Any]]:
        """Fetch historical stock data using HistoricalStockMarketTool."""
        result = HistoricalStockMarketTool()._run(ticker, days)  # Fetch data
        return result.get("historical_data", [])  # Return list of historical data
    
    def _calculate_sma(self, data: List[Dict[str, Any]], period: int = 20) -> List[float]:
        """Computes Simple Moving Average (SMA)."""
        close_prices = [entry["close"] for entry in data]
        sma_values = np.convolve(close_prices, np.ones(period)/period, mode='valid')
        return sma_values.tolist()
    
    def _calculate_ema(self, data: List[Dict[str, Any]], period: int = 20) -> List[float]:
        """Computes Exponential Moving Average (EMA)."""
        close_prices = np.array([entry["close"] for entry in data])
        ema_values = np.zeros_like(close_prices)
        multiplier = 2 / (period + 1)
        ema_values[0] = close_prices[0]  # First value is same as the close price
        for i in range(1, len(close_prices)):
            ema_values[i] = (close_prices[i] - ema_values[i - 1]) * multiplier + ema_values[i - 1]
        return ema_values.tolist()
    
    def _calculate_rsi(self, data: List[Dict[str, Any]], period: int = 14) -> List[float]:
        """Computes Relative Strength Index (RSI)."""
        close_prices = np.array([entry["close"] for entry in data])
        delta = np.diff(close_prices)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = np.convolve(gain, np.ones(period)/period, mode='valid')
        avg_loss = np.convolve(loss, np.ones(period)/period, mode='valid')
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.tolist()
    
    def _calculate_macd(self, data: List[Dict[str, Any]], short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> Dict[str, List[float]]:
        """Computes Moving Average Convergence Divergence (MACD)."""
        close_prices = np.array([entry["close"] for entry in data])
        short_ema = self._calculate_ema(data, period=short_period)
        long_ema = self._calculate_ema(data, period=long_period)
        macd_line = np.array(short_ema) - np.array(long_ema)
        signal_line = np.convolve(macd_line, np.ones(signal_period)/signal_period, mode='valid')
        return {"macd_line": macd_line.tolist(), "signal_line": signal_line.tolist()}
    
    def _run(self, ticker: str, days: int = 90, indicators: List[str] = ["SMA", "EMA", "RSI", "MACD"]) -> Dict[str, Any]:
        """Synchronous method to analyze stock trends."""
        data = self._fetch_stock_data(ticker, days)
        result = {"ticker": ticker}
        
        if "SMA" in indicators:
            result["SMA_20"] = self._calculate_sma(data, period=20)
        if "EMA" in indicators:
            result["EMA_20"] = self._calculate_ema(data, period=20)
        if "RSI" in indicators:
            result["RSI_14"] = self._calculate_rsi(data, period=14)
        if "MACD" in indicators:
            result["MACD"] = self._calculate_macd(data)
        
        return result
    
    async def _arun(self, ticker: str, days: int = 90, indicators: List[str] = ["SMA", "EMA", "RSI", "MACD"]) -> Dict[str, Any]:
        """Asynchronous method to analyze stock trends."""
        return self._run(ticker, days, indicators)
