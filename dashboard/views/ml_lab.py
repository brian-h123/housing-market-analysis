import streamlit as st

from utils.db import load_data
from utils.ui_helpers import guard_page_data

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

    st.subheader("🧠 How the ML System Works")

    st.markdown("""
    This tool uses a machine learning model to estimate property prices and identify mispriced transactions.

    **Workflow:**
    - Prediction → Expected price
    - Residual → Difference from actual price
    - Z-score → Severity of mispricing
    - Insights → Interpretation of patterns

    **Model Used:**
    - Ridge Regression (chosen for stability and interpretability)

    **Key Price Drivers:**
    - Location (district)
    - Property size (area)
    - Building age
    """)

    st.header("Step 1 — Predict a Property")
    render_prediction_widget(df)

    st.divider()

    st.header("Step 2 — Compare with Market Transactions")
    render_anomaly_explorer(df)

    st.divider()

    st.header("Step 3 — Understand Insights")
    render_market_insights()

    st.divider()

    st.subheader("📏 Model Performance")

    st.write("""
    The model estimates property prices with a typical error of approximately ±18.6%.
    """)

    st.caption("""
    Predictions are generally close to actual prices, 
    but individual cases may vary depending on property characteristics.
    """)

    st.divider()

    st.subheader("✅ When to Trust the Model")

    st.write("""
    The model performs best under the following conditions:
    - Common property types (e.g. standard apartments)
    - High-transaction districts (more data available)
    - Typical property sizes and ages
    """)

    st.divider()

    st.subheader("⚠️ When to Be Cautious")

    st.write("""
    Predictions may be less reliable for:
    - Rare property types
    - Districts with low transaction volume
    - Extreme property sizes or unusual features
    """)

    st.divider()

    st.subheader("🧭 How to Use This Tool")

    st.write("""
    Use the system as a guide rather than an absolute answer:

    1. Start with a prediction → estimate expected price  
    2. Compare with anomaly cases → see how real transactions behave  
    3. Use insights → understand broader market patterns  
    """)