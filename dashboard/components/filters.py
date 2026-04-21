import math
import streamlit as st
import pandas as pd

def render_filter_sidebar(df):
    st.sidebar.header('Filters')

    # Districts filter
    districts = sorted(df['district'].unique())
    selected_districts = st.sidebar.multiselect(
        'District',
        districts,
        default=districts
    )

    # Date filter
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

    # Price range filter
    min_price = int(df['final_price_per_sqm'].min())
    max_price = int(df['final_price_per_sqm'].max())
    rounded_min_price = int(math.floor(min_price / 10000) * 10000)
    rounded_max_price = int(math.ceil(max_price / 10000) * 10000)
    price_range = st.sidebar.slider(
        "Price per sqm range",
        min_value=rounded_min_price,
        max_value=rounded_max_price,
        value=(rounded_min_price, rounded_max_price),
        step=10000
    )

    # Area range slider
    min_area = int(df['area'].min())
    max_area = int(df['area'].max())
    rounded_min_area = int(math.floor(min_area / 10) * 10)
    rounded_max_area = int(math.ceil(max_area / 10) * 10)
    area_range = st.sidebar.slider(
        "Area (sqm)",
        min_value= rounded_min_area,
        max_value= rounded_max_area,
        value=(rounded_min_area, rounded_max_area),
        step=10
    )

    return {
        'districts': selected_districts,
        'start_date': date_range[0],
        'end_date': date_range[1],
        'min_price': price_range[0],
        'max_price': price_range[1],
        'min_area': area_range[0],
        'max_area': area_range[1]
    }

def render_filter_summary(filters):
    st.caption(f"""
    **Filters Applied:**
    - Districts: {', '.join(filters['districts']) if filters['districts'] else 'All'}
    - Date: {filters['start_date']} → {filters['end_date']}
    - Price: {filters['min_price']} → {filters['max_price']}
    - Area: {filters['min_area']} → {filters['max_area']}
    """)