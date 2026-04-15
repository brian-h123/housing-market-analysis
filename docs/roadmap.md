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

## ✅ Day 4 — Data Scope Refinement & Visualization (Completed)

### Objective

Ensure dataset consistency and begin producing meaningful visual insights.

### Completed

**Data Scope Refinement**

- Included `transaction_type` in dataset
- Filtered dataset to housing-related transactions only (`房地`)
- Removed land-only and parking-only records
- Validated dataset consistency after filtering

**Visualization**

- Generated distribution plots:
  - log(price)
  - log(area)
- Built key comparison charts:
  - price vs area
  - district-level price metrics

### Key Outcome

- Dataset is now **consistent and comparable**
- `price_per_sqm` is now meaningful across observations
- Established a reliable foundation for insight generation

---

## ✅ Day 5 — Insight Generation & Storytelling (Completed)

### Objective

Transform analysis results into clear, structured insights.

### Tasks

**Time-based Analysis**

- Analyzed monthly trends:
  - Average price per sqm over time
  - Transaction volume over time
- Identified general market movement patterns (growth / stability / fluctuations)

**Visualization Improvements**

- Improved chart readability:
  - Fixed overlapping text
  - Adjusted label positioning
  - Added clear titles and axis labels
- Ensured consistent formatting across charts

**Insight Generation**

- Identified key district-level pricing differences
- Observed variation patterns across districts:
  - High-variance districts (e.g. wider spread in boxplots)
  - Low-variance districts (more stable pricing)
- Noted presence of long whiskers in some districts → indicating occasional extreme transactions

**Documentation**

- Summarized findings into structured observations
- Highlighted:
  - Key trends
  - Notable anomalies
  - Early interpretations of market behavior

### Key Outcome

- Raw analysis is now translated into **clear, explainable insights**
- Visualizations are **presentation-ready**
- Foundation is set for deeper analytical validation (Day 6)

---

## ✅ Day 6 — Analytical Deep Dive (Completed)

### Objective

Deepen analysis and validate pricing logic and data reliability.

### Completed

**Pricing Method Analysis**

- Compared `original`, `net_adjusted`, and `fallback_computed`
- Measured differences using:
  - `price_diff`
  - `net_price_diff`
- Observed that:
  - `original` pricing shows small deviations vs computed values
  - `net_adjusted` significantly reduces discrepancy when parking is involved

**District Segmentation**

- Ranked districts by `final_price_per_sqm`
- Identified:
  - High-priced districts (premium areas)
  - Lower-priced districts (more affordable areas)
- Observed clear pricing gaps between top and bottom tiers

**Data Quality Validation**

- Measured usage of pricing methods:
  - Majority: `original`
  - Significant portion: `net_adjusted`
  - Small portion: `fallback_computed`
- Validated that:
  - `net_adjusted` improves pricing consistency
  - fallback logic is necessary but limited in usage

**Discrepancy Analysis**

- `price_diff` confirms mismatch in raw dataset
- `net_price_diff` shows improved alignment after adjustment
- Confirms correctness of pricing logic design

### Key Outcome

- Pricing methodology is **validated and reliable**
- Dataset is **internally consistent**
- Analytical assumptions are now **tested and defensible**

---

# ✅ Phase 1 Summary — Data Foundation & First Insights

### What Was Achieved

- Built a complete **data pipeline**:

  - ingestion → cleaning → storage (SQLite)

- Transformed raw data into a **clean, structured dataset**:

  - Removed invalid and inconsistent records
  - Scoped dataset to **housing-only transactions**

- Developed **robust pricing logic**:

  - Introduced `net_price` and `net_area`
  - Created `final_price_per_sqm`
  - Implemented `pricing_method` tracking

- Generated **meaningful insights**:

  - District-level pricing differences
  - Distribution patterns and skewness
  - Time-based trends
  - Variance differences across districts

- Validated **data reliability**:
  - Identified inconsistencies in raw dataset
  - Demonstrated improvement via `net_adjusted` logic
  - Quantified discrepancies using `price_diff`

---

### Key Learnings

- Raw real estate data is **context-dependent**, not plug-and-play
- Parking inclusion is a **major source of pricing distortion**
- Data cleaning is not just preprocessing — it is **core to analysis validity**
- Defining dataset scope is **as important as feature engineering**

---

### Limitations

- Dataset only covers **housing transactions**
- No handling yet for:
  - land
  - parking-only transactions
- No external data enrichment (e.g. location, transport, demographics)

---

### Phase 1 Conclusion

Phase 1 successfully delivers a **clean, reliable, and analyzable dataset**, along with **validated pricing logic and initial insights**.

## → Ready to transition into **productization (Phase 2)**

# Phase 2 — Analytical Product Development

## 🚀 Day 7 — Dashboard MVP (Streamlit)

### Objective

Convert analysis into an interactive exploration tool.

### Tasks

**Setup**

- Initialize Streamlit app structure
- Connect to SQLite database
- Load cleaned dataset

**Core UI**

- Page title + short project description
- Sidebar filters:
  - district (dropdown)
  - date range (slider)

**Core Visuals (MVP)**

- Distribution:

  - price per sqm (histogram)

- Comparison:

  - district-level average price

- Trend:
  - price per sqm over time

**Interactivity**

- Ensure all charts respond to filters
- Keep layout clean and readable

### Expected Outcome

- Functional dashboard MVP
- Users can explore pricing across:
  - districts
  - time

---

## 🚀 Day 8 — Dashboard Enhancement & UX Improvement

### Objective

Improve usability, clarity, and analytical depth of the dashboard.

### Tasks

**UX Improvements**

- Improve layout spacing and structure
- Add section headers (Distribution / Comparison / Trends)
- Add chart titles and descriptions

**New Features**

- Add metric cards:
  - average price per sqm
  - total transactions
- Add top/bottom district ranking table

**Data Controls**

- Add pricing method filter:
  - original / net_adjusted / fallback_computed

**Visualization Improvements**

- Improve readability:
  - axis formatting
  - label clarity
- Reduce clutter and overlapping elements

### Expected Outcome

- Dashboard is **not just functional, but usable**
- Insights are easier to interpret for non-technical users

---

# Phase 2 Completion Criteria

Phase 2 will be considered complete when:

- A working **interactive dashboard (Streamlit)** is deployed
- Users can:

  - filter by district and date
  - explore price distributions
  - compare districts
  - view time trends

- Dashboard includes:

  - at least 3–5 core visualizations
  - clear labels and explanations
  - responsive interactivity

- Key insights from Phase 1 are:

  - reflected in the dashboard
  - easily discoverable

- Codebase is:
  - modular
  - readable
  - reproducible

---

### Stretch Goals (Optional)

- Add map-based visualization
- Add export functionality
- Add automated data refresh pipeline

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
