import numpy as np
import joblib
import json
from pathlib import Path

from ml.data_prep import prepare_dataset

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / 'models' / 'artifacts'
model_path = ARTIFACT_DIR / 'ridge_model.pkl'
feature_path = ARTIFACT_DIR / 'feature_columns.json'

if not model_path.exists():
    raise FileNotFoundError(f'Model not found at: {model_path}')

with open(feature_path, 'r') as f:
    feature_columns = json.load(f)

model = joblib.load(model_path)

# ---------------------
# Generate Predictions
# ---------------------

df = prepare_dataset()

X = df.drop(columns='final_price_per_sqm')
X = X[feature_columns]
y = df['final_price_per_sqm']

y_pred = model.predict(X)

df = X.copy()
df['actual_price'] = y
df['predicted_price'] = y_pred

# ---------------------
# Reconstruct District column
# ---------------------

district_cols = [col for col in df.columns if col.startswith('district_')]

df['district'] = (df[district_cols].idxmax(axis=1).str.replace('district_',''))

# ---------------------
# Compute Residuals
# ---------------------

df['residual'] = (df['actual_price'] - df['predicted_price']).round(2)
df['abs_residual'] = df['residual'].abs()

# ---------------------
# Z-Score Standardization
# ---------------------

mean_res = df['residual'].mean()
std_res = df['residual'].std()

df['residual_z'] = (df['residual'] - mean_res) / std_res

df['anomaly_flag'] = np.where(
    df['residual_z'].abs() > 2,
    'anomaly', 'normal'
)

# ---------------------
# Basic Anomaly Detection
# ---------------------

df_sorted = df.sort_values('residual', ascending=True)

top_overpriced = df_sorted.head(20)
top_undervalued = df_sorted.tail(20)

cols = [
    "district",
    "actual_price",
    "predicted_price",
    "residual",
    "abs_residual",
    "residual_z",
    'anomaly_flag'
]

top_overpriced = top_overpriced[cols]
top_undervalued = top_undervalued[cols]

# ---------------------
# District Level Residual Insight
# ---------------------

district_stats = df.groupby('district').agg(
    mean_residual = ('residual', 'mean'),
    avg_error = ('abs_residual', 'mean'),
    volatility = ('residual_z', 'std'),
    transaction_count = ('actual_price', 'count')
).reset_index()

most_overpriced_districts = district_stats.sort_values('mean_residual', ascending=False).head(10)
most_undervalued_districts = district_stats.sort_values('mean_residual').head(10)
most_volatile_districts = district_stats.sort_values('volatility', ascending=False).head(10)

# ---------------------
# Export Outputs
# ---------------------

df.to_csv(ARTIFACT_DIR / 'anomalies_data.csv', index=False)
top_overpriced.to_csv(ARTIFACT_DIR / 'top_overpriced.csv', index=False)
top_undervalued.to_csv(ARTIFACT_DIR / 'top_undervalued.csv', index=False)
district_stats.to_csv(ARTIFACT_DIR / 'district_residuals.csv', index=False)