# Master Sync Logic: Sheets -> Logic Engine
import json
import csv
import os

# This script is a blueprint for the Zapia-managed sync process.
# It aggregates data from Wholesale Ops, Content Pipelines, and Study Logs.

def calculate_mission_score(revenue, scripts, study):
    # Standard weights: Financial (0.4), Equity (0.4), Growth (0.2)
    rev_score = min(revenue / 50000, 1.0) * 4
    script_score = min(scripts / 8, 1.0) * 4
    study_score = min(study / 4, 1.0) * 2
    return round(rev_score + script_score + study_score, 2)

def sync():
    # In a real execution, Zapia pulls this from Google Sheets via CLI
    # Here we simulate the processed result of the sync
    print("Syncing data from Google Workspace...")
    
    # Placeholder for the latest data found in the sync turn
    sync_results = [
        {"date": "2026-05-07", "revenue": 48000, "scripts": 2, "study": 3},
        {"date": "2026-05-08", "revenue": 144000, "scripts": 0, "study": 2},
        {"date": "2026-05-09", "revenue": 33600, "scripts": 1, "study": 4}
    ]
    
    history_file = "data/mission_history.csv"
    file_exists = os.path.isfile(history_file)
    
    with open(history_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "revenue", "scripts", "study", "score"])
        if not file_exists:
            writer.writeheader()
        
        for entry in sync_results:
            entry["score"] = calculate_mission_score(entry["revenue"], entry["scripts"], entry["study"])
            writer.writerow(entry)
            print(f"Logged: {entry['date']} | Score: {entry['score']}")

if __name__ == "__main__":
    sync()
