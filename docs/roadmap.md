# Project Roadmap

This roadmap tracks the evolution of the Taiwan housing data project.

It is intentionally structured as a living document:
new phases and tasks will be added as the project progresses.

---

## Target Users (Current Focus)

This project is currently designed for:

- Property analysts

Primary use cases:

- Analyze pricing trends across districts
- Compare market segments
- Identify anomalies and outliers in transactions
- Validate pricing consistency and data reliability

**Note:**

- Future iterations may expand to other users (e.g. agents, general buyers)

## Project Goal

Build an analyst-focused dashboard for exploring and validating Taiwan housing transaction data.

# Phase 1 — Data Foundation & First Insights

## Phase 1 Overview

### Goal

Transform raw housing data into a clean, reliable dataset,
define robust pricing metrics, and generate validated insights.

---

## Execution

### ✅ Day 1 — Data Cleaning & Validation (Completed)

#### Objective

Improve the quality and consistency of the dataset.

#### Completed

**Built data ingestion pipeline (`ingestion.py`)**

- Downloaded and extracted ZIP data
- Loaded CSV into pandas
- Stored cleaned data into SQLite

**Cleaned dataset**

- Renamed columns to English
- Converted `date` to datetime format
- Cleaned numeric fields (`price`, `area`, `price_per_sqm`)
- Standardized string fields (`address`, `district`)

**Data validation**

- Removed invalid values (price <= 0, area <= 0)
- Applied basic outlier filtering
- Verified dataset using summary statistics

**Feature creation**

- `computed_price_per_sqm`
- `price_diff`

### ✅ Day 2 — Exploratory Data Analysis (Completed)

#### Objective

Understand pricing patterns and identify data issues.

#### Completed

**Analyzed distributions of**

- price
- area
- price_per_sqm

**Applied log transformation to**

- price
- area

**Created visualizations**

- histograms (raw and log)
- scatter plots (price vs area)

**Aggregated district-level metrics**

- average price
- median price
- transaction volume

**Investigated discrepancies**

- Identified mismatch between `price_per_sqm` and computed values
- Found that discrepancies are largely explained by:
  - parking price
  - parking area

#### Key Outcome

- Identified missing components in dataset that affect pricing accuracy
  - Led to pipeline improvement in Day 3

### ✅ Day 3 — Data Refinement & Feature Engineering (Completed)

#### Objective

Improve accuracy and reliability of pricing metrics by refining calculation logic and handling missing/inconsistent data.

#### Completed

**Enhanced ingestion pipeline with additional fields**

- `parking_price`
- `parking_area`
- `main_area`

**Implemented conditional pricing logic**

- If parking data is available → exclude parking from both price and area
- Otherwise → fallback to total price and total area

**Added fallback logic for missing `price_per_sqm`**

- Use computed `price / area` when original value is missing

**Introduced new features**

- `net_price`, `net_area`
- `net_price_per_sqm`
- `final_price_per_sqm`
- `pricing_method` (original / net_adjusted / fallback_computed)

**Re-evaluated discrepancies between**

- original vs computed vs adjusted pricing

#### Key Outcome

- `price_per_sqm` is **context-dependent**, not a simple ratio:

  - Strongly affected by parking inclusion/exclusion

- Raw dataset contains **heterogeneous transaction types**:

  - e.g. housing, land, parking

- Identified an important missing feature:

  - `交易標的` (transaction type)

- Observed that:

  - Land transactions → building area = 0 → invalid for current calculations
  - Parking-only transactions → `price_per_sqm` is naturally missing

**Implications**

- Current dataset mixes **non-comparable transaction types**
- Some rows violate assumptions behind `price_per_sqm`
- A **data scope definition problem** exists (not just a calculation issue)

**Decision**

- For MVP, prioritize **data consistency via filtering**
- Defer full multi-type handling to later phases

### ✅ Day 4 — Data Scope Refinement & Visualization (Completed)

#### Objective

Ensure dataset consistency and begin producing meaningful visual insights.

#### Completed

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

#### Key Outcome

- Dataset is now **consistent and comparable**
- `price_per_sqm` is now meaningful across observations
- Established a reliable foundation for insight generation

### ✅ Day 5 — Insight Generation & Storytelling (Completed)

#### Objective

Transform analysis results into clear, structured insights.

#### Completed

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

#### Key Outcome

- Raw analysis is now translated into **clear, explainable insights**
- Visualizations are **presentation-ready**
- Foundation is set for deeper analytical validation (Day 6)

### ✅ Day 6 — Analytical Deep Dive (Completed)

