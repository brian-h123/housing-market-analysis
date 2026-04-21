import streamlit as st

from utils.db import load_data
from utils.filters import apply_filters, validate_filters

from components.filters import render_filter_sidebar
from components.sections import render_table

def app():
    st.title("Data Explorer")
    st.caption("Inspect individual transactions based on selected filters")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # Sidebar filters
    filters = render_filter_sidebar(df)

    # Validate inputs
    if not validate_filters(filters):
        return
    
    # Apply filters
    filtered_df = apply_filters(df, filters)

    render_table(filtered_df)