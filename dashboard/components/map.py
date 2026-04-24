import streamlit as st
import plotly.express as px
from utils.aggregation import get_district_aggregation, METRIC_MAP
from utils.geo import load_geojson

def filter_geojson_taipei(geojson):
    filtered_features = [
        feature for feature in geojson['features']
        if feature['properties']['COUNTYNAME'] == '台北市'
    ]

    return {
        'type': 'FeatureCollection',
        'features': filtered_features
    }


def render_map(df):
    st.subheader("Grographic Distribution")

    agg_df = get_district_aggregation(df)
    agg_df['district_normalized'] = agg_df['district'].str.strip()

    if agg_df.empty:
        st.warning("test No data available for current filters")
        return

    try:
        geojson = load_geojson()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    geojson =filter_geojson_taipei(geojson)

    metric_key = st.selectbox(
        'Select Metric',
        list(METRIC_MAP.keys())
    )

    metric_col = METRIC_MAP[metric_key]

    if metric_key != 'transaction_volume':
        agg_df['selected_metric'] = agg_df[metric_col].apply(
            lambda x: f"{x:,.0f} TWD"
        )
    else:
        agg_df['selected_metric'] = agg_df[metric_col].apply(
            lambda x: f"{x:,}"
        )

    agg_df['transaction_display'] = agg_df['transaction_volume'].apply(
        lambda x: f"{x:,}"
    )

    fig = px.choropleth(
        agg_df,
        geojson=geojson,
        locations='district_normalized',
        featureidkey='properties.TOWNNAME',
        color=metric_col,
        hover_name='district',
        hover_data={
            'selected_metric': True,
            'transaction_display': True,
            metric_col: False,
            'transaction_volume': False,
            'district_normalized': False,
            'avg_price_per_sqm': False,
            'median_price_per_sqm':False
        },
        labels={
            metric_col: metric_key,
            'selected_metric': metric_key,
            'transaction_volume': 'Transaction Volume',
            'transaction_display': 'Transaction Volume'
        },
        color_continuous_scale='Blues'
    )

    fig.update_geos(
        fitbounds='locations',
        visible=False
    )

    fig.update_traces(marker_line_width=0.5)

    st.plotly_chart(fig, use_container_width=True)