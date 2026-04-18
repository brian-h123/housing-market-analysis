import streamlit as st
from .charts import (
    plot_price_distribution,
    plot_district_comparison,
    plot_price_trend_allinone,
    plot_price_trend_bylevel
)

def render_distribution_section(df):
    st.subheader('Price Distribution')
    st.caption("Shows spread of transaction prices within selected filters")
    fig = plot_price_distribution(df)
    st.pyplot(fig)

def render_comparison_section(df):
    st.subheader('District Comparison')
    st.caption("Average price per sqm by district (numbers in brackets = transaction count)")
    fig = plot_district_comparison(df)
    st.pyplot(fig)

def render_trend_section_allinone(df):
    st.subheader('Price Trend (Daily + Smoothed)')
    fig = plot_price_trend_allinone(df)
    st.pyplot(fig)

def render_trend_section_bylevel(df):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Price Trend Over Time")

    with col2:
        freq = st.selectbox(
            "Granularity",
            ['Daily', 'Weekly', 'Monthly']
        )

    fig = plot_price_trend_bylevel(df, freq)
    st.pyplot(fig)

def render_table(df):
    st.subheader("Sample Transactions")
    st.caption("Showing most recent transactions based on selected filters")
    display_df = df.copy()
    display_df['date'] = display_df['date'].dt.date
    display_df = display_df.sort_values('date', ascending=False).reset_index(drop=True)

    display_df = display_df[[
        'date',
        'building_type',
        'district',
        'address',
        'price',
        'area',
        'final_price_per_sqm'
    ]]

    csv = display_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="Download data as csv",
        data=csv,
        file_name="filtered_transactions.csv",
        mime="text/csv"
    )

    st.dataframe(display_df.head(15))