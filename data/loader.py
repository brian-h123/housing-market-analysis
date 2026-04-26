import os
import sqlite3
import pandas as pd

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'taiwan_housing.db')

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(
            "SELECT * FROM transactions",
            conn,
            parse_dates=['date']
        )

    return df