#### Objective

Deepen analysis and validate pricing logic and data reliability.

#### Completed

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

#### Key Outcome

- Pricing methodology is **validated and reliable**
- Dataset is **internally consistent**
- Analytical assumptions are now **tested and defensible**

---

## ✅ Phase 1 Summary — Data Foundation & First Insights

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

### Key Learnings

- Raw real estate data is **context-dependent**, not plug-and-play
- Parking inclusion is a **major source of pricing distortion**
- Data cleaning is not just preprocessing — it is **core to analysis validity**
- Defining dataset scope is **as important as feature engineering**

### Limitations

- Dataset only covers **housing transactions**
- No handling yet for:
  - land
  - parking-only transactions
- No external data enrichment (e.g. location, transport, demographics)

### Phase 1 Conclusion

Phase 1 successfully delivers a **clean, reliable, and analyzable dataset**, along with **validated pricing logic and initial insights**.

## Ready to transition into Phase 2 — Productization

---

# Phase 2 — From Analysis to Product

## Phase 2 Overview

With a validated dataset and insights, the next phase focuses on:

- Building an interactive dashboard
- Enabling user-driven exploration
- Translating analysis into a usable tool

### Goal

Transform the cleaned dataset and analysis into a **user-focused analytical dashboard** that supports real-world decision making.

### Key Focus Areas

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

## Execution

### ✅ Day 7 — Dashboard MVP - Streamlit (Completed)

#### Objective

Convert the analytical pipeline into an interactive dashboard for exploring Taiwan housing data.

#### Completed

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

#### Key Outcome

- Functional dashboard MVP completed
- Users can explore:

  - pricing distribution
  - district comparisons
  - time trends
  - transaction-level data

- Codebase is modular and ready for scaling

### ✅ Day 8 — Dashboard Enhancement & UX Improvement (Completed)

#### Objective

Improve dashboard usability, clarity, and analytical value by enhancing layout, interactivity, and visualization design.

#### Completed

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

#### Key Outcome

- Dashboard is now **user-friendly and insight-driven**
- Users can:
  - Quickly understand the market (via metrics)
  - Explore trends and distributions interactively
  - Drill down into real transaction data
- Marks transition from **functional MVP → usable analytical product**

### ✅ Day 9 — Filter Consistency & Data Integrity Alignment (Completed)

#### Objective

Ensure all dashboard components use consistent filtering logic and improve robustness of user interactions.

#### Completed

**Filter Consistency**

- Standardized all charts and components to use `filtered_df`
- Ensured a single source of truth for filtered data across:
  - metrics
  - charts
  - tables

**Data Integrity Validation**

- Added assertions to validate critical fields:
  - `final_price_per_sqm`
  - `area`
- Applied `dropna` after filtering to prevent invalid data from propagating into visualizations

**Edge Case Handling**

- Improved filter robustness:
  - Prevented invalid date selection (must select full range)
  - Prevented empty district selection
- Added user feedback via warnings when filters are invalid or result in no data

**UX Improvements**

- Enhanced slider usability:
  - Rounded price bounds to cleaner values (e.g. steps of 10,000)
  - Improved readability and user control over filter ranges

**User Feedback**

- Added dynamic summary caption showing:
  - selected districts
  - date range
  - price and area filters
  - total transactions
- Provides immediate transparency into current filter state

#### Key Outcome

- Dashboard is now **logically consistent and reliable**
- Filters behave predictably across all components
- Users receive **clear feedback and smoother interaction experience**

### ✅ Day 10 — App Architecture Refactor (Completed)

#### Objective

Refactor the dashboard into a multi-page structure to improve scalability, maintainability, and prepare for future feature expansion.

#### Completed

**Multi-Page Structure**

- Converted app into a multi-page architecture using a sidebar navigation selectbox
- Created separate pages:
  - Overview
  - Trends
  - District Analysis
  - Data Explorer (transactions table)
- Ensured each page renders independently via modular `views/` structure

**Code Organization**

- Refactored `app.py` into a router/controller:
  - Handles navigation logic only
  - Delegates rendering to page-specific modules
- Split codebase into clearer components:
  - `views/` → page-level UI
  - `components/` → reusable UI elements (charts, metrics, sections)
  - `utils/` → data loading and shared logic
- Improved separation of concerns and readability

**Shared Filter System**

- Maintained consistent filter logic across pages
- Ensured all pages rely on the same filtered dataset approach
- Preserved:
  - data integrity checks
  - edge case handling (empty filters, invalid ranges)

**Stability Validation**

