import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

from components.filters_ui import render_filter_sidebar, render_filter_summary

from components.prediction import render_prediction_widget
from components.anomaly_explorer import render_anomaly_explorer

def app():
    st.title("ML Lab")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # render_prediction_widget(df)

    render_anomaly_explorer(df)