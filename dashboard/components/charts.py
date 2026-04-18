from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

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