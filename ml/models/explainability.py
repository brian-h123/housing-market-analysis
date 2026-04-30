import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # for Traditional Chinese
plt.rcParams['axes.unicode_minus'] = False

def get_feature_importance(model, feature_names):
    df = pd.DataFrame({
        'feature': feature_names,
        'coefficient': model.coef_
    })

    df['abs_coef'] = df['coefficient'].abs()

    return df.sort_values(by='abs_coef', ascending=False)

def clean_feature_names(df):
    def clean(name):
        if name.startswith('district_'):
            return name.replace('district_', '')
        elif name.startswith('building_type_'):
            return name.replace('building_type_', '')
        else:
            return name

    df['feature_clean'] = df['feature'].apply(clean)
    return df

def categorize_feature(name):
    if name.startswith('district_'):
        return 'location'
    elif name.startswith('building_type_'):
        return 'building_type'
    elif name in ['log_area', 'area_ratio']:
        return 'size'
    elif name in ['total_floors']:
        return 'structure'
    elif name in ['building_age']:
        return 'age'
    elif name in ['parking_area', 'has_parking']:
        return 'parking'
    elif name in ['time_index']:
        return 'time'
    else:
        return 'other'

def get_top_features(df, n=15):
    return df.head(n)

def plot_feature_importance(df, n=15):
    top_df = df.head(n).iloc[::-1]

    plt.figure(figsize=(14,6))
    plt.barh(top_df['feature_clean'], top_df['coefficient'])
    plt.xlabel('Coefficient')
    plt.title('Top Feature Importance (Ridge)')
    plt.show()