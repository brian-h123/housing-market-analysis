import sqlite3
import pandas as pd

def load_data():
    db_path = 'data/taiwan_housing.db'

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(
            "SELECT * FROM transactions",
            conn,
            parse_dates=['date']
        )

    return df
