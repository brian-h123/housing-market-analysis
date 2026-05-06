import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

from components.filters_ui import render_filter_sidebar, render_filter_summary

from components.prediction import render_prediction_widget
from components.anomaly_explorer import render_anomaly_explorer
from components.market_insights import render_market_insights

def app():
    st.title("ML Lab")

    # Load data
    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    tab1, tab2, tab3 = st.tabs(['Prediction Simulator', 'Anomaly Explorer', 'Insights'])

    with tab1:
        render_prediction_widget(df)
    with tab2:
        render_anomaly_explorer(df)
    with tab3:
        render_market_insights()