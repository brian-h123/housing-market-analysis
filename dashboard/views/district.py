import streamlit as st

from utils.db import load_data
from utils.filters import apply_filters

from components.filters import render_filter_sidebar
from components.sections import render_comparison_section

def app():
    st.title("District Analysis")
    st.caption("Compare pricing and transaction activity across districts")

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

    render_comparison_section(filtered_df)