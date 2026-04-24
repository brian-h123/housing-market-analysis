import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

from components.filters_ui import render_filter_sidebar, render_filter_summary
from components.metrics import render_metrics
from components.sections import (
    render_quick_insight,
    render_quick_trend
)
from components.map import render_map
from controllers.filter_controller import apply_filter_pipeline

def app():
    st.title("Overview Dashboard")
    st.info("Use the filters to explore overall housing trends.")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    all_districts = sorted(df["district"].unique())

    # Sidebar inputs
    base_filters = render_filter_sidebar(df)

    # Full pipeline
    filtered_df, filters = apply_filter_pipeline(df, base_filters)

    if guard_page_data(filtered_df):
        return
    
    st.write("Filtered rows:", len(filtered_df))
    render_filter_summary(filters, all_districts)

    # Metrics
    render_metrics(filtered_df)

    # Map insight
    render_map(filtered_df)

    # High level trend
    render_quick_trend(filtered_df)

    # Quick Insight
    render_quick_insight(filtered_df)