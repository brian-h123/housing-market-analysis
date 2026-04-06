# Project Roadmap

This roadmap tracks the evolution of the Taiwan housing data project.

It is intentionally structured as a living document:
new phases and tasks will be added as the project progresses.

---

# Current Phase: Phase 1 — Data Foundation & First Insights

## Goal

Transform raw housing transaction data into a clean, analysable dataset and produce initial insights and visualizations.

This phase focuses on:

- data quality improvements
- exploratory analysis
- first visual outputs

---

# Phase 1 — Short-Term Plan (Next 3 Days)

## Day 1 — Data Cleaning & Validation

### Objective

Improve the quality and consistency of the dataset.

### Tasks

- Convert `date` field into datetime format
- Improve numeric handling for:
  - price
  - area
  - price_per_sqm
- Add fallback logic for missing `price_per_sqm`
- Basic outlier handling (percentile-based filtering)
- Validate dataset using summary statistics

### Output

- Clean and consistent dataset ready for analysis

---

## Day 2 — Exploratory Data Analysis (EDA)

### Objective

Understand pricing patterns across districts.

### Tasks

- Compute median and average price per district
- Rank districts by price per square meter
- Count transaction volume per district
- Identify top/bottom priced districts

### Output

- Core analytical tables
- Initial insight summary

---

## Day 3 — Data Visualization Layer

### Objective

Translate analysis into visual insights.

### Tasks

- Create price distribution histogram
- Create district comparison bar chart
- Create simple time trend (monthly aggregation)
- Export plots for documentation

### Output

- 2–3 visualizations representing key insights
- First “data story” from the dataset

---

# Phase Completion Criteria

Phase 1 will be considered complete when:

- Dataset is clean and analysis-ready
- Core descriptive insights are generated
- At least 2 meaningful visualizations are created

---

# Future Work (To Be Defined)

The following areas are planned for later phases and will be expanded after Phase 1:

- Interactive dashboard (Streamlit or similar)
- Geographic visualization (map-based analysis)
- Automated data ingestion (GitHub Actions)
- Data source improvements or expansion
- Advanced feature engineering and modeling
