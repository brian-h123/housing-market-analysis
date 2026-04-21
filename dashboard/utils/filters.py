import pandas as pd
import streamlit as st

def apply_filters(df, filters):
    filtered_df = df.copy()
    
    # District filter
    if filters['districts']:
        filtered_df = filtered_df[
            filtered_df['district'].isin(filters['districts'])
        ]

    start_date = pd.to_datetime(filters["start_date"])
    end_date = pd.to_datetime(filters["end_date"])
    
    # Date filter
    filtered_df = filtered_df[
        (filtered_df['date'] >= start_date) &
        (filtered_df['date'] <= end_date)
    ]

    # Price filter
    filtered_df = filtered_df[
        (filtered_df["final_price_per_sqm"] >= filters["min_price"]) &
        (filtered_df["final_price_per_sqm"] <= filters["max_price"])
    ]

    # Area filter
    filtered_df = filtered_df[
        (filtered_df["area"] >= filters["min_area"]) &
        (filtered_df["area"] <= filters["max_area"])
    ]

    # Final safety cleanup
    filtered_df = filtered_df.dropna(subset=["final_price_per_sqm", "area"])

    return filtered_df

def validate_filters(filters, require_district=True):
    if not filters.get('start_date') or not filters.get('end_date'):
        st.warning('Please select a valid date range')
        return False

    if require_district and not filters.get('districts'):
        st.warning("Please select at least one district")
        return False
    
    return True