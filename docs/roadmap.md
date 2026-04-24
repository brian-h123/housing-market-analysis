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

### ✅ Day 12 — Smart Filtering (Responsiveness & UX) (Completed)

#### Objective

Enhance filtering experience by making it responsive to user selections and improving overall usability and interaction design.

#### Completed

**Reactive / Dynamic Filters**

- Implemented dynamic price and area sliders that adjust based on:
  - selected districts
  - selected date range
- Ensured:
  - no invalid or impossible selections
  - filter ranges always reflect the current dataset
- Maintained stability by controlling re-renders and preserving consistent behavior across pages

**Hierarchical Filtering System**

- Redesigned sidebar filters into a **hierarchical structure**:
  - upstream filters (district, date) influence downstream filters (price, area)
- Established clear dependency flow:
  - district → date → price / area
- Improved logical consistency and prevented misleading filter combinations

**District Filter UX Improvements**

- Added **“Select All” option** for district multiselect
- Standardized behavior:
  - “Select All” = equivalent to selecting all districts
  - Manual selection and “Select All” remain consistent
- Ensured compatibility with:
  - Comparison Mode (override still works as intended)

**Filter Layout & Organization**

- Grouped sidebar filters into clear sections:
  - Location (district)
  - Time (date range)
  - Property (price, area)
- Improved spacing and labeling for better readability
- Created a more intuitive and structured user experience

**Filter State Clarity & Feedback**

- Updated filter summary to reflect:
  - dynamic slider ranges
  - district selection (including “All selected” state)
- Clarified distinction between:
  - manual “all districts selected”
  - Comparison Mode override
- Improved transparency of current filter state

**Validation & Stability**

- Tested filter behavior across:
  - different district selections
  - varying date ranges
  - edge cases (narrow ranges, near-empty datasets)
- Ensured:
  - no inconsistencies between filters and displayed data
  - no regression in existing functionality

#### Key Outcome

- Filtering system is now **responsive, structured, and intuitive**
- Users experience:
  - smoother interactions
  - clearer filter logic
  - reduced confusion from invalid selections
- Dashboard achieves a more **polished, product-level UX**, especially for multi-dimensional filtering workflows

---

### ✅ Day 13 — District Ranking & Market Positioning (Completed)

#### Objective

Introduce clear district-level rankings to help users quickly identify top and bottom performing areas based on key metrics.

#### Completed

**District Aggregation Layer**

- Built a reusable district-level aggregation pipeline based on the filtered dataset
- Computed key metrics per district:
  - Average price per sqm (`mean`)
  - Median price per sqm
  - Transaction volume (count)
- Ensured aggregation is fully aligned with:
  - `final_price_per_sqm`
  - Active filters (district, date, price, area)
- Structured output as a consistent dataframe for reuse across ranking and visualization components

**Ranking Visualization (Core MVP)**

- Implemented a district ranking view (table / bar chart)
- Default sorting:
  - Descending by average price per sqm
- Displayed key ranking information:
  - District name
  - Selected metric value
- Ensured ranking dynamically updates based on:
  - filtered dataset
  - selected metric

**Metric Selection (Core Control Feature)**

- Added metric selector for ranking view:
  - Average price per sqm
  - Median price per sqm
  - Transaction volume
- Implemented dynamic re-sorting based on selected metric
- Ensured consistent formatting across all metric types

**Integration with District Analysis Page**

- Integrated ranking section into the District Analysis page
- Positioned ranking below comparison visualizations for logical flow:
  - comparison → ranking → insights
- Ensured no duplication of aggregation logic by reusing shared pipeline

**Validation & Edge Case Handling**

- Handled edge cases:
  - Very small datasets (few districts)
  - Tied metric values across districts
  - Empty filtered results
- Added fallback UI for empty states:
  - “No data available for current filters”
- Verified stability across all filter combinations

#### Key Outcome

- Users can now clearly identify:

  - Most expensive districts
  - Most active districts by transaction volume
  - Relative positioning of districts across multiple metrics

- Transforms raw aggregated data into a **clear, decision-oriented ranking system**

- Establishes a foundation for future enhancements such as:
  - geographic visualization (Day 14 map integration)

---

### ✅ Day 14 — Map Visualization (Geographic Insight) (Completed)

