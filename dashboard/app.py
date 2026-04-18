from utils.db import load_data
from utils.filters import apply_filters
from components.filters import render_filter_sidebar
from components.metrics import render_metrics
from components.sections import (
    render_distribution_section,
    render_comparison_section,
    render_trend_section_allinone,
    render_trend_section_bylevel,
    render_table
)
import streamlit as st

# Main App Flow
def main():
    st.title('Taiwan Housing Dashboard')
    st.info("Use the filters on the left to explore districts and time periods.")

    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # Sidebar
    selected_districts, date_range, price_range, area_range = render_filter_sidebar(df)

    if len(date_range) != 2:
        st.warning("Please select a valid date range")
        return
    
    if not selected_districts:
        st.warning("Please select at least one district")
        return

    # Filtering
    filtered_df = apply_filters(df, selected_districts, date_range, price_range, area_range)

    if filtered_df.empty:
        st.warning('No data for selected filters')
        return

    st.caption(f"""
    Filtered Data:
    - Districts: {len(selected_districts)}
    - Date: {date_range[0]} -> {date_range[1]}
    - Price range{price_range}
    - Area range {area_range}
    - Transactions: {len(filtered_df)}
    """)
    
    # Key Metrics
    render_metrics(filtered_df)
    st.caption("Price per sqm excludes parking where applicable (net-adjusted pricing)")
    
    # Sections
    render_trend_section_allinone(filtered_df)
    render_trend_section_bylevel(filtered_df)
    render_distribution_section(filtered_df)
    render_comparison_section(filtered_df)

    if st.checkbox("Show transaction data"):
        render_table(filtered_df)

if __name__ == "__main__":
    main()