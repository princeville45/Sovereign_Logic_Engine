# Market Intelligence Engine (MIE)
# Strategic Analysis for Crypto & Forex Trading Decisions
import numpy as np
import datetime

class TradingEngine:
    def __init__(self, asset_name, current_price, annual_drift, annual_vol):
        self.asset_name = asset_name
        self.price = current_price
        self.mu = annual_drift
        self.sigma = annual_vol

    def run_market_simulation(self, days=7, iterations=5000):
        # High-iteration simulation for trading precision
        dt = 1/365
        z = np.random.standard_normal((iterations, days))
        daily_returns = np.exp((self.mu - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * z)
        
        price_paths = np.zeros((iterations, days))
        price_paths[:, 0] = self.price
        for t in range(1, days):
            price_paths[:, t] = price_paths[:, t-1] * daily_returns[:, t]
        
        return price_paths

    def generate_trade_signals(self):
        # Analyze a 7-day window for immediate trading impact
        paths = self.run_market_simulation(days=7)
        final_prices = paths[:, -1]
        
        expected_val = np.mean(final_prices)
        risk_floor = np.percentile(final_prices, 5)   # 95% chance price stays above this
        ceiling_target = np.percentile(final_prices, 95) # 5% chance price hits this
        
        # Calculate Reward-to-Risk Ratio (RRR)
        potential_upside = ceiling_target - self.price
        potential_downside = self.price - risk_floor
        rrr = potential_upside / potential_downside if potential_downside != 0 else 0
        
        return {
            "Asset": self.asset_name,
            "Current_Price": round(self.price, 2),
            "Expected_7d": round(expected_val, 2),
            "Risk_Floor_95": round(risk_floor, 2),
            "Ceiling_Target_95": round(ceiling_target, 2),
            "Reward_to_Risk_Ratio": round(rrr, 2),
            "Sentiment": "BULLISH" if rrr > 1.5 else "CAUTIOUS" if rrr > 0.8 else "BEARISH"
        }

if __name__ == "__main__":
    print("--- MIE: Trading Decision Support Matrix ---")
    
    # 1. BTC/USD Simulation (High Volatility Trading)
    btc_engine = TradingEngine("BTC/USD", 63200, 0.40, 0.70)
    btc_signal = btc_engine.generate_trade_signals()
    
    # 2. NGN/USD Simulation (Forex Volatility/Devaluation)
    ngn_engine = TradingEngine("NGN/USD", 1460, 0.20, 0.25)
    ngn_signal = ngn_engine.generate_trade_signals()
    
    for sig in [btc_signal, ngn_signal]:
        print(f"ASSET: {sig['Asset']}")
        print(f"  > Logic: Entry at {sig['Current_Price']} | 7d Ceiling: {sig['Ceiling_Target_95']}")
        print(f"  > Risk: Stop-Loss Floor: {sig['Risk_Floor_95']}")
        print(f"  > Signal: {sig['Sentiment']} (RRR: {sig['Reward_to_Risk_Ratio']})")
        print("-" * 30)