#### Objective

Introduce a geographic view of district-level metrics to enhance spatial understanding of pricing and transaction patterns.

Builds directly on the **district aggregation layer from Day 13**.

#### Completed

**Reuse of District Aggregation Layer**

- Reused district-level aggregated dataset:
  - Average price per sqm
  - Median price per sqm
  - Transaction volume
- Ensured full consistency between:
  - Ranking values (Day 13)
  - Map visualization values (Day 14)
- Maintained single source of truth for district metrics

**GeoJSON Integration**

- Sourced Taiwan district-level GeoJSON dataset
- Mapped GeoJSON regions to dataset `district` field
- Handled naming alignment between:
  - GeoJSON regions
  - Transaction dataset districts
- Validated:
  - All districts correctly matched
  - No missing or misaligned regions in final map

**Choropleth Map Implementation**

- Implemented district-level choropleth map on Overview page
- Color encoding:
  - Intensity represents selected metric value
- Default metric:
  - Average price per sqm
- Ensured map updates dynamically based on:
  - active filters
  - selected metric

**Metric Selector (Shared with Ranking Logic)**

- Added metric selector for map:
  - Average price per sqm
  - Median price per sqm
  - Transaction volume
- Reused same selection logic as Day 13 ranking
- Ensured consistent formatting and behavior across metrics

**Tooltip & Interactivity**

- Implemented hover tooltip displaying:
  - District name
  - Selected metric value
  - Transaction volume
- Improved readability:
  - Applied number formatting (commas / currency where applicable)
- Ensured tooltip reflects current metric selection dynamically

**Integration with Overview Page**

- Integrated map into Overview page as a high-level insight component
- Positioned map to support:
  - quick spatial understanding before deeper analysis
- Ensured no duplication with:
  - District Analysis ranking view

**Validation & Edge Case Handling**

- Handled:
  - empty filtered dataset (graceful fallback UI)
  - potential GeoJSON mismatches
- Verified stability across:
  - different filter combinations
  - metric selections
- Ensured no regression in:
  - filtering logic
  - aggregation consistency

#### Key Outcome

- Users can now visually explore **spatial distribution of housing metrics**
- Enables:
  - Immediate identification of high / low value regions
  - Geographic validation of district rankings (Day 13)
- Adds a critical **geographic dimension** to the dashboard
- Establishes a strong foundation for future spatial enhancements
  - heatmaps
  - clustering
  - transaction-level mapping

---

### ✅ Day 15 — Final Dashboard Polish (UX & Consistency) (Completed)

#### Objective

Apply final usability and visual refinements to:

- District ranking system (Day 13)
- Map visualization (Day 14)

Focus on improving **clarity, consistency, and overall user experience**, completing the Phase 2 MVP.

#### Completed

**Metric Standardization**

- Standardized formatting across all components:
  - Applied consistent number formatting (commas, currency where appropriate)
  - Ensured uniform display of:
    - price-based metrics
    - transaction volume
- Aligned metric definitions between:
  - map visualization
  - ranking system
- Eliminated discrepancies between displayed values across components

**Map Visualization Improvements**

- Refined choropleth presentation:
  - Improved color scale readability and interpretability
- Improved tooltip formatting:
  - Clear display of:
    - district name
    - selected metric value
    - transaction volume
  - Consistent formatting with other components

**District Analysis Transformation**

- Replaced previous **district comparison chart** with a more meaningful **Market Activity Overview**
- Shifted focus from redundant comparisons to:
  - clearer representation of district-level activity
  - better alignment with ranking and map insights
- Reduced duplication between:
  - comparison chart
  - district ranking visualization

**UX & Visual Consistency**

- Improved consistency across pages:
  - Overview (map)
  - District Analysis (ranking & activity overview)
- Ensured coherent analytical flow:
  - Overview → spatial insight
  - District Analysis → detailed breakdown
- Cleaned up redundant or overlapping visual elements

**Validation & Stability**

- Verified consistency across:
  - different metric selections
  - various filter combinations
- Tested edge cases:
  - small datasets
  - extreme filter ranges
  - empty states
- Ensured:
  - no broken visuals
  - consistent behavior across all components

#### Key Outcome

