# Multi-Asset Strategic Analyzer (MASA)
# Logic: Generalized GBM for Forex and Crypto Analysis
import numpy as np

class AssetAnalyzer:
    def __init__(self, name, price, drift, vol):
        self.name = name
        self.price = price
        self.drift = drift # Annualized expected return
        self.vol = vol     # Annualized volatility (Crypto is high, Forex is low)

    def simulate_paths(self, days=30, iterations=1000):
        dt = 1/365
        paths = np.zeros((iterations, days))
        paths[:, 0] = self.price
        for t in range(1, days):
            z = np.random.standard_normal(iterations)
            paths[:, t] = paths[:, t-1] * np.exp((self.drift - 0.5 * self.vol**2) * dt + self.vol * np.sqrt(dt) * z)
        return paths

    def report_confidence_intervals(self, days=30):
        paths = self.simulate_paths(days)
        final_prices = paths[:, -1]
        return {
            "Asset": self.name,
            "Current": self.price,
            "Mean_Projection": np.mean(final_prices),
            "Lower_Bound_95": np.percentile(final_prices, 2.5),
            "Upper_Bound_95": np.percentile(final_prices, 97.5)
        }

if __name__ == "__main__":
    print("--- MASA: Multi-Asset Strategic Analysis ---")
    
    # Forex Example: NGN/USD
    forex = AssetAnalyzer("NGN/USD", 1450, 0.25, 0.30)
    
    # Crypto Example: Bitcoin (High Volatility)
    crypto = AssetAnalyzer("Bitcoin", 65000, 0.50, 0.85)
    
    for asset in [forex, crypto]:
        res = asset.report_confidence_intervals()
        print(f"{res['Asset']} | Current: {res['Current']} | 30d Range: {res['Lower_Bound_95']:.2f} - {res['Upper_Bound_95']:.2f}")
