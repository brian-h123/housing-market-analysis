import streamlit as st

from utils.db import load_data

from components.filters_ui import render_filter_sidebar, render_filter_summary
from components.metrics import render_metrics
from components.charts import (
    plot_price_trend_bylevel,
    plot_district_comparison
)
from controllers.filter_controller import apply_filter_pipeline

import pandas as pd

def app():
    st.title("Overview Dashboard")
    st.info("Use the filters to explore overall housing trends.")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # Sidebar inputs
    base_filters = render_filter_sidebar(df)

    # Full pipeline
    filtered_df, filters = apply_filter_pipeline(df, base_filters)

    if filtered_df is None:
        return
    
    st.write("Filtered rows:", len(filtered_df))
    render_filter_summary(filters)

    # Metrics
    render_metrics(filtered_df)

    # High level trend
    st.subheader("Market Trend (Monthly)")
    st.pyplot(plot_price_trend_bylevel(filtered_df, 'Monthly'))

    # Quick Insight
    st.subheader("Quick District Snapshot")
    st.pyplot(plot_district_comparison(filtered_df))