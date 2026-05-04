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
@st.chace_data
def load_anomalies():
    return pd.read_csv(ARTIFACT_DIR / 'anomalies_data.csv')

def load_top_overpriced():
    return pd.read_csv(ARTIFACT_DIR / 'top_overpriced.csv')

def load_top_undervalued():
    return pd.read_csv(ARTIFACT_DIR / 'top_undervalued.csv')

class AnomalyExplorer:
    def __init__(self):
        self.anomalies = load_anomalies()

    def filter(self, input_dict: dict) -> pd.DataFrame:
        df = self.anomalies.copy()

        filtered = df[df['district'].isin(input_dict['districts'])]
        filtered = filtered[filtered['residual_z'].abs() >= input_dict['z_threshold']]

        if input_dict['anomaly_type'] == 'Overpriced':
            filtered = filtered[filtered['residual'] > 0]
        elif input_dict['anomaly_type'] == 'Undervalued':
            filtered = filtered[filtered['residual'] < 0]

        return filtered