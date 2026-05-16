import numpy as np

def calculate_atr(high, low, close, window=14):
    """Calculates the Average True Range (ATR) to measure market volatility."""
    tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
    atr = tr.rolling(window=window).mean()
    return atr