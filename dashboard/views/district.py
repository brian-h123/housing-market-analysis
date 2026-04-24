import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

from components.filters_ui import render_filter_sidebar, render_filter_summary
from components.sections import render_market_activity_overview
from components.district_ranking import render_district_ranking
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

    # Comparison Mode input
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

    if guard_page_data(filtered_df):
        return
    
    if comparison_mode:
        st.info("Comparison Mode Active: Showing all districts.")

    render_filter_summary(
        filters, 
        all_districts, 
        comparison_mode=comparison_mode
    )
    
    render_market_activity_overview(filtered_df)
    render_district_ranking(filtered_df)