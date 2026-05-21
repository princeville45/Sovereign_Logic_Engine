import pandas as pd

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Calculates Bollinger Bands (upper, middle, lower)."""
    middle_band = data['close'].rolling(window=window).mean()
    std_dev = data['close'].rolling(window=window).std()
    upper_band = middle_band + (std_dev * num_std)
    lower_band = middle_band - (std_dev * num_std)
    return upper_band, middle_band, lower_band