import streamlit as st

from services.ml_service import PredictionService

def render_prediction_widget(df, show_debug=False):
    st.subheader("🏠 Price Prediction Simulator")
    st.caption("Estimate the expected pprice per sqm based on property features.")

    with st.form('prediction form'):
        district = st.selectbox(
            'District',
            options=sorted(df['district'].unique())
        )

        building_type = st.selectbox(
            'Building Type',
            options=sorted(df['building_type'].unique())
        )

        area = st.number_input(
            'Area (sqm)',
            min_value=5.0,
            max_value=500.0,
            value=30.0,
            step=1.0
        )

        building_age = st.number_input(
            'Building Age (years)',
            min_value=0,
            max_value=100,
            value=10
        )

        submitted = st.form_submit_button('Predict Price')

    if submitted:
        input_data = {
            'district': district,
            'building_type': building_type,
            'area': area,
            'building_age': building_age
        }

        service = PredictionService()
        result = service.predict(input_data)

        st.metric(
            'Predicted Price (per sqm)',
            f"{result['predicted_price_per_sqm']:,.0f}"
        )

        if show_debug:
            with st.expander("Debug Info"):
                st.write("Input:", input_data)
                st.write("Result:", result)
        
        return result
    
    return None
