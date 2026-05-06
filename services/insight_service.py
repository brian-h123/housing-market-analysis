from pathlib import Path
import json
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
def load_insights():
    with open(ARTIFACT_DIR / 'insights.json', 'r') as f:
        payload = json.load(f)
    return payload

class InsightService:
    def __init__(self):
        self.insights = load_insights()

    def get_district_insights(self):
        return self.insights.get('district_insights', {})

    def get_transaction_insights(self):
        return self.insights.get('transaction_insights', {})