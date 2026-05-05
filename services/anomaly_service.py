from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / 'ml' /'models' / 'artifacts'

# ---------------------
# Loaders
# ---------------------
@st.cache_data
def load_anomalies():
    return pd.read_csv(ARTIFACT_DIR / 'anomalies_data.csv')

@st.cache_data
def load_top_overpriced():
    return pd.read_csv(ARTIFACT_DIR / 'top_overpriced.csv')

@st.cache_data
def load_top_undervalued():
    return pd.read_csv(ARTIFACT_DIR / 'top_undervalued.csv')

class AnomalyExplorer:
    def __init__(self):
        self.anomalies = load_anomalies()

    def filter(self, input_dict: dict) -> pd.DataFrame:
        df = self.anomalies.copy()

        filtered = df[df['district'].isin(input_dict['districts'])]
        filtered = filtered[filtered['residual_z'].abs() >= input_dict['z_threshold']]

        anomaly_type = input_dict.get('anomaly_type', 'All')
        if anomaly_type == 'Overpriced':
            filtered = filtered[filtered['residual'] > 0]
        elif anomaly_type == 'Undervalued':
            filtered = filtered[filtered['residual'] < 0]

        return filtered