- Verified that all existing functionality works after refactor:
  - charts render correctly across pages
  - filters behave consistently
  - no regression in data handling

#### Key Outcome

- App is now **modular and scalable**
- New features can be added per page without affecting others
- Codebase is significantly easier to maintain and extend

### ✅ Day 11 — Smart Filtering (Control & Clarity) (Completed)

#### Objective

Introduce controlled flexibility in filtering while ensuring behavior remains predictable, transparent, and easy to understand.

#### Completed

**Comparison Mode (District Analysis)**

- Implemented **Comparison Mode toggle** on District Analysis page
- Behavior:
  - Default:
    - Uses selected districts from sidebar filters
  - Comparison Mode (enabled):
    - Overrides district filter and displays **all districts**
- Enables clear and intentional district comparison workflows

**Active Filter Logic**

- Introduced concept of **active filters** on District Analysis page:
  - Default filters → user-selected filters from sidebar
  - Active filters → dynamically adjusted based on comparison mode
- Ensured all components (charts, summaries, tables) use **active filters**
- Prevented inconsistencies between UI state and displayed data

**Filter Transparency & Feedback**

- Improved filter summary display:
  - Clearly shows:
    - selected districts (or “All districts” in comparison mode)
    - date range
    - price range
    - area range
    - total transaction count
- Added explicit indication when:
  - Comparison Mode is active
  - District filter is being overridden

**Empty State Handling**

- Added handling for empty datasets:
  - Displays clear message:
    - “No transactions found for selected filters”
- Prevented rendering of charts/tables when dataset is empty
- Improved robustness of user interactions

**Validation & Stability**

- Verified consistent behavior across:
  - normal filtering mode
  - comparison mode
- Tested edge cases:
  - empty district selection
  - narrow date ranges
  - extreme price/area filters
- Ensured no regressions in:
  - filter logic
  - data integrity
  - chart rendering

#### Key Outcome

- Filtering system is now **more flexible yet predictable**
- Users can clearly distinguish between:
  - filtered views
  - full comparison views
- Dashboard provides **better transparency and usability**, especially for district-level analysis

---

### ⏳ Day 12 — Smart Filtering (Responsiveness & UX)

#### Objective

Enhance filtering experience by making it responsive to user selections and improving overall usability and interaction design.

#### Tasks

**Dynamic / Reactive Filters**

- Update price and area sliders dynamically based on:
  - selected districts
  - selected date range
- Ensure:
  - no impossible selections
  - no misleading ranges
- Maintain stability:
  - avoid excessive re-renders
  - ensure consistent behavior across pages

**District Filter UX Improvement**

- Improve district multiselect usability:
  - Add **“Select All” option** for quick full selection
  - Ensure behavior is intuitive and consistent with:
    - manual multi-selection
    - comparison mode override
- Clearly define interaction logic:
  - “Select All” = equivalent to selecting all districts
  - Should not conflict with Comparison Mode (which overrides filter)

**Filter Layout & UX Improvements**

- Improve sidebar organization:
  - Group filters into sections:
    - Location (district)
    - Time (date range)
    - Property (price, area)
- Add clear section labels for readability
- Improve spacing and visual clarity

**Default Value Optimization**

- Set smarter default filter values:
  - Recent date range (e.g. last 12 months)
  - Reasonable price and area bounds
- Ensure good “first impression” state when app loads

**State Clarity & Feedback**

- Ensure filter summary reflects:
  - dynamic slider ranges
  - district selection (including “All selected” state)
- Avoid ambiguity between:
  - “All selected manually”
  - “Comparison Mode active”

**Optional Enhancements (If Time Permits)**

- Top N district selector for comparison charts
- Sorting options:
  - average price
  - median price
  - transaction volume

#### Expected Outcome

- Filters feel **responsive, adaptive, and intuitive**
- Users can quickly:
  - select all districts
  - refine data without confusion
- Clear distinction between:
  - filtered views
  - comparison mode behavior
- Dashboard delivers a smoother, more polished product experience

---

### ⏳ Day 13 — District Ranking & Market Positioning

#### Objective

Introduce clear district-level rankings to help users quickly identify top and bottom performing areas based on key metrics.

#### Tasks

**District Aggregation Layer**

- Compute district-level metrics from filtered dataset:
  - average price per sqm
  - median price per sqm
  - transaction volume
- Ensure:
  - consistent use of `final_price_per_sqm`
  - aggregation respects active filters

**Ranking Table / Visualization**

- Build a ranking table or bar chart:
  - districts sorted by selected metric
- Allow sorting by:
  - average price per sqm
  - median price per sqm
  - transaction volume
