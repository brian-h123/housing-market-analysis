import streamlit as st

from utils.db import load_data

from components.filters_ui import render_filter_sidebar, render_filter_summary
from components.sections import render_comparison_section
from controllers.filter_controller import apply_filter_pipeline

def app():
    st.title("District Analysis")
    st.caption("Compare pricing and transaction activity across districts")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    comparison_mode = st.toggle("Enable Comparison Mode", value=False)

    base_filters = render_filter_sidebar(df, comparison_mode)

    all_districts = sorted(df['district'].unique())

    if comparison_mode:
        active_filters = {
            **base_filters,
            'districts': all_districts
        }
    else:
        active_filters = base_filters

    filtered_df, filters = apply_filter_pipeline(df, active_filters)

    if filtered_df is None:
        return
    
    if comparison_mode:
        st.info("Comparison Mode Active: Showing all districts.")

    render_filter_summary(filters)
    render_comparison_section(filtered_df)