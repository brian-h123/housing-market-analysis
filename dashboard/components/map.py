import streamlit as st
import plotly.express as px
from utils.aggregation import get_district_aggregation
from utils.geo import load_geojson
from utils.metrics import METRIC_CONFIG

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
        options=list(METRIC_CONFIG.keys()),
        format_func=lambda x: METRIC_CONFIG[x]['label']
    )

    formatter = METRIC_CONFIG[metric_key]['format']
    metric_label = METRIC_CONFIG[metric_key]['label']

    agg_df['selected_metric'] = agg_df[metric_key].apply(formatter)

    volume_formatter = METRIC_CONFIG['transaction_volume']['format']
    agg_df['transaction_display'] = agg_df['transaction_volume'].apply(volume_formatter)

    fig = px.choropleth(
        agg_df,
        geojson=geojson,
        locations='district_normalized',
        featureidkey='properties.TOWNNAME',
        color=metric_key,
        hover_name='district',
        custom_data=['selected_metric', 'transaction_display'],
        color_continuous_scale='YlOrRd',
        labels={metric_key: metric_label}
    )

    fig.update_geos(
        fitbounds='locations',
        visible=False
    )

    fig.update_traces(
        marker_line_width=0.5,
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        f"{metric_label}: " + "%{customdata[0]}<br>" +
        "Transaction Volume: %{customdata[1]}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)