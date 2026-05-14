import numpy as np

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculates Bollinger Bands for a price series."""
    sma = np.convolve(prices, np.ones(window)/window, mode='valid')
    rstd = np.array([np.std(prices[i:i+window]) for i in range(len(prices)-window+1)])
    upper_band = sma + (rstd * num_std)
    lower_band = sma - (rstd * num_std)
    return upper_band, sma, lower_band