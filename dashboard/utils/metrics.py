def format_currency(x):
    return f"${x:,.0f}"

def format_number(x):
    return f"{x:,.0f}"

def format_billions(x, pos):
    return f"{x*1e-9:.1f}B"

METRIC_CONFIG = {
    "avg_price_per_sqm": {
        "label": "Average Price per SQM",
        # "variable": "avg_price_per_sqm",
        "format": format_currency
    },
    "median_price_per_sqm": {
        "label": "Median Price per SQM",
        # "variable": "median_price_per_sqm",
        "format": format_currency
    },
    "transaction_volume": {
        "label": "Transaction Volume",
        # "variable": "transaction_volume",
        "format": format_number
    }
}