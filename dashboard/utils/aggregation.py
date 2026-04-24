from .metrics import METRIC_CONFIG

METRIC_MAP = {
    'Average Price per SQM': 'avg_price_per_sqm',
    'Median Price per SQM': 'median_price_per_sqm',
    'Transaction Volume': 'transaction_volume'
}

def get_district_aggregation(df):
    agg_df = (
        df.groupby('district')
        .agg(
            avg_price_per_sqm=('final_price_per_sqm', 'mean'),
            median_price_per_sqm=('final_price_per_sqm', 'median'),
            transaction_volume=('district','count')
        ).reset_index()
    )

    agg_df['avg_price_per_sqm'] = agg_df['avg_price_per_sqm'].round(0)
    agg_df['median_price_per_sqm'] = agg_df['median_price_per_sqm'].round(0)

    return agg_df

def rank_districts(agg_df, metric_key):

    return (
        agg_df.sort_values(by=metric_key, ascending=False)
        .reset_index(drop=True)
    )