- Dashboard achieves a **polished MVP standard**
- Map and district analysis now function as a **cohesive analytical system**
- Visualizations are:
  - clearer
  - more consistent
  - more aligned with user workflows
- Redundant components removed, improving overall usability and focus

---

## ✅ Phase 2 Summary — From Analysis to Product

Phase 2 successfully transforms the project from exploratory analysis into a **functional, user-focused analytical dashboard**.

### What Was Achieved

- Built a **multi-page Streamlit dashboard** with clear structure:

  - Overview (spatial insights via map)
  - District Analysis (ranking & market activity)
  - Trends (time-based analysis)
  - Data Explorer (transaction-level data)

- Implemented a **robust and consistent filtering system**:

  - District, date, price, and area filters
  - Reactive and hierarchical filtering logic
  - Clear user feedback and edge case handling

- Developed **core analytical features**:

  - District-level aggregation (mean, median, volume)
  - Ranking system for market comparison
  - Time-series trend analysis
  - Distribution visualizations

- Introduced **geographic visualization**:

  - Choropleth map for spatial understanding of market patterns
  - Fully aligned with ranking metrics and filters

- Achieved **UX and visual consistency**:
  - Standardized metric formatting across all components
  - Removed redundant visuals and improved clarity
  - Established a logical analytical flow across pages

### Key Outcome

- The project is now a **polished MVP analytical product**
- Users can:

  - Explore market trends
  - Compare districts
  - Identify high-activity areas
  - Validate transaction-level data

- The codebase is **modular, scalable, and ready for future enhancements**

---

**Phase 2 Conclusion:**

A complete transition from **data analysis → interactive analytical tool**, delivering real value for property analysts.

---

# Future Work & Improvements (Post-MVP)

With Phase 2 complete, the project has reached a functional and polished MVP.

Future work will focus on expanding:

- analytical depth
- data coverage
- user experience
- product readiness

---

## 1. Dashboard & UX Enhancements

### Ranking Improvements

- Top N / Bottom N toggle for district ranking
- Sorting controls:
  - ascending / descending toggle
- Optional highlighting:
  - emphasize top-performing districts
- Improve ranking readability for large district lists

### Map Enhancements

- Transaction-level map (point-based visualization)
- Heatmaps:
  - price intensity
  - transaction volume density
- Geographic clustering of transactions
- Drill-down capability:
  - click district → view detailed breakdown

### New Visualizations

- Price growth charts:
  - month-over-month (MoM)
  - year-over-year (YoY)
- Volatility indicators:
  - price stability / variance by district
- Distribution comparisons:
  - side-by-side district boxplots
- Outlier detection visuals:
  - highlight overpriced / underpriced transactions

### UX & Interaction Improvements

- KPI cards with trend indicators (↑ ↓)
- Improved layout and visual hierarchy
- Better loading and performance optimization
- Enhanced filter UX (e.g. presets, quick selections)

---

## 2. Advanced Analytics

- District segmentation:
  - high-end vs mid-tier vs affordable areas
- Price momentum analysis:
  - identifying fast-growing districts
- Comparative analysis:
  - benchmark districts against each other
- Anomaly detection:
  - identify unusual or inconsistent transactions

---

## 3. Data & Model Expansion

### Data Enrichment

- Integrate external datasets:
  - MRT / transport proximity
  - demographics
  - amenities (schools, malls, etc.)
- Enhance spatial context for deeper analysis

### Data Model Expansion

Current dataset is scoped to **housing transactions only**.

Future expansion may include:

- housing
- land
- parking

#### Challenges

- Different transaction types require different metrics:
  - housing → price per sqm
  - land → price per land area
  - parking → price per unit
- Current pricing logic is not directly transferable

#### Potential Approaches

- Split dataset by transaction type
- Introduce normalized schema
- Build type-specific analytical views

---

## 4. Productization & Deployment

- Deploy dashboard (e.g. Streamlit Cloud)
- Add user documentation / usage guide
- Improve README for portfolio presentation
- Optimize performance and data loading
- Prepare project for real-world usage and sharing

---

## 5. Future User Segments

### Property Buyers

- affordability insights
- recent comparable transactions
- localized price trends

### Investors

- high-growth districts
- emerging areas
- price momentum indicators

### Analysts / Developers

- deeper statistical tools
- clustering and segmentation models
- long-term trend analysis

---
