import math
import streamlit as st
from utils.filters import apply_filters, validate_filters

def compute_bounds(base_df):
    return {
        'min_price': int(base_df['final_price_per_sqm'].min()),
        'max_price': int(base_df['final_price_per_sqm'].max()),
        'min_area': int(base_df['area'].min()),
        'max_area': int(base_df['area'].max())
    }

def round_bounds(bounds):
    return {
        'min_price': int(math.floor(bounds['min_price'] / 10000) * 10000),
        'max_price': int(math.ceil(bounds['max_price'] / 10000) * 10000),
        'min_area': int(math.floor(bounds['min_area'] / 10) * 10),
        'max_area': int(math.ceil(bounds['max_area'] / 10) * 10)
    }

def render_secondary_filters(bounds):
    st.sidebar.header("🏠 Property")

    # Price slider
    price_range = st.sidebar.slider(
        "Price per sqm",
        min_value=bounds["min_price"],
        max_value=bounds["max_price"],
        value=(bounds["min_price"], bounds["max_price"]),
        step=10000
    )

    # Area Slider
    area_range = st.sidebar.slider(
        "Area (sqm)",
        min_value=bounds["min_area"],
        max_value=bounds["max_area"],
        value=(bounds["min_area"], bounds["max_area"]),
        step=10
    )

    return {
        'min_price': price_range[0],
        'max_price': price_range[1],
        'min_area': area_range[0],
        'max_area': area_range[1]
    }

def validate_slider_filters(filters):
    if filters['min_price'] == filters['max_price']:
        st.warning("Please select a valid price range")
        return False
    if filters['min_area'] == filters['max_area']:
        st.warning("Please select a valid area range")
        return False
    return True

def apply_filter_pipeline(df, base_filters):
    # Validate
    if not validate_filters(base_filters):
        return None, None
    
    # Base filtering (District + Date)
    base_df = apply_filters(df, base_filters)

    if base_df.empty:
        st.warning("No data for selected district/date")
        return None, None
    
    # Compute bounds (Price + Area)
    bounds = compute_bounds(base_df)
    bounds = round_bounds(bounds)

    # Render sliders (Price + Area)
    secondary_filters = render_secondary_filters(bounds)

    full_filters = {
        **base_filters,
        **secondary_filters
    }

    # Validate
    if not validate_slider_filters(full_filters):
        return None, None

    # Final filtering
    filtered_df = apply_filters(base_df, full_filters)

    return filtered_df, full_filters