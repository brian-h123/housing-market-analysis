import streamlit as st

def app():
    st.title("📊 Key Market Insights")

    st.caption("""
    A summary of key findings derived from pricing models, anomaly detection, and transaction data.
    """)

    with st.container():
        st.subheader("📍 Location is the strongest driver of price")

        st.write("""
        Property prices are primarily driven by district-level location effects. 
        Premium districts such as 大安區, 信義區, and 中正區 consistently show the strongest positive influence on price, 
        while districts like 北投區, 萬華區, and 文山區 are associated with lower pricing levels.
        """)

        st.caption("""
        Model coefficients show clear separation between high-end and lower-priced districts, 
        indicating that location alone explains a significant portion of price variation.
        """)

    with st.container():
        st.subheader("⚖️ The market contains measurable mispricing")

        st.write("""
        Approximately 4.7% of transactions are flagged as significant anomalies, 
        with pricing deviations exceeding ±2 standard deviations from model expectations.
        """)

        st.caption("""
        Residual z-scores range from -2.5 to +3.85, indicating that some properties are priced far above or below 
        what the model considers reasonable based on their features.
        """)

    with st.container():
        st.subheader("🔴 Premium districts show consistent overpricing")

        st.write("""
        High-end districts such as 松山區, 信義區, and 大安區 exhibit consistently positive residuals, 
        indicating that transactions in these areas are often priced above model expectations.
        """)

        st.caption("""
        This suggests a location-driven premium beyond what can be explained by observable features, 
        potentially reflecting brand value, demand pressure, or buyer sentiment.
        """)

    with st.container():
        st.subheader("🟢 Certain districts show signs of undervaluation")

        st.write("""
        Districts such as 南港區, 萬華區, and 內湖區 tend to have negative residuals, 
        indicating that properties are often priced below model expectations.
        """)

        st.caption("""
        These areas may represent relative value opportunities where prices are lower than what comparable features would suggest.
        """)

    with st.container():
        st.subheader("📊 Pricing consistency varies across districts")

        st.write("""
        Some districts, such as 南港區 and 大同區, show high variability in pricing behavior, 
        with large standard deviations in residuals.
        """)

        st.caption("""
        This indicates less consistent pricing and potentially higher uncertainty, 
        where similar properties may be priced very differently.
        """)

    with st.container():
        st.subheader("⚠️ Extreme mispricing is concentrated in specific districts")

        st.write("""
        The most extreme pricing deviations reach up to +3.85 standard deviations (undervalued) 
        and -2.5 standard deviations (overpriced), indicating substantial mispricing in certain cases.
        """)

        st.caption("""
        Among the top anomaly cases, 中正區 appears disproportionately often, suggesting that 
        even within premium areas, pricing can vary significantly across transactions.
        """)