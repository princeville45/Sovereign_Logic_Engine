import requests
import time
import json

# Configuration
SYMBOL = "SOLUSDT"
INTERVAL = "1d"
RSI_PERIOD = 14
TAKE_PROFIT = 160.0
STOP_LOSS = 140.0

def get_klines(symbol, interval, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    return response.json()

def calculate_rsi(data, period=14):
    closes = [float(candle[4]) for candle in data]
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def monitor_price():
    print(f"--- Starting SOL Price Monitor for {SYMBOL} ---")
    data = get_klines(SYMBOL, INTERVAL)
    current_price = float(data[-1][4])
    rsi = calculate_rsi(data, RSI_PERIOD)
    
    print(f"Current Price: ${current_price}")
    print(f"Current RSI(14): {rsi:.2f}")
    
    if current_price >= TAKE_PROFIT:
        verdict = "SELL - Take Profit Reached"
    elif current_price <= STOP_LOSS:
        verdict = "SELL - Stop Loss Reached"
    elif rsi > 70:
        verdict = "CAUTION - Overbought (RSI > 70)"
    elif rsi < 30:
        verdict = "BUY SIGNAL - Oversold (RSI < 30)"
    else:
        verdict = "HOLD - No Signal"
        
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    monitor_price()
