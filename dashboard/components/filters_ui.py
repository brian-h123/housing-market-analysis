import streamlit as st
import pandas as pd

def render_filter_sidebar(df, comparison_mode=False):
    # Districts filter
    st.sidebar.header("📍 Location")

    districts = sorted(df['district'].unique())
    selected_districts = st.sidebar.multiselect(
        'District',
        districts,
        default=districts,
        disabled=comparison_mode
    )

    # Date filter
    st.sidebar.header("📅 Time")

    min_date = df['date'].min()
    max_date = df['date'].max()
    current_year = pd.Timestamp.today().year
    default_start = max(pd.Timestamp(f"{current_year}-01-01"), min_date)
    default_end = min(pd.Timestamp(f"{current_year}-12-31"), max_date)
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[default_start, default_end],
        min_value = min_date,
        max_value = max_date
    )

    return {
        'districts': selected_districts,
        'start_date': date_range[0],
        'end_date': date_range[1],
        'min_price': None,
        'max_price': None,
        'min_area': None,
        'max_area': None
    }

def render_filter_summary(filters):
    st.caption(f"""
    **Filters Applied:**
    - Districts: {', '.join(filters['districts']) if filters['districts'] else 'All'}
    - Date: {filters['start_date']} → {filters['end_date']}
    - Price: {filters['min_price']} → {filters['max_price']}
    - Area: {filters['min_area']} → {filters['max_area']}
    """)