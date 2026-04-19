import streamlit as st

from utils.db import load_data
from utils.filters import apply_filters

from components.filters import render_filter_sidebar
from components.sections import render_trend_section_allinone, render_trend_section_bylevel

def app():
    st.title("Market Trends")
    st.caption("Analyze how prices change over time")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # Sidebar filters
    selected_districts, date_range, price_range, area_range = render_filter_sidebar(df)

    # Validate inputs
    if len(date_range) != 2:
        st.warning("Please select a valid date range")
        return
    
    if not selected_districts:
        st.warning("Please select at least one district")
        return
    
    # Apply filters
    filtered_df = apply_filters(
        df,
        selected_districts,
        date_range,
        price_range,
        area_range
    )

    render_trend_section_allinone(filtered_df)
    render_trend_section_bylevel(filtered_df)