- Display:
  - rank position
  - district name
  - selected metric value

**Top / Bottom Highlighting**

- Clearly highlight:
  - top N districts (e.g. top 5)
  - bottom N districts
- Optional:
  - use color or labels to distinguish tiers

**User Controls**

- Add simple controls:
  - metric selector (avg / median / volume)
  - optional: top N selector
- Ensure controls integrate smoothly with existing filters

**Integration with Existing Pages**

- Decide placement:
  - District Analysis page (recommended)
- Ensure:
  - no duplication of logic
  - consistent UI with other components

**Validation & Edge Cases**

- Handle:
  - small datasets (few districts)
  - ties in ranking
  - empty filtered data
- Ensure stable rendering across all filter states

#### Expected Outcome

- Users can quickly identify:
  - most expensive districts
  - most active districts
- Enhances decision-making by turning data into **clear rankings**
- Bridges gap between exploration and actionable insight

---

### ⏳ Day 14 — Map Visualization (Geographic Insight)

#### Objective

Introduce a geographic view of the data to enhance spatial understanding of pricing and transaction patterns.

#### Tasks

**Data Preparation**

- Aggregate district-level metrics:
  - average / median price per sqm
  - transaction volume
- Ensure alignment with:
  - active filters
  - ranking metrics (Day 13)

**GeoJSON Integration**

- Source Taiwan district-level GeoJSON dataset
- Map dataset districts to your `district` field:
  - handle naming inconsistencies if any
- Validate:
  - all districts correctly matched
  - no missing or misaligned regions

**Map Visualization (MVP)**

- Implement basic map using Streamlit-compatible library:
  - e.g. `st.pydeck_chart` or `plotly`
- Choose visualization approach:
  - Choropleth (recommended):
    - color intensity = price per sqm or volume
- Keep design simple and functional:
  - prioritize clarity over styling

**User Controls**

- Allow user to select metric displayed on map:
  - average price
  - median price
  - transaction volume
- Ensure consistency with:
  - Day 13 ranking metrics

**Tooltip & Interactivity**

- Add hover tooltip showing:
  - district name
  - selected metric value
- Optional:
  - include multiple metrics in tooltip

**Integration with Dashboard**

- Decide placement:
  - Overview page (high-level view) OR
  - District Analysis page (deeper analysis)
- Ensure:
  - consistent layout and sizing
  - no disruption to existing components

**Validation & Edge Cases**

- Handle:
  - missing geo data
  - unmatched districts
  - empty filtered dataset
- Ensure graceful fallback (e.g. message instead of map)

#### Expected Outcome

- Users gain **spatial understanding** of the market
- Enables:
  - quick identification of high/low price regions
  - geographic pattern recognition
- Significantly enhances dashboard’s analytical depth and product quality

---

## Phase 2 Completion Criteria

Phase 2 is considered complete when the dashboard:

### 1. Product Structure

- Has a **multi-page layout** with clear separation of:
  - overview
  - district analysis
  - transaction exploration

### 2. User-Focused Design

- Clearly targets a defined user group:
  - property analysts (primary)
  - property agents (secondary, future expansion)
- Supports key user questions:
  - Where is activity highest?
  - How are prices trending?
  - What are comparable transactions?

### 3. Analytical Capabilities

- Includes:
  - price trends over time
  - distribution analysis
  - district-level comparison
  - transaction volume metrics
  - median price (not just mean)

### 4. Interactivity

- Fully functional filtering:

  - district (multi-select)
  - date range
  - (optional) price / area filters

- All components respond consistently to filters

### 5. Core Features

- Transaction exploration table
- District ranking (price & volume)
- Basic map visualization (district-level)

### 6. Code Quality

- Modular and maintainable code structure
- Clear separation of:
  - data
  - logic
  - UI

### Final Outcome

A **functional analytical product MVP** that goes beyond visualization and supports decision-making for property agents.

---

# Future Work & Improvements (Post-MVP)

## Advanced Analytics

- Price growth analysis (month-over-month, year-over-year)
- District segmentation (high-end vs affordable areas)
- Volatility / stability indicators
- Outlier detection (overpriced / underpriced transactions)

## Enhanced Map Features

- Transaction-level map (point-based visualization)
- Heatmaps for price and volume
- Geographic clustering

## User Experience Improvements

- KPI cards with trend indicators (↑ ↓)
- Better layout and visual polish
- Improved loading performance

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

## Productization

- Deploy dashboard (Streamlit Cloud or similar)
- Add documentation and usage guide
- Improve README for portfolio presentation

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
