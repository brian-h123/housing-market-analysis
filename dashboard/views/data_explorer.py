import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

from components.filters_ui import render_filter_sidebar, render_filter_summary
from components.sections import render_table
from controllers.filter_controller import apply_filter_pipeline

def app():
    st.title("Data Explorer")
    st.caption("Inspect individual transactions based on selected filters")

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

    render_filter_summary(filters, all_districts)
    render_table(filtered_df)