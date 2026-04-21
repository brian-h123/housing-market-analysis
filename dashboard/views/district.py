import streamlit as st

from utils.db import load_data
from utils.filters import apply_filters, validate_filters

from components.filters import render_filter_sidebar, render_filter_summary
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
    filters = render_filter_sidebar(df)

    comparison_mode = st.checkbox("Enable Comparison Mode")

    if comparison_mode:
        st.info("Comparison mode: showing all districts (district filter ignored)")
        # Apply all filters EXCEPT district
        active_filters = filters.copy()
        active_filters['districts'] = []
    else:
        active_filters = filters

    # Validate inputs
    if not validate_filters(active_filters, not comparison_mode):
        return

    # Apply filters
    district_df = apply_filters(df, active_filters)

    render_filter_summary(active_filters)
    render_comparison_section(district_df)