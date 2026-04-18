import pandas as pd

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