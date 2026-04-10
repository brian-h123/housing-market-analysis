# Progress Log

This file tracks daily execution of the project starting from Phase 1.

---

## Day 1 — Data Cleaning & Validation

### Completed

- Built initial data ingestion pipeline (`ingestion.py`)

  - Fetch data from Taiwan real estate API (ZIP download)
  - Extract and load CSV into pandas
  - Save cleaned data into SQLite database

- Implemented data cleaning logic:

  - Renamed columns to English
  - Converted `date` to datetime format
  - Cleaned numeric fields (`price`, `area`, `price_per_sqm`)
  - Removed invalid values (price <= 0, area <= 0)
  - Applied basic outlier filtering
  - Standardized string fields (`address`, `district`)

- Added derived fields:
  - `computed_price_per_sqm`
  - `price_diff` (difference between computed and provided values)

### Key Observations

- `price_per_sqm` is not always consistent with `price / area`
- Likely causes:
  - parking space inclusion
  - different area definitions
  - rounding differences

---

## Day 2 — Exploratory Data Analysis (EDA)

### Completed

- Performed EDA using `eda_day2.ipynb`
- Analyzed distribution of:

  - price
  - area
  - price_per_sqm

- Aggregated metrics by district:

  - average price
  - median price
  - transaction count

- Identified:
  - high-priced districts
  - lower-priced districts
  - distribution skewness in key variables

### Key Observations

- Price and area distributions are right-skewed
- Certain districts dominate transaction volume
- Outliers still exist but are partially controlled

---

## Current Status

- Dataset is cleaned and usable
- Initial insights have been generated
- Ready to proceed to visualization and further feature improvements

---

## Next Steps

- Apply log transformation to skewed variables
- Re-evaluate distributions post-transformation
- Begin building visualizations (Day 3)
