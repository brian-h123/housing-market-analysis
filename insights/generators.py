def generate_district_insight(row):
    if row['mean_residual'] > 0:
        label = 'Overpriced District'
        pricing_desc = 'tends to be priced above model expectation'
    else:
        label = 'Undervalued District'
        pricing_desc = 'tends to be priced below model expectations'

    if row['volatility'] > 1.5:
        stability_desc = 'Pricing is highly inconsistent, suggestion diverse or unpredictable.'
    elif row['volatility'] > 1:
        stability_desc = 'Pricing shows moderate variation across transactions.'
    else:
        stability_desc = 'Pricing is relatively stable.'

    explanation = (
        f"{row['district']} {pricing_desc}. {stability_desc}"
    )

    return {
        'district': row['district'],
        'label': label,
        'explanation': explanation,
        'metrics': {
            'mean_residual': row['mean_residual'],
            'volatility': row['volatility'],
            'transaction_count': row['transaction_count']
        }
    }

def generate_transaction_insight(row):
    if row['residual'] > 0:
        label = 'Overpriced'
    else:
        label = 'Undervalued'

    pct = abs(row['pct_diff']) * 100

    z = abs(row['residual_z'])

    if z > 3:
        severity = 'extremely'
    elif z > 2:
        severity = 'significantly'
    else:
        severity = 'moderately'

    explanation = (
        f"This property is {severity} {label.lower()} "
        f"by approximately {pct:.1f}% compared to similar properties."
    )

    return {
        'district': row['district'],
        'label': label,
        'severity': severity,
        'explanation': explanation,
        'metrics': {
            'actual_price': row['actual_price'],
            'predicted_price': row['predicted_price'],
            'residual': row['residual'],
            'pct_diff': row['pct_diff']
        }
    }
