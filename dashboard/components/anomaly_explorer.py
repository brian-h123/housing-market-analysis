import streamlit as st

from services.anomaly_service import AnomalyExplorer

def render_anomaly_explorer(df):
    st.subheader("🚨 Market Anomalies")

    districts = sorted(df['district'].unique())
    selected_districts = st.multiselect(
        "District",
        districts,
        default=districts
    )

    z_threshold = st.slider(
        "Minimum anomaly severity (|z-score|)",
        min_value=0.0,
        max_value=5.0,
        value=2.0,
        step=0.1
    )

    anomaly_type = st.selectbox(
        "Anomaly Type",
        ['All', 'Overpriced', 'Undervalued']
    )

    input_data = {
        'districts': selected_districts,
        'z_threshold': z_threshold,
        'anomaly_type': anomaly_type
    }

    service = AnomalyExplorer()
    result = service.filter(input_data)

    st.write(f"Showing {len(result)}")

    st.dataframe(
        result[[
            'district', 
            'actual_price', 
            'predicted_price', 
            'residual', 
            'residual_z', 
            'anomaly_flag'
        ]].sort_values('residual_z', ascending=False)
    )