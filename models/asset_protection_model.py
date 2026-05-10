# Stochastic Asset Protection Model (SAP-M)
# Logic: Geometric Brownian Motion (GBM) to hedge against NGN Volatility
# Goal: Minimize the 'Inflation Gap' for the N1.2M Laptop Procurement

import numpy as np
import datetime

def simulate_naira_devaluation(current_rate, mu, sigma, days, iterations=1000):
    # mu: Drift (Expected devaluation rate)
    # sigma: Volatility (Market noise)
    dt = 1/365
    paths = np.zeros((iterations, days))
    paths[:, 0] = current_rate
    
    for t in range(1, days):
        # GBM Formula: S(t) = S(t-1) * exp((mu - 0.5 * sigma**2) * dt + sigma * sqrt(dt) * Z)
        z = np.random.standard_normal(iterations)
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    return paths

def analyze_risk(paths, target_usd_price=800):
    # Calculate the required Naira at the end of the period
    final_rates = paths[:, -1]
    required_naira = final_rates * target_usd_price
    
    expected_cost = np.mean(required_naira)
    risk_95 = np.percentile(required_naira, 95) # Value at Risk (VaR)
    
    return {
        "expected_naira_cost": round(expected_cost, 2),
        "worst_case_95": round(risk_95, 2),
        "volatility_impact": round(risk_95 - expected_cost, 2)
    }

if __name__ == "__main__":
    print("--- SAP-M: NGN/USD Volatility Analysis ---")
    # Current Stats: Rate ~1450 NGN/USD, Drift ~20% annual, Volatility ~35%
    sim_paths = simulate_naira_devaluation(current_rate=1450, mu=0.20, sigma=0.35, days=30)
    results = analyze_risk(sim_paths)
    
    print(f"Expected Laptop Cost (30 days): N{results['expected_naira_cost']:,}")
    print(f"Risk-Adjusted Cost (P95): N{results['worst_case_95']:,}")
    print(f"Inflation Hedge Requirement: N{results['volatility_impact']:,}")
