import json
import pandas as pd
from pathlib import Path

from insights.generators import (
    generate_district_insight,
    generate_transaction_insight
)

# ---------------------
# Config
# ---------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / 'ml' /'models' / 'artifacts'

# ---------------------
# Data Loading
# ---------------------

def load_anomaly_outputs():
    anomalies = pd.read_csv(ARTIFACT_DIR / 'anomalies_data.csv')
    top_overpriced = pd.read_csv(ARTIFACT_DIR / 'top_overpriced.csv')
    top_undervalued = pd.read_csv(ARTIFACT_DIR / 'top_undervalued.csv')
    district_stats = pd.read_csv(ARTIFACT_DIR / 'district_residuals.csv')

    return anomalies, top_overpriced, top_undervalued, district_stats

# ---------------------
# Interpretability Boost
# ---------------------

def add_derived_metrics(df):
    df = df.copy()

    df['pct_diff'] = (
        (df['actual_price'] - df['predicted_price'])
        / df['predicted_price'] 
    )

    return df

# ---------------------
# Aggregation Layer
# ---------------------

def build_district_insights(district_stats):
    top_overpriced = district_stats.sort_values(
        'mean_residual', ascending=False
    ).head(10)

    top_undervalued = district_stats.sort_values(
        'mean_residual'
    ).head(10)

    most_volatile = district_stats.sort_values(
        'volatility', ascending=False
    ).head(10)

    return {
        'overpriced': [
            generate_district_insight(row)
            for _, row in top_overpriced.iterrows()
        ],
        'undervalues': [
            generate_district_insight(row)
            for _, row in top_undervalued.iterrows()
        ],
        'volatile': [
            generate_district_insight(row)
            for _, row in most_volatile.iterrows()
        ]
    }

def build_transaction_insights(top_overpriced, top_undervalued):
    return {
        'overpriced': [
            generate_transaction_insight(row)
            for _, row in top_overpriced.iterrows()
        ],
        'undervalued': [
            generate_transaction_insight(row)
            for _, row in top_undervalued.iterrows()
        ]
    }

# ---------------------
# Main API for Dashboard Usage
# ---------------------

def build_insight_payload():
    anomalies, top_overpriced, top_undervalued, district_stats = load_anomaly_outputs()

    # Add % deviation metric
    anomalies = add_derived_metrics(anomalies)
    top_overpriced = add_derived_metrics(top_overpriced)
    top_undervalued = add_derived_metrics(top_undervalued)

    payload = {
        'district_insights': build_district_insights(district_stats),
        'transaction_insights': build_transaction_insights(
            top_overpriced, top_undervalued
        )
    }

    return payload

# ---------------------
# Optional Export
# ---------------------

def export_insights_to_json(filepath=None):
    payload = build_insight_payload()

    if filepath is None:
        filepath = ARTIFACT_DIR / 'insights.json'

    with open(filepath, 'w') as f:
        json.dump(payload, f, indent=2)

    print(f"Insights saved to {filepath}")