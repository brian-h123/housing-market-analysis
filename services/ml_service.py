from pathlib import Path
import joblib
import json
import pandas as pd
import numpy as np
import streamlit as st

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / 'ml' /'models' / 'artifacts'
MODEL_PATH = ARTIFACT_DIR / 'ridge_model.pkl'
FEATURE_PATH = ARTIFACT_DIR / 'feature_columns.json'

# -----------------------------
# Model Loader (cached)
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load(str(MODEL_PATH))

@st.cache_data
def load_feature_columns():
    with open(FEATURE_PATH) as f:
        return json.load(f)

# -----------------------------
# Feature Builder
# -----------------------------
class FeatureBuilder:
    def __init__(self, feature_columns: list):
        self.feature_columns = feature_columns

        self.district_features = [f for f in feature_columns if f.startswith('district_')]
        self.type_features = [f for f in feature_columns if f.startswith('building_type_')]

    def build(self, input_dict: dict) -> pd.DataFrame:
        df = pd.DataFrame([input_dict])

        df = self._engineer_features(df)
        df = self._encode_categorical(df)
        df = self._align(df)

        return df
    
    DEFAULT_AREA_RATIO = 0.8
    DEFAULT_TIME_INDEX = 1

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['area'] = pd.to_numeric(df['area'], errors='coerce').fillna(0)

        df['building_age'] = pd.to_numeric(df.get('building_age', 0), errors='coerce').fillna(0)

        df['parking_area'] = 0
        df['has_parking'] = 0

        df['log_area'] = np.log(df['area'])

        df['area_ratio'] = self.DEFAULT_AREA_RATIO

        df['time_index'] = self.DEFAULT_TIME_INDEX

        return df
    
    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        district = df.get('district', [''])[0]
        for col in self.district_features:
            df[col] = 1 if col == f"district_{district}" else 0

        btype = df.get('building_type', [''])[0]
        for col in self.type_features:
            df[col] = 1 if col == f"building_type_{btype}" else 0

        return df
    
    def _align(self, df: pd.DataFrame) -> pd.DataFrame:
        # Align to model feature space
        df = df.reindex(columns=self.feature_columns, fill_value=0)

        return df
    
# -----------------------------
# Prediction Service
# -----------------------------
class PredictionService:
    def __init__(self):
        self.model = load_model()
        self.feature_columns = load_feature_columns()
        self.builder = FeatureBuilder(self.feature_columns)

    def predict(self, input_dict: dict) -> dict:
        # Main API
        X = self.builder.build(input_dict)

        prediction = self.model.predict(X)[0]

        return {
            'predicted_price_per_sqm': float(prediction)
        }
    
    def predict_with_context(self, input_dict: dict, district_avg: float=None) -> dict:
        # Extend output with interpretation
        result = self.predict(input_dict)

        pred = result['predicted_price_per_sqm']

        if district_avg is not None:
            diff = pred - district_avg
            pct_diff = diff / district_avg if district_avg != 0 else 0

            result.update({
                'district_avg': district_avg,
                'difference': diff,
                'pct_difference': pct_diff,
                'label': self._interpret(pct_diff)
            })

        return result
    
    def _interpret(self, pct_diff: float) -> str:
        if pct_diff > 0.1:
            return 'Above Market'
        elif pct_diff < -0.1:
            return 'Below Market'
        else:
            return 'Fair Value'