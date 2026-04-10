# Project Roadmap

This roadmap tracks the evolution of the Taiwan housing data project.

It is intentionally structured as a living document:
new phases and tasks will be added as the project progresses.

---

# Current Phase: Phase 1 — Data Foundation & First Insights

## Goal

Transform raw housing transaction data into a clean, analysable dataset and produce initial insights and visualizations.

---

# Phase 1 Progress

## ✅ Day 1 — Data Cleaning & Validation (Completed)

### Objective

Improve the quality and consistency of the dataset.

### Completed

- Built data ingestion pipeline (`ingestion.py`)

  - Downloaded and extracted ZIP data
  - Loaded CSV into pandas
  - Stored cleaned data into SQLite

- Cleaned dataset:

  - Renamed columns to English
  - Converted `date` to datetime format
  - Cleaned numeric fields (`price`, `area`, `price_per_sqm`)
  - Standardized string fields (`address`, `district`)

- Data validation:

  - Removed invalid values (price <= 0, area <= 0)
  - Applied basic outlier filtering
  - Verified dataset using summary statistics

- Feature creation:
  - `computed_price_per_sqm`
  - `price_diff`

---

## ✅ Day 2 — Exploratory Data Analysis (Completed)

### Objective

Understand pricing patterns and identify data issues.

### Completed

- Analyzed distributions of:

  - price
  - area
  - price_per_sqm

- Applied log transformation to:

  - price
  - area

- Created visualizations:

  - histograms (raw and log)
  - scatter plots (price vs area)

- Aggregated district-level metrics:

  - average price
  - median price
  - transaction volume

- Investigated discrepancies:
  - Identified mismatch between `price_per_sqm` and computed values
  - Found that discrepancies are largely explained by:
    - parking price
    - parking area

### Key Outcome

- Identified missing components in dataset that affect pricing accuracy  
  → Led to pipeline improvement in Day 3

---

## 🔄 Day 3 — Data Refinement & Feature Engineering (In Progress)

### Objective

Improve accuracy of pricing metrics by incorporating missing components (e.g. parking).

### Tasks

- Update ingestion pipeline to include:

  - `parking_price` (車位總價元)
  - `parking_area` (車位移轉總面積平方公尺)
  - `main_building_area` (主建物面積)

- Clean and convert new columns to numeric

- Create improved pricing features:

  - `net_price = price - parking_price`
  - `net_area = area - parking_area`
  - `net_price_per_sqm = net_price / net_area`

- Re-evaluate discrepancies between:

  - original `price_per_sqm`
  - computed values
  - net values

- Implement fallback logic:
  - Fill missing `price_per_sqm` using computed values

### Output

- More accurate and reliable dataset
- Clear explanation of pricing discrepancies

---

## 📊 Day 4 — Visualization & Insight Communication (Planned)

### Objective

Transform refined data into clear and compelling visual insights.

### Tasks

- Finalize distribution plots:

  - price (log scale)
  - area (log scale)

- Create district-level comparisons:

  - average / median price per sqm (bar charts)
  - transaction volume by district

- Build time-based analysis:

  - monthly price trends
  - transaction volume over time

- Refine existing plots:
  - improve labeling and readability
  - ensure consistency in styling
  - remove unnecessary clutter

### Output

- 3–5 high-quality visualizations
- Clear and interpretable data story

---

# Phase Completion Criteria

Phase 1 will be considered complete when:

- Dataset is clean and analysis-ready
- Pricing logic is accurate and validated
- Core descriptive insights are generated
- At least 3 meaningful visualizations are created
- Key findings are documented

---

# Future Work (To Be Defined)

The following areas are planned for later phases:

- Interactive dashboard (Streamlit)
- Geographic visualization (map-based analysis)
- Automated data ingestion (e.g. scheduled updates)
- Data enrichment (external datasets)
- Feature engineering and predictive modeling
