# Taiwan Housing Analytics Platform

Taiwan publishes every residential property transaction as open data, but the raw
feed is difficult to reason with. Records arrive with mixed traditional-Chinese field encodings, ambiguous property area values, and land and building areas reported separately. The result is a dataset that is public but not usable, and that gap is what this rpoject closes.

This repository takes that raw feed and produces three things: a price prediction
model for residential units, an anomaly detector that surfaces transactions whose
recorded price is implausible given comparable properties, and a Streamlit
dashboard for exploring price drivers across districts and property types.

## Design decisions

A few choices worth flagging, since they shaped everything downstream.

**Feature engineering over model complexity.** `price per sqm`, `building age`, `area`, `transaction type`, `location`. Most of the predictive signal came from `price per sqm` and `location`, so effort went into deriving those cleanly rather than into a heavier model.

**Ridge Regression.** Chose [Ridge Regression] over [Random Forest] and [XGBoost] because the underlying structure of the dataset is largely linear rather than highly non-linear.

**Anomaly detection as a separate layer.** Rather than filtering outliers out during cleaning, they are flagged and preserved, since they are real property transactions that highlights even within premium areas, pricing can vary significantly across transactions, as well as how real transactions differ from model predictions which indicates overpricing and undervaluations. 

**Modular scripts, not notebooks.** The pipeline runs end to end from a clean
checkout. Exploratory notebooks are archived under `archive/notebooks` and are not
part of the execution path.

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

## Data 

**Source.** https://lvr.land.moi.gov.tw/

Data is download directly from "https://plvr.land.moi.gov.tw/Download?type=zip&fileName=lvr_landcsv.zip"

**Coverage.** 200+ transactions on all districts from Taipei City, from Jan to Mar 2026. 

**Granularity.** Transaction-level records. Each row carries `date`, `address`, `price`, `area`, `price per sqm`, `building type`, `district`.

**Preprocessing.** Dataset is filtered to housing-related transactions only, not including presale contracts, rentals, and parking-space-only. 

**Known limitation.** The dataset size is relatively small as it only span across three months of 2026 in Taipei City. Geospatial information is also capped at district level, where finer granulaties like coordinates and distance to nearest MRT station could have reveal more insights.

Raw data is not committed to this repository. Run `python ingestion.py` to fetch
it, or see `docs/` for the manual download steps.

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

## Notebooks

Exploratory and experimental notebooks are stored under `/archive/notebooks`.

These include:

- early EDA
- model experimentation
- explainability analysis

The production system is fully implemented in modular Python scripts under:

- `data/`
- `ml/`
- `insights/`
- `dashboard/`
