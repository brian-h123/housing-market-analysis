# Data Layer
import streamlit as st
import pandas as pd

# Filter Logic
def apply_filters(df, selected_districts, date_range, price_range, area_range):
    filtered = df[
        (df['district'].isin(selected_districts)) &
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1])) &
        (df['final_price_per_sqm'].between(price_range[0], price_range[1])) &
        (df['area'].between(area_range[0], area_range[1]))
    ]

    filtered = filtered.dropna(subset=['final_price_per_sqm', 'area'])

    return filtered

# Chart Functions
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # for Traditional Chinese
plt.rcParams['axes.unicode_minus'] = False

def plot_price_distribution(df):
    fig, ax = plt.subplots()
    ax.hist(df['final_price_per_sqm'], bins=50)
    ax.set_title("Price per sqm Distribution")
    ax.set_xlabel("Price per sqm")
    ax.set_ylabel("Frequency")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    return fig

def plot_district_comparison(df):
    #district_avg = df.groupby('district')['final_price_per_sqm'].mean().sort_values()
    district_stats = df.groupby('district').agg(
        avg_price_per_sqm = ('final_price_per_sqm', 'mean'),
        volume = ('district', 'count')
    ).sort_values(by='avg_price_per_sqm', ascending=True)
    fig, ax = plt.subplots()
    #district_avg.plot(kind='barh', ax=ax)
    district_stats['avg_price_per_sqm'].plot(kind='barh', ax=ax)
    for i, v in enumerate(district_stats['avg_price_per_sqm']):
        ax.text(v, i, f" ({district_stats['volume'].iloc[i]})")
    ax.set_title("Average Price per sqm by District")
    ax.set_xlabel("Price per sqm")
    ax.set_ylabel("Districts")
    return fig

def plot_price_trend_allinone(df):
    trend = df.groupby('date')['final_price_per_sqm'].mean()
    fig, ax = plt.subplots()
    trend.plot(ax=ax)
    trend.rolling(7).mean().plot(ax=ax, alpha=0.5)
    trend.rolling(30).mean().plot(ax=ax, alpha=0.5)
    ax.set_title("Price Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price per sqm")
    return fig

def plot_price_trend_bylevel(df, freq):
    if freq == 'Daily':
        trend = df.groupby('date')['final_price_per_sqm'].mean()
    elif freq == 'Weekly':
        trend = df.groupby(df['date'].dt.to_period('W'))['final_price_per_sqm'].mean()
        trend.index = trend.index.to_timestamp()
    elif freq == "Monthly":
        trend = df.groupby(df['date'].dt.to_period('M'))['final_price_per_sqm'].mean()
        trend.index = trend.index.to_timestamp()

    fig, ax = plt.subplots()
    trend.plot(ax=ax)
    ax.set_title(f"Price Trend ({freq})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price per sqm")
    return fig

# UI Sections
def render_sidebar(df):
    st.sidebar.header('Filters')

    # Districts filter
    districts = sorted(df['district'].unique())
    selected_districts = st.sidebar.multiselect(
        'District',
        districts,
        default=districts
    )

    # Date filter
    min_date = df['date'].min()
    max_date = df['date'].max()
    current_year = pd.Timestamp.today().year
    default_start = max(pd.Timestamp(f"{current_year}-01-01"), min_date)
    default_end = min(pd.Timestamp(f"{current_year}-12-31"), max_date)
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[default_start, default_end],
        min_value = min_date,
        max_value = max_date
    )

    # Price range filter
    min_price = int(df['final_price_per_sqm'].min())
    max_price = int(df['final_price_per_sqm'].max())
    rounded_min_price = int(math.floor(min_price / 10000) * 10000)
    rounded_max_price = int(math.ceil(max_price / 10000) * 10000)
    price_range = st.sidebar.slider(
        "Price per sqm range",
        min_value=rounded_min_price,
        max_value=rounded_max_price,
        value=(rounded_min_price, rounded_max_price),
        step=10000
    )

    # Area range slider
    min_area = int(df['area'].min())
    max_area = int(df['area'].max())
    area_range = st.sidebar.slider(
        "Area (sqm)",
        min_value= int(math.floor(min_area / 10) * 10),
        max_value= int(math.ceil(max_area / 10) * 10),
        value=(min_area, max_area),
        step=10
    )

    return selected_districts, date_range, price_range, area_range

def render_metrics(df):
    st.subheader('Key Metrics')

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Price / sqm", f"{df['final_price_per_sqm'].mean():,.0f}")
    col2.metric("Median Price / sqm", f"{df['final_price_per_sqm'].median():,.0f}")
    col3.metric("Transactions", len(df))

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

from utils.db import load_data

# Main App Flow
def main():
    st.title('Taiwan Housing Dashboard')
    st.info("Use the filters on the left to explore districts and time periods.")

    try:
        df = load_data()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

    # Sidebar
    selected_districts, date_range, price_range, area_range = render_sidebar(df)

    if len(date_range) != 2:
        st.warning("Please select a valid date range")
        return
    
    if not selected_districts:
        st.warning("Please select at least one district")
        return

    # Filtering
    filtered_df = apply_filters(df, selected_districts, date_range, price_range, area_range)

    if filtered_df.empty:
        st.warning('No data for selected filters')
        return

    st.caption(f"""
    Filtered Data:
    - Districts: {len(selected_districts)}
    - Date: {date_range[0]} -> {date_range[1]}
    - Price range{price_range}
    - Area range {area_range}
    - Transactions: {len(filtered_df)}
    """)
    
    # Key Metrics
    render_metrics(filtered_df)
    st.caption("Price per sqm excludes parking where applicable (net-adjusted pricing)")
    
    # Sections
    render_trend_section_allinone(filtered_df)
    render_trend_section_bylevel(filtered_df)
    render_distribution_section(filtered_df)
    render_comparison_section(filtered_df)

    if st.checkbox("Show transaction data"):
        render_table(filtered_df)

if __name__ == "__main__":
    main()