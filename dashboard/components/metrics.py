import streamlit as st

def render_metrics(df):
    st.subheader('Key Metrics')

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Price / sqm", f"{df['final_price_per_sqm'].mean():,.0f}")
    col2.metric("Median Price / sqm", f"{df['final_price_per_sqm'].median():,.0f}")
    col3.metric("Transactions", len(df))