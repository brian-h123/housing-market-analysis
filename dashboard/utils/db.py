from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)
def load_data():
    db_path = Path(__file__).resolve().parents[2] / "data" / "taiwan_housing.db"
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}")

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(
            "SELECT * FROM transactions",
            conn,
            parse_dates=['date']
        )

    # Development Check (remove before production)
    assert df['final_price_per_sqm'].notna().all()
    assert df['area'].notna().all()

    return df