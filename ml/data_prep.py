from data.loader import load_data
from ml.features import (
    add_ml_features,
    engineer_features,
    encode_features
)

TARGET = 'final_price_per_sqm'
BASE_FEATURES = [
    'area',
    'main_area',
    'net_area',
    'district',
    'building_type',
    'date',
    'parking_area',
    'total_floors_raw',
    'floor_info_raw',
    'building_year_raw'
]
MODEL_COLUMNS = [TARGET] + BASE_FEATURES

def load_modeling_data():
    df = load_data()
    return df[MODEL_COLUMNS]

def clean_modeling_data(df):
    df = df.dropna(subset=[
        'final_price_per_sqm',
        'area',
        'district',
        'building_type'
    ])

    df = df[df['area'] > 0]
    df = df[df['final_price_per_sqm'] > 0]

    df['district'] = df['district'].astype(str)
    df['building_type'] = df['building_type'].astype(str)

    df = df.reset_index(drop=True)

    return df

def filter_modeling_data(df):
    df = df.copy()

    df = df.dropna(subset=['floor_level'])

    return df

def select_features(df):
    FINAL_FEATURES = [
        'final_price_per_sqm',
        'area',
        'main_area',
        'net_area',
        'parking_area',
        'total_floors',
        'floor_level',
        'building_year',
        'building_age',
        'transaction_year',
        'transaction_month',
        'area_ratio',
        'time_index',
        'log_area',
        'has_parking',
        # 'building_age_missing',
        'district',
        'building_type'
    ]
    df = df[FINAL_FEATURES]
    return df

def prepare_dataset():
    df = load_modeling_data()

    df = clean_modeling_data(df)

    df = add_ml_features(df)
    df = engineer_features(df)

    df = filter_modeling_data(df)

    df = select_features(df)

    df = encode_features(df)
    return df

# def main():
#     print('loading data')
#     df = prepare_dataset()

#     print(df.info())

# if __name__ == '__main__':
#     main()