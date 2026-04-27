import numpy as np
import pandas as pd
import re

def chinese_to_int(s):
    mapping ={
        '一':1, '二':2, '三':3, '四':4, '五':5,
        '六':6, '七':7, '八':8, '九':9
    }
    
    if s == '十':
        return 10
    elif '十' in s:
        parts = s.split('十')
        tens = mapping.get(parts[0], 1) if parts[0] != '' else 1
        ones = mapping.get(parts[1], 0) if len(parts) > 1 else 0
        return tens * 10 + ones
    else:
        return mapping.get(s, None)

def extract_floors(text):
    if pd.isna(text):
        return []

    matches = re.findall(r'[一二三四五六七八九十]+', str(text))
    return [chinese_to_int(m) for m in matches if chinese_to_int(m) is not None]

def process_total_floors(df):
    def parse(x):
        try:
            x = str(x).replace('層', '')
            return chinese_to_int(x)
        except:
            return None
    
    df['total_floors'] = df['total_floors_raw'].apply(parse)
    return df

def process_building_age(df):
    def parse_year(x):
        try:
            if pd.isna(x):
                return None
            x = str(x).zfill(7)
            roc_year = int(x[:3])
            return roc_year + 1911
        except:
            None
    df['building_year'] = df['building_year_raw'].apply(parse_year)
    df['building_age'] = df['date'].dt.year - df['building_year']

    # Remove pre-sale (building age negative)
    df = df[df['building_age'] >= 0].copy()

    # Flag missing
    df['building_age_missing'] = df['building_age'].isna().astype(int)

    # Impute missing building age
    median_age = df['building_age'].median()
    df['building_age'] = df['building_age'].fillna(median_age)
    return df

def process_floor_info(df):
    def parse(x):
        try:
            text = str(x)

            if '地下' in text:
                return -1
            
            floors = extract_floors(text)

            if len(floors) == 0:
                return None
            return floors[0]
        except:
            return None
    
    df['floor_level'] = df['floor_info_raw'].apply(parse)
    return df

def add_ml_features(df):
    df = df.copy()

    df = process_total_floors(df)
    df = process_building_age(df)
    df = process_floor_info(df)
    return df

def engineer_features(df):
    df['transaction_year'] = df['date'].dt.year
    df['transaction_month'] = df['date'].dt.month

    df['area_ratio'] = df['main_area'] / df['area']

    df['time_index'] = (df['transaction_year'] - df['transaction_year'].min()) * 12 + df['transaction_month']

    df['log_area'] = np.log(df['area'])

    df['has_parking'] = (df['parking_area'] > 0).astype(int)
    return df

def encode_features(df):
    df = pd.get_dummies(
        df,
        columns=['district', 'building_type'],
        drop_first=True
    )
    return df