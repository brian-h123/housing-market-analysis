# Data Layer
import streamlit as st
import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "data", "taiwan_housing.db")

@st.cache_data(ttl=600)
def load_data():
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(
            'SELECT * FROM transactions', 
            conn,
            parse_dates=['date']
        )

# Filter Logic
def apply_filters(df, district, start_date, end_date):
    filtered = df[
        (df['district'] == district) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]
    return filtered

# Chart Functions
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # for Traditional Chinese
plt.rcParams['axes.unicode_minus'] = False

def plot_price_distribution(df):
    fig, ax = plt.subplots()
    ax.hist(df['final_price_per_sqm'], bins=50)
    ax.set_title("Price per sqm Distribution")
    return fig

def plot_district_comparison(df):
    district_avg = df.groupby('district')['final_price_per_sqm'].mean().sort_values()
    fig, ax = plt.subplots()
    district_avg.plot(kind='barh', ax=ax)
    ax.set_title("Average Price per sqm by District")
    return fig

def plot_price_trend(df):
    trend = df.groupby('date')['final_price_per_sqm'].mean()
    fig, ax = plt.subplots()
    trend.plot(ax=ax)
    ax.set_title("Price Trend Over Time")
    return fig

# UI Sections
def render_sidebar(df):
    st.sidebar.header('Filters')

    districts = sorted(df['district'].unique())
    selected_district = st.sidebar.selectbox('District', districts)

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

    return selected_district, date_range

def render_distribution_section(df):
    st.subheader('Distribution')
    fig = plot_price_distribution(df)
    st.pyplot(fig)

def render_comparison_section(df):
    st.subheader('District Comparison')
    fig = plot_district_comparison(df)
    st.pyplot(fig)

def render_trend_section(df):
    st.subheader('Trend')
    fig = plot_price_trend(df)
    st.pyplot(fig)

def render_table(df):
    st.subheader("Sample Transactions")
    display_df = df.copy()
    display_df['date'] = display_df['date'].dt.date

    st.dataframe(
        display_df[[
            'date',
            'district',
            'address',
            'price',
            'area',
            'final_price_per_sqm'
        ]].head(15)
    )

# Main App Flow
def main():
    st.title('Taiwan Housing Dashboard')

    df = load_data()

    # Sidebar
    selected_district, date_range = render_sidebar(df)
    start_date, end_date = date_range

    # Filtering
    filtered_df = apply_filters(df, selected_district, start_date, end_date)

    if filtered_df.empty:
        st.warning('No data for selected filters')
        return
    
    # Sections
    render_distribution_section(filtered_df)
    render_comparison_section(df)
    render_trend_section(filtered_df)

    if st.checkbox("Show transaction data"):
        render_table(filtered_df)

if __name__ == "__main__":
    main()