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

## ✅ Day 3 — Data Refinement & Feature Engineering (Completed)

### Objective

Improve accuracy and reliability of pricing metrics by refining calculation logic and handling missing/inconsistent data.

### Completed

- Enhanced ingestion pipeline with additional fields:

  - `parking_price`
  - `parking_area`
  - `main_area`

- Implemented **conditional pricing logic**:

  - If parking data is available → exclude parking from both price and area
  - Otherwise → fallback to total price and total area

- Added **fallback logic for missing `price_per_sqm`**:

  - Use computed `price / area` when original value is missing

- Introduced new features:

  - `net_price`, `net_area`
  - `net_price_per_sqm`
  - `final_price_per_sqm`
  - `pricing_method` (original / net_adjusted / fallback_computed)

- Re-evaluated discrepancies between:
  - original vs computed vs adjusted pricing

### Key Findings

- `price_per_sqm` is **context-dependent**, not a simple ratio:

  - Strongly affected by parking inclusion/exclusion

- Raw dataset contains **heterogeneous transaction types**:

  - e.g. housing, land, parking

- Identified an important missing feature:

  - `交易標的` (transaction type)

- Observed that:
  - Land transactions → building area = 0 → invalid for current calculations
  - Parking-only transactions → `price_per_sqm` is naturally missing

### Implication

- Current dataset mixes **non-comparable transaction types**
- Some rows violate assumptions behind `price_per_sqm`
- A **data scope definition problem** exists (not just a calculation issue)

→ Decision:

- For MVP, prioritize **data consistency via filtering**
- Defer full multi-type handling to later phases

---

## 📊 Day 4 — Data Scope Refinement & Visualization (Planned)

### Objective

Ensure dataset consistency and begin producing meaningful visual insights.

### Tasks

**Data Scope Refinement (High Priority)**

- Include `transaction_type` (`交易標的`) in cleaned dataset
- Filter dataset to **housing-related transactions only**
  - Exclude land-only and parking-only records
- Validate impact of filtering on:
  - distribution
  - pricing metrics

**Visualization**

- Finalize distribution plots:

  - price (log scale)
  - area (log scale)

- Create district-level comparisons:
  - average / median price per sqm
  - transaction volume

---

## 📊 Day 5 — Insight Generation & Storytelling (Planned)

### Objective

Turn analysis into clear, structured insights.

### Tasks

- Build time-based analysis:

  - monthly price trends
  - transaction volume over time

- Improve visualization quality:

  - labeling
  - readability
  - consistency

- Identify and document key insights:
  - pricing differences across districts
  - trend patterns over time

---

# Phase Completion Criteria

Phase 1 will be considered complete when:

- Dataset is **clean, consistent, and scoped to valid housing transactions**
- Pricing logic (`price_per_sqm`) is:
  - clearly defined
  - consistently applied
  - documented with assumptions
- Core descriptive insights are generated
- At least 3–5 meaningful visualizations are created
- Key findings and limitations are documented

---

# Future Work & Improvements (Post-MVP)

### Data Modeling

- Handle different transaction types separately:

  - housing
  - land
  - parking

- Define **type-specific metrics**:

  - housing → price per sqm
  - land → price per land area
  - parking → price per unit

- Consider splitting dataset or introducing a normalized schema

---

### Pipeline Enhancements

- Modularize ingestion pipeline further
- Add data validation checks by transaction type
- Implement logging and monitoring

---

### Analysis & Product

- Interactive dashboard (Streamlit)
- Geographic visualization (map-based analysis)
- Automated data ingestion (scheduled updates)

---

### Advanced Analytics

- Feature engineering for modeling
- Predictive modeling (price estimation)
- External data enrichment (e.g. demographics, transport)
