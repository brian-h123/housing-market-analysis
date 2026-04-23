import streamlit as st
import plotly.express as px

from utils.aggregation import (
    compute_district_metrics,
    rank_districts,
    METRIC_MAP
)

def render_district_ranking(df):
    st.subheader("📊 District Ranking")

    # Metric selector
    metric_key = st.selectbox(
        "Ranking Metric",
        list(METRIC_MAP.keys())
    )

    if df.empty:
        st.warning("No data available for selected filters")
        return
    
    # Aggregation + ranking
    agg_df = compute_district_metrics(df)
    ranked_df = rank_districts(agg_df, metric_key)

    metric_col = METRIC_MAP[metric_key]

    # Chart
    fig = px.bar(
        ranked_df,
        x=metric_col,
        y='district',
        orientation='h',
        title=f"District Ranking by {metric_key}"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig, use_container_width=True)