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

### Completed

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

## Goal

Transform the cleaned dataset and analysis into a **user-focused analytical dashboard** that supports real-world decision making.

---

## Key Focus Areas

1. **Interaction Layer**

   - Filters
   - Visualizations
   - User exploration

2. **Analytical Depth**

   - Rankings
   - Distributions
   - Comparisons
   - Derived metrics (median, volume)

3. **Productization**
   - Multi-page structure
   - UX improvements
   - Clear user workflows

---

## ✅ Day 7 — Dashboard MVP - Streamlit (Completed)

### Objective

Convert the analytical pipeline into an interactive dashboard for exploring Taiwan housing data.

### Completed

**App Architecture Improvements**

- Built Streamlit dashboard (`app.py`)
- Structured code into clear sections:
  - Data layer
  - Filter logic
  - Visualization functions
  - UI rendering components
  - Main application flow
- Improved maintainability and readability of codebase

**Core Functionality**

- Connected Streamlit app to SQLite database
- Implemented cached data loading (`st.cache_data`)

**Filtering System**

- Sidebar filters implemented:
  - District selection
  - Date range selection
- Applied stricter date handling:
  - Prevents invalid selections
  - Ensures consistent datetime filtering

**Visualizations (MVP)**

- Price per sqm distribution (histogram)
- District-level average price comparison (bar chart)
- Price trend over time (line chart)

**Data Exploration Table**

- Added sample transaction table
- Displays:
  - date (formatted as date only)
  - district
  - address
  - price
  - area
  - final_price_per_sqm
- Toggle to show/hide table

### Key Outcome

- Functional dashboard MVP completed
- Users can explore:

  - pricing distribution
  - district comparisons
  - time trends
  - transaction-level data

- Codebase is modular and ready for scaling

---

## 🚀 Day 8 — Dashboard Enhancement & UX Improvement

### Objective

Improve usability, consistency, and analytical depth of the dashboard.

### Tasks

**UX / UI Improvements**

- Improve layout structure and section grouping
- Ensure consistent chart sizing and spacing
- Add clearer visual hierarchy (titles, sections, flow)

**Filter Enhancements**

- Support multi-district selection
- Add additional filters:
  - price range
  - area range (optional)
- Ensure all charts use consistent filtered dataset

**Bug Fixes / Consistency**

- Fix inconsistency where some charts use unfiltered data
- Standardize filtering across all components

**Analytical Enhancements**

- Add at least 1–2 deeper insights:
  - median price per district
  - district ranking (top/bottom)
  - boxplot for price distribution by district

**Table Improvements**

- Enable sorting (e.g. by price)
- Improve readability and usability
- Optional: limit control or pagination

### Expected Outcome

- Dashboard becomes more intuitive and consistent
- Improved analytical value beyond basic visualization
- Better user experience for exploration

---

## 🚀 Day 9 — Product Direction & Multi-Page Dashboard

### Objective

Transition from a single-page analytical dashboard into a **user-focused analytical product** tailored for property agents.

Define product direction, restructure the app, and introduce key features that support real-world decision making.

---

### Tasks

**Product Definition**

- Define primary target user:
  - Property agents
- Identify key user needs:
  - Market overview (price trends, distributions)
  - High-activity districts (transaction volume)
  - Pricing benchmarks (median, ranges)
  - Comparable transactions (recent deals)

---

**App Restructuring (Multi-Page Architecture)**

- Refactor Streamlit app into multiple pages:

  1. **Market Overview**

     - KPI metrics:
       - average price per sqm
       - median price per sqm
       - total transactions
     - price trend over time
     - price distribution

  2. **District / Map Analysis**

     - District-level comparison:
       - average price per sqm
       - transaction volume
     - Ranking:
       - top districts by price
       - top districts by volume

  3. **Transaction Explorer**
     - Enhanced transaction table
     - Sorting (price, area, date)
     - Filter-heavy exploration

  _(Optional for later)_ 4. **District Deep Dive**

  - Detailed breakdown for a selected district

---

**Map Visualization (Key Feature)**

- Introduce map-based visualization:
  - District-level view:
    - color → price
    - size → transaction volume
- Evaluate tools:
  - `pydeck` (preferred)
  - or `plotly` maps

---

**Analytical Enhancements**

- Add new metrics:
  - median price per sqm
  - transaction volume per district
- Introduce district ranking:
  - by price
  - by volume

---

### Expected Outcome

- Dashboard evolves from MVP → structured analytical product
- Clear separation of user workflows across pages
- Introduction of decision-oriented insights (not just visuals)
- Foundation for further feature expansion (Day 10+)

# Phase 2 Completion Criteria

Phase 2 is considered complete when the dashboard:

### 1. Product Structure

- Has a **multi-page layout** with clear separation of:
  - overview
  - district analysis
  - transaction exploration

---

### 2. User-Focused Design

- Clearly targets a defined user group:
  - property agents
- Supports key user questions:
  - Where is activity highest?
  - How are prices trending?
  - What are comparable transactions?

---

### 3. Analytical Capabilities

- Includes:
  - price trends over time
  - distribution analysis
  - district-level comparison
  - transaction volume metrics
  - median price (not just mean)

---

### 4. Interactivity

- Fully functional filtering:

  - district (multi-select)
  - date range
  - (optional) price / area filters

- All components respond consistently to filters

---

### 5. Core Features

- Transaction exploration table
- District ranking (price & volume)
- Basic map visualization (district-level)

---

### 6. Code Quality

- Modular and maintainable code structure
- Clear separation of:
  - data
  - logic
  - UI

---

### Final Outcome

A **functional analytical product MVP** that goes beyond visualization and supports decision-making for property agents.

---

# Future Work & Improvements (Post-MVP)

## Advanced Analytics

- Price growth analysis (month-over-month, year-over-year)
- District segmentation (high-end vs affordable areas)
- Volatility / stability indicators
- Outlier detection (overpriced / underpriced transactions)

---

## Enhanced Map Features

- Transaction-level map (point-based visualization)
- Heatmaps for price and volume
- Geographic clustering

---

## User Experience Improvements

- KPI cards with trend indicators (↑ ↓)
- Better layout and visual polish
- Improved loading performance

---

## Additional User Segments

### Property Buyers

- affordability insights
- recent comparable transactions
- price trends by area

### Investors

- high-growth districts
- emerging areas
- price momentum indicators

### Analysts / Developers

- deeper statistical analysis
- clustering and segmentation
- long-term trend analysis

---

## Productization

- Deploy dashboard (Streamlit Cloud or similar)
- Add documentation and usage guide
- Improve README for portfolio presentation

---

## Data Expansion

- Incorporate external data:
  - transport (MRT proximity)
  - demographics
  - amenities
- Extend beyond housing-only dataset

## Data Model Expansion (Future Phase)

Current dataset is scoped to **housing transactions only** for consistency.

Future expansion may include handling multiple transaction types:

- housing
- land
- parking

### Challenges

- Each type requires different metrics:

  - housing → price per sqm
  - land → price per land area
  - parking → price per unit

- Current pricing logic is **not directly transferable**

### Potential Approaches

- Split dataset by transaction type
- Introduce normalized schema
- Build type-specific analytical views

### Implication

- Requires redesign of:
  - data pipeline
  - pricing logic
  - dashboard UX
