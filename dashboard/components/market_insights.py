from services.insight_service import InsightService
import streamlit as st

def render_district_insight(title, insights):
    st.subheader(title)

    if not insights:
        st.info("No insights available.")
        return

    for item in insights[:5]:
        district = item.get('district')

        with st.expander(f"📍 {district}"):
            label = item.get("label", "")
            explanation = item.get("explanation", "")
            metrics = item.get("metrics", {})

            st.markdown(f"""
            **📍 {district} — {label}**

            {explanation}

            **Key Metrics**
            - Mean Residual: {metrics.get('mean_residual'):,.0f}
            - Volatility: {metrics.get('volatility'):.2f}
            - Transactions: {metrics.get('transaction_count')}
            """)

def render_transaction_insight(title, insights):
    st.subheader(title)

    if not insights:
        st.info("No insights available.")
        return
    
    for item in insights[:5]:
        district = item.get('district')
        label = item.get('label', '')
        severity = item.get('severity', '')
        explanation = item.get('explanation', '')
        metrics = item.get('metrics', {})

        st.markdown(f"""
        **📍 {district} — {severity} {label}**
        
        {explanation}
        """)
        with st.expander(f"Key metrics"):
            st.markdown(f"""
            - Actual Price: {metrics.get('actual_price'):,.0f}
            - Predicted Price: {metrics.get('predicted_price'):,.0f}
            - Difference: {metrics.get('residual'):,.0f}
            - Percentage Difference: {metrics.get('pct_diff') * 100:.2f}%
            """)


def render_market_insights():
    st.header("🧠 Market Insights")
    st.caption("Interpret patterns behind pricing behavior using model-driven insights.")

    service = InsightService()

    st.subheader("🏙️ District Insights")
    district_data = service.get_district_insights()
    render_district_insight(
        "🔺 Overpriced Districts",
        district_data.get('overpriced', [])
    )
    render_district_insight(
        "🔻 Undervalued Districts",
        district_data.get('undervalued', [])
    )

    st.subheader("📍 Transaction-Level Insights")
    tx_data = service.get_transaction_insights()
    render_transaction_insight(
        "🔺 Most Overpriced Transactions",
        tx_data.get('overpriced', [])
    )
    render_transaction_insight(
        "🔻 Most Undervalued Transactions",
        tx_data.get('undervalued', [])
    )