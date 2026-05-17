import pandas as pd

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Calculates Bollinger Bands for identifying overbought/oversold conditions."""
    sma = data['close'].rolling(window=window).mean()
    std = data['close'].rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return sma, upper_band, lower_band