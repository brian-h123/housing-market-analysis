import streamlit as st

def handle_empty_data(df, message="No data available for selected filters"):
    if df.empty:
        st.warning(message)
        return True
    return False

def guard_page_data(df):
    if df is None:
        return True
    
    if handle_empty_data(df, "No results from the filter selection"):
        return True
    
    return False