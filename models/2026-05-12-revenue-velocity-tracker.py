"""
Revenue Velocity Tracker
Author: Irem Victor Chinonso | Statistical Business Architect
Date: 2026-05-12
Repo: Sovereign-Logic-Engine

Measures the speed at which revenue is growing or decelerating
across multiple income streams. Velocity = change in revenue per unit time.
Flags streams that are accelerating vs. stalling.
"""

import pandas as pd
import numpy as np


INCOME_STREAMS = [
    "Salary",
    "Crypto",
    "YouTube",
    "Freelance",
    "Airdrop"
]


def generate_monthly_revenue(streams, months=6):
    """Simulate 6 months of income stream data."""
    np.random.seed(7)
    records = []
    base_values = {
        "Salary": 45000,
        "Crypto": 12000,
        "YouTube": 3000,
        "Freelance": 8000,
        "Airdrop": 5000
    }
    for month in range(1, months + 1):
        for stream in streams:
            base = base_values[stream]
            noise = np.random.normal(0, base * 0.1)
            trend = base * 0.05 * month if stream in ["YouTube", "Freelance"] else 0
            value = max(0, round(base + noise + trend, 2))
            records.append({
                "month": month,
                "stream": stream,
                "revenue_ngn": value
            })
    return pd.DataFrame(records)


def compute_velocity(df):
    """Compute month-over-month velocity per stream."""
    df = df.sort_values(["stream", "month"])
    df["prev_revenue"] = df.groupby("stream")["revenue_ngn"].shift(1)
    df["velocity"] = df["revenue_ngn"] - df["prev_revenue"]
    df["velocity_pct"] = ((df["velocity"] / df["prev_revenue"]) * 100).round(2)
    return df.dropna(subset=["velocity"])


def compute_acceleration(velocity_df):
    """Compute acceleration (change in velocity over time)."""
    v = velocity_df.sort_values(["stream", "month"])
    v["prev_velocity"] = v.groupby("stream")["velocity"].shift(1)
    v["acceleration"] = v["velocity"] - v["prev_velocity"]
    return v.dropna(subset=["acceleration"])


def classify_stream(df):
    """Classify each stream as ACCELERATING, STABLE, or STALLING."""
    summary = df.groupby("stream").agg(
        avg_velocity=("velocity", "mean"),
        avg_acceleration=("acceleration", "mean"),
        total_revenue=("revenue_ngn", "sum")
    ).round(2)

    def status(row):
        if row["avg_acceleration"] > 500:
            return "ACCELERATING"
        elif row["avg_acceleration"] < -500:
            return "STALLING"
        else:
            return "STABLE"

    summary["status"] = summary.apply(status, axis=1)
    return summary


def run_tracker():
    print("=" * 60)
    print("REVENUE VELOCITY TRACKER")
    print("Sovereign Logic Engine | Irem Victor Chinonso")
    print("=" * 60)

    df = generate_monthly_revenue(INCOME_STREAMS, months=6)

    velocity_df = compute_velocity(df)
    accel_df = compute_acceleration(velocity_df)

    print("\n--- MONTH-OVER-MONTH VELOCITY (NGN) ---")
    pivot = velocity_df.pivot(index="stream", columns="month", values="velocity_pct")
    print(pivot.to_string())

    summary = classify_stream(accel_df)
    print("\n--- STREAM CLASSIFICATION ---")
    print(summary.to_string())

    print("\n--- STRATEGIC SIGNALS ---")
    for stream, row in summary.iterrows():
        if row["status"] == "ACCELERATING":
            print(f"  {stream}: Double down. Revenue is building momentum.")
        elif row["status"] == "STALLING":
            print(f"  {stream}: Investigate. Velocity is declining — needs attention.")
        else:
            print(f"  {stream}: Holding steady. Monitor for shift.")

    print("\nTracker complete.")


if __name__ == "__main__":
    run_tracker()
