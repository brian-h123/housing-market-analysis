# Taiwan Housing Analytics Platform

An end-to-end data science project that transforms raw Taiwan housing transaction data into an interactive analytical and machine learning-powered dashboard.

The system includes:

- Data cleaning & feature engineering pipeline
- Exploratory data analysis & insights
- Machine learning price prediction model
- Anomaly detection system
- Interactive Streamlit dashboard

## System Architecture

Raw Data
↓
Data Ingestion (ingestion.py)
↓
Feature Engineering (data_prep.py)
↓
ML Model Training (final_model.py)
↓
Artifact Generation:

- model.pkl
- feature_columns.json
- anomalies_dataset.csv
- insights artifacts
  ↓
  Streamlit Dashboard (dashboard/app.py)
  ↓
  ML Lab + Insights + Visualization

## Setup

### 1. Install dependencies

```bash
conda env create -f environment.yml
conda activate taiwan-housing
```

### 2. Run data pipeline (required first time only)

```bash
python ingestion.py
python data_prep.py
```

### 3. Train ML model (required for ML features)

```bash
python final_model.py
```

### 4. Genrate anomaly + insight artifacts

```bash
python anomaly.py
python engine.py
```

### 5. Run Dashbaord

```bash
streamlit run dashboard/app.py
```

## Recommended Execution Order

1. ingestion.py
2. data_prep.py
3. final_model.py
4. anomaly.py
5. engine.py
6. streamlit run dashboard/app.py
