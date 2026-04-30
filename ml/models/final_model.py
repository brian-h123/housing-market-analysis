import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error

from ml.data_prep import prepare_dataset
from ml.models.explainability import (
    get_feature_importance,
    clean_feature_names,
    plot_feature_importance
)

# ---------------------
# Config
# ---------------------

TARGET = 'final_price_per_sqm'
ARTIFACT_DIR = 'ml/models/artifacts'
MODEL_PATH = os.path.join(ARTIFACT_DIR, 'ridge_model.pkl')
FEATURE_PATH = os.path.join(ARTIFACT_DIR, 'feature_columns.json')

RANDOM_STATE = 42

# ---------------------
# Training Pipeline
# ---------------------

def train_model():
    # Load dataset
    df = prepare_dataset()

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # ---------------------
    # Feature Selection
    # ---------------------

    # Drop correlated area features
    cols_to_drop = [
        'area',
        'main_area',
        'net_area'
    ]
    X = X.drop(columns=cols_to_drop)

    # Simplify time features
    X = X.drop(columns=[
        'transaction_year',
        'transaction_month',
        'building_year'
    ])

    # Handle weak/noisy features
    X = X.drop(columns=['floor_level'])

    # ---------------------
    # Save final feature schema
    # ---------------------
    feature_columns = X.columns.tolist()

    # ---------------------
    # Train-test split
    # ---------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")

    return model, feature_columns

# ---------------------
# Save Artifacts
# ---------------------

def save_artifacts(model, feature_columns):
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    # Save model
    joblib.dump(model, MODEL_PATH)

    # Save feature columns
    with open(FEATURE_PATH, 'w') as f:
        json.dump(feature_columns, f)

def run_explainability_pipeline(model, feature_columns):
    importance_df = get_feature_importance(model, feature_columns)
    importance_df = clean_feature_names(importance_df)

    # Save output
    importance_df.to_csv(
        os.path.join(ARTIFACT_DIR, 'feature_importance.csv'),
        index = False
    )

    plot_feature_importance(importance_df)
    print('Explanability completed.')

# ---------------------
# Main
# ---------------------

def main(run_explainability=True):
    print('Start training.')
    model, feature_columns = train_model()
    save_artifacts(model, feature_columns)
    
    if run_explainability:
        print('Start explainability pipeline')
        run_explainability_pipeline(model, feature_columns)

    print('Done.')


if __name__ == "__main__":
    main()