import pandas as pd
import numpy as np

class TrendAnalysisTool:
    """
    Tool to analyze financial trends using SMA, EMA, RSI, and MACD.
    """

    @staticmethod
    def calculate_sma(df, period=20):
        """
        Computes Simple Moving Average (SMA).
        :param df: DataFrame with 'Close' prices.
        :param period: Lookback period for SMA.
        :return: SMA values.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")
        return df["Close"].rolling(window=period).mean()

    @staticmethod
    def calculate_ema(df, period=20):
        """
        Computes Exponential Moving Average (EMA).
        :param df: DataFrame with 'Close' prices.
        :param period: Lookback period for EMA.
        :return: EMA values.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")
        return df["Close"].ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_rsi(df, period=14):
        """
        Computes Relative Strength Index (RSI).
        :param df: DataFrame with 'Close' prices.
        :param period: Lookback period for RSI.
        :return: RSI values.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")
            
        delta = df["Close"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=period).mean()
        avg_loss = pd.Series(loss).rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return pd.Series(rsi, index=df.index)

    @staticmethod
    def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
        """
        Computes Moving Average Convergence Divergence (MACD).
        :param df: DataFrame with 'Close' prices.
        :param short_period: Fast EMA period.
        :param long_period: Slow EMA period.
        :param signal_period: Signal line period.
        :return: MACD line and Signal line.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        short_ema = df["Close"].ewm(span=short_period, adjust=False).mean()
        long_ema = df["Close"].ewm(span=long_period, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        return macd_line, signal_line
