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

## ✅ Day 8 — Dashboard Enhancement & UX Improvement (Completed)

### Objective

Improve dashboard usability, clarity, and analytical value by enhancing layout, interactivity, and visualization design.

### Tasks

### Completed

**Page Structure & User Flow**

- Reorganized dashboard into a clear top-down analytical story:
  - Title → Key Metrics → Filters (sidebar) → Trends → Distribution → Comparison → Table
- Improved logical flow to guide users from overview → exploration → detail

**Key Metrics**

- Added summary metrics at the top of the dashboard:
  - Average price per sqm
  - Median price per sqm
  - Transaction count
- Provides immediate high-level context before deeper analysis

**Filter Enhancements**

- Upgraded district filter to **multiselect** for flexible comparison
- Added:
  - Price range filter
  - Area range filter
- Improved user control over dataset exploration

**Visualization Improvements**

- Enhanced chart readability and interpretability:
  - Added axis labels and titles
  - Included captions to explain chart purpose and usage
- Made charts more self-explanatory for non-technical users

**Price Trend Enhancements**

- Redesigned trend visualization into two approaches:
  - **Daily trend with rolling averages**
    - Helps reveal underlying patterns and smooth volatility
  - **Flexible aggregation view**
    - User-selectable granularity: Daily / Weekly / Monthly
- Allows both detailed inspection and high-level trend analysis

**Table Improvements**

- Enhanced transaction table usability:
  - Sorted by most recent transactions
  - Added `building_type` field for more context
  - Formatted date to display only date (no time component)
- Added **CSV download button** for data export
- Improves usability for real-world users (e.g. property agents, analysts)

### Key Outcome

- Dashboard is now **user-friendly and insight-driven**
- Users can:
  - Quickly understand the market (via metrics)
  - Explore trends and distributions interactively
  - Drill down into real transaction data
- Marks transition from **functional MVP → usable analytical product**

---

## 🔄 Day 9 — Filter Consistency & Data Integrity Alignment (Planned)

### Objective

Ensure all dashboard components respond consistently to user filters and establish a clear, unified analytical logic before further architectural changes.

---

### Key Focus Areas

#### 1. Filter Consistency Across All Visualizations (HIGH PRIORITY)

- Ensure **all charts use filtered dataset (`filtered_df`)**
- Fix inconsistency where some visualizations rely on full dataset (e.g. district comparison)
- Align dashboard behavior with user expectation:
  - “All charts reflect current filter selection”

---

#### 2. Standardize Core Metric Definition (HIGH PRIORITY)

- Confirm `final_price_per_sqm` as the **primary analytical metric**
- Ensure consistent usage across:
  - charts
  - filters
  - key metrics section
- Avoid mixing different pricing definitions in core analysis

---

#### 3. Improve Filter Logic Consistency (HIGH PRIORITY)

- Review and align behavior of:
  - price range slider
  - area range slider
- Ensure filters are applied in a clear and predictable way
- Define whether filter ranges represent:
  - full dataset bounds, or
  - dynamically filtered bounds (future enhancement)

---

#### 4. UX Clarity & Trust Improvements (MEDIUM PRIORITY)

- Add captions or notes to reinforce:
  - filtering behavior
  - metric definitions
- Ensure dashboard interactions feel intuitive and reliable

---

### Optional Improvements (If Time Permits)

- Improve slider UX:
  - rounded values (e.g. steps of 10,000)
  - better readability and formatting
- Minor UI polish for consistency

---

### Key Outcome

- Dashboard becomes **consistent, predictable, and trustworthy**
- All components align with user-selected filters
- Analytical foundation is stabilized for future expansion

---

### Note

Multi-page architecture and layout redesign are intentionally deferred to Day 10 to avoid compounding inconsistencies during structural changes.

---

## 🧱 Day 10 — Multi-Page Architecture & Product Structuring (Planned)

### Objective

Refactor the dashboard into a multi-page structure to improve usability, scalability, and alignment with real-world analytical workflows.

---

### Key Focus Areas

#### 1. Introduce Multi-Page App Structure (HIGH PRIORITY)

- Split dashboard into logical pages using Streamlit multi-page architecture
- Ensure clean separation of concerns between pages
- Maintain shared data loading and filter logic

---

#### 2. Define Page-Level Responsibilities (HIGH PRIORITY)

**Overview Page**

- Key metrics
- Price trends
- Price distribution

**District Analysis Page**

- District comparison
- Ranking and aggregation insights

**Data Explorer Page**

- Transaction table
- Detailed record-level exploration

---

#### 3. Refactor Filter Design (HIGH PRIORITY)

- Adapt filters to be **context-aware per page**
- Ensure filters shown are relevant to page purpose
- Avoid redundant or misleading controls (e.g. district filter in comparison context)

---

#### 4. Improve Navigation & User Flow (MEDIUM PRIORITY)

- Add clear page navigation (sidebar or top-level selection)
- Ensure smooth transition between:
  - overview → comparison → detailed exploration
- Maintain consistent user experience across pages

---

### Optional Improvements (If Time Permits)

- Introduce shared filter components across pages
- Improve layout and spacing for readability
- Explore better organization of UI sections

---

### Key Outcome

- Dashboard evolves into a **structured analytical product**
- Users can navigate between:
  - high-level overview
  - comparative insights
  - detailed data exploration
- Codebase becomes more modular and scalable for future features

---

### Note

Further UX enhancements (advanced filter interactions, layout redesign, styling improvements) will be explored in subsequent iterations after structural foundation is complete.

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
