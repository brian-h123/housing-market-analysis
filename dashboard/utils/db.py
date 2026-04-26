import streamlit as st
from data.loader import load_data as base_load_data

DASHBOARD_COLUMNS = [
    'date',
    'district',
    'price',
    'area',
    'final_price_per_sqm',
    'building_type',
    'address'
]

@st.cache_data(ttl=600)
def load_data():
    df = base_load_data()

    df = df[DASHBOARD_COLUMNS]

    # Development Check (remove before production)
    assert df['final_price_per_sqm'].notna().all()
    assert df['area'].notna().all()

    return df