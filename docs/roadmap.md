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

## 📊 Day 6 — Analytical Deep Dive

### Objective

Deepen analysis and validate pricing logic and data reliability.

### Tasks

- Analyze pricing methods:

  - Compare `original`, `net_adjusted`, and `fallback_computed`
  - Evaluate differences in price per sqm

- Perform district segmentation:

  - Rank districts by price per sqm
  - Compare top vs bottom districts
  - Identify pricing patterns and gaps

- Conduct data quality checks:

  - Measure usage of each pricing method
  - Analyze discrepancies (`price_diff`, `net_price_diff`)
  - Assess reliability of computed values

- Summarize findings:
  - Highlight key patterns and inconsistencies
  - Identify strengths and limitations of the dataset

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

# Phase 2 — Analytical Product Development

## 🚀 Day 7 — Dashboard Foundation (Streamlit)

### Objective

Transform analysis into an interactive tool for exploration.

### Tasks

- Set up Streamlit project structure
- Load cleaned dataset from SQLite
- Build basic UI:

  - Title and project description
  - Sidebar filters:
    - district
    - date range

- Create initial visualizations:

  - Price per sqm distribution
  - District comparison chart
  - Time trend chart

- Ensure interactivity:
  - Filters dynamically update charts

### Expected Outcome

- A working interactive dashboard (MVP)
- Users can explore housing prices by district and time

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
