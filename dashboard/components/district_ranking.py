import streamlit as st
import plotly.express as px

from utils.aggregation import (
    get_district_aggregation,
    rank_districts
)
from utils.metrics import METRIC_CONFIG

def render_district_ranking(df):
    st.subheader("📊 District Ranking")

    # Metric selector
    metric_key = st.selectbox(
        "Ranking Metric",
        options=list(METRIC_CONFIG.keys()),
        format_func=lambda x: METRIC_CONFIG[x]['label']
    )

    if df.empty:
        st.warning("No data available for selected filters")
        return
    
    # Aggregation + ranking
    agg_df = get_district_aggregation(df)
    ranked_df = rank_districts(agg_df, metric_key)

    formatter = METRIC_CONFIG[metric_key]['format']
    metric_label = METRIC_CONFIG[metric_key]['label']

    ranked_df['selected_metric'] = ranked_df[metric_key].apply(formatter)

    # Chart
    fig = px.bar(
        ranked_df,
        x=metric_key,
        y='district',
        orientation='h',
        title=f"District Ranking by {metric_label}",
        hover_name='district',
        custom_data=['selected_metric'],
        labels={metric_key: metric_label}
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        yaxis_title='District'
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        f"{metric_label}: " + "%{customdata[0]}<br>"
    )

    st.plotly_chart(fig, use_container_width=True)