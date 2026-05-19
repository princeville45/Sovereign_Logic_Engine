import pandas as pd

def calculate_macd(data, slow=26, fast=12, signal=9):
    """Calculates Moving Average Convergence Divergence (MACD) and signal line."""
    exp1 = data['close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    exp3 = macd.ewm(span=signal, adjust=False).mean()
    return macd, exp3