# ingestion.py

# ---------------------
# Fetch Layer
# ---------------------
import requests
import zipfile
import io
import pandas as pd

def fetch_data():
    # url = 'https://plvr.land.moi.gov.tw/DownloadOpenData' <- url to the webpage 
    url = "https://plvr.land.moi.gov.tw/Download?type=zip&fileName=lvr_landcsv.zip" # <- url to download

    try: 
        print('Downloading data')
        # Download
        response = requests.get(url)
        print(f'Status Code: {response.status_code}')
        print(f'Content-Type: {response.headers.get('Content-Type')}') # should contain zip
        response.raise_for_status()
    
        # Load Zip
        z = zipfile.ZipFile(io.BytesIO(response.content))

        # List files
        file_list = z.namelist()
        print(file_list[:5])

        # Pick one csv
        target_file = 'a_lvr_land_a.csv'

        # Read csv
        with z.open(target_file) as f:
            try :
                df = pd.read_csv(f, encoding='utf-8')
            except UnicodeDecodeError:
                print('utf-8 failed')
        
        return df

    except Exception as e:
        print('Error occurred:', str(e))
        return None

# ---------------------
# Transform Layer
# ---------------------
import pandas as pd

def clean_data(df):
    '''
    Available columns
    Index(['鄉鎮市區', '交易標的', '土地位置建物門牌', '土地移轉總面積平方公尺', '都市土地使用分區', '非都市土地使用分區',
        '非都市土地使用編定', '交易年月日', '交易筆棟數', '移轉層次', '總樓層數', '建物型態', '主要用途', '主要建材',
        '建築完成年月', '建物移轉總面積平方公尺', '建物現況格局-房', '建物現況格局-廳', '建物現況格局-衛',
        '建物現況格局-隔間', '有無管理組織', '總價元', '單價元平方公尺', '車位類別', '車位移轉總面積平方公尺', '車位總價元',
        '備註', '編號', '主建物面積', '附屬建物面積', '陽台面積', '電梯', '移轉編號'],
    '''
    if df is None or df.empty:
        raise ValueError("input Dataframe is empty")

    # Remove duplicate header row
    df = df.iloc[1:].reset_index(drop=True)

    BASE_COLUMNS = [
        '交易年月日', '土地位置建物門牌', '總價元',
        '建物移轉總面積平方公尺', '單價元平方公尺',
        '建物型態', '鄉鎮市區'
    ]

    EXTRA_COLUMNS = [
        '車位總價元',
        '車位移轉總面積平方公尺',
        '主建物面積'
    ]

    df = df[BASE_COLUMNS + EXTRA_COLUMNS]
    
    df = df.rename(columns={
        "交易年月日": "date",
        "土地位置建物門牌": "address",
        "總價元": "price",
        "建物移轉總面積平方公尺": "area",
        "單價元平方公尺": "price_per_sqm", # contains missing value
        "建物型態": "building_type",
        "鄉鎮市區": "district",
        "車位總價元": "parking_price",
        "車位移轉總面積平方公尺": "parking_area",
        "主建物面積": "main_area"
    })

    # Strip whitespace
    df['address'] = df['address'].str.strip()
    df['district'] = df['district'].str.strip()

    # Handle weird numeric values
    df['price'] = df['price'].astype(str).str.replace(',','')
    df['area'] = df['area'].astype(str).str.replace(',','')
    df['parking_price'] = df['parking_price'].astype(str).str.replace(',','')
    df['parking_area'] = df['parking_area'].astype(str).str.replace(',','')
    df['main_area'] = df['main_area'].astype(str).str.replace(',','')

    # Convert numeric fields
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['area'] = pd.to_numeric(df['area'], errors='coerce')
    df['parking_price'] = pd.to_numeric(df['parking_price'], errors='coerce')
    df['parking_area'] = pd.to_numeric(df['parking_area'], errors='coerce')
    df['main_area'] = pd.to_numeric(df['main_area'], errors='coerce')
    df['price_per_sqm'] = pd.to_numeric(df['price_per_sqm'], errors='coerce')

    # Fillna for parking
    df['parking_price'] = df['parking_price'].fillna(0)
    df['parking_area'] = df['parking_area'].fillna(0)

    # Engineer new features
    df['net_price'] = df['price'] - df['parking_price']
    df['net_area'] = df['area'] - df['parking_area']

    # Convert date properly
    df['date'] = df['date'].astype(str).str.zfill(7)
    df['year'] = df['date'].str[:3].astype(int) + 1911
    df['month'] = df['date'].str[3:5]
    df['day'] = df['date'].str[5:7]
    df['date'] = pd.to_datetime(
        df['year'].astype(str) + '-' + df['month'] + '-' + df['day'],
        errors='coerce'
    )
    df = df.drop(columns=['year','month','day'])

    # Remove impossible values
    df = df[df['price'] > 0]
    df = df[df['area'] > 0]

    # Detect outliers (simple version)
    df = df[df['price'] < 1e9]
    df = df[df['area'] < 1000]

    # Recompute price_per_sqm
    df['computed_price_per_sqm'] = (df['price'] / df['area']).round()
    df['net_price_per_sqm'] = (df['net_price'] / df['net_area']).round()
    df['price_diff'] = abs(df['computed_price_per_sqm'] - df['price_per_sqm'])
    df['net_price_diff'] = abs(df['net_price_per_sqm'] - df['price_per_sqm'])

    # Final pricing
    df['final_price_per_sqm'] = df['price_per_sqm']
    ## When parking area > 0
    mask = (df['parking_price'] > 0) & (df['parking_area'] > 0)
    df.loc[mask, 'final_price_per_sqm'] = df['net_price_per_sqm']
    ## When parking area == 0 -> use original price_per_sqm
    ## When price_per_sqm missing -> fallback
    df.loc[df['final_price_per_sqm'].isna(), 'final_price_per_sqm'] = df['computed_price_per_sqm']

    # Pricing method label
    df['pricing_method'] = 'original'
    df.loc[mask, 'pricing_method'] = 'net_adjusted'
    df.loc[df['price_per_sqm'].isna(), 'pricing_method']  = 'fallback_computed'

    # NOTE:
    # price_per_sqm may not equal price / area due to:
    # - parking space inclusion
    # - different area definitions
    # - source rounding

    df = df.dropna(subset=['price', 'area'])

    print(f"Final rows: {len(df)}")
    print(f'Missing price_per_sqm: {df['price_per_sqm'].isna().sum()}')

    return df

# ---------------------
# Storage Layer
# ---------------------
import sqlite3

def save_to_sqlite(cleaned_df, db_path = 'taiwan_housing.db'):
    with sqlite3.connect(db_path) as conn:
        cleaned_df.to_sql(
            'transactions',
            conn,
            if_exists='append',
            index=False
        )

# ---------------------
# Orchestration Layer
# ---------------------
def main():
    raw = fetch_data()
    clean = clean_data(raw)
    save_to_sqlite(clean)
    print('completed')

if __name__ == "__main__":
    main()