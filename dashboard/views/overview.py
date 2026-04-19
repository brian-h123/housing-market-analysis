import streamlit as st

from utils.db import load_data
from utils.filters import apply_filters

from components.filters import render_filter_sidebar
from components.metrics import render_metrics
from components.charts import (
    plot_price_trend_bylevel,
    plot_district_comparison
)

def app():
    st.title("Overview Dashboard")
    st.info("Use the filters to explore overall housing trends.")

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

    # Metrics
    render_metrics(filtered_df)

    # High level trend
    st.subheader("Market Trend (Monthly)")
    st.pyplot(plot_price_trend_bylevel(filtered_df, 'Monthly'))

    # Quick Insight
    st.subheader("Quick District Snapshot")
    st.pyplot(plot_district_comparison(filtered_df))