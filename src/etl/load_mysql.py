import os
import mysql.connector
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "traffic_safety"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
}

DATA_DIR = "data/processed"

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_dataframe(conn, table_name, df, batch_size=2000):
    cursor = conn.cursor()
    columns = [col.lower() for col in df.columns]
    col_str = ", ".join([f"`{c}`" for c in columns])
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO `{table_name}` ({col_str}) VALUES ({placeholders})"

    cleaned_df = df.replace({np.nan: None})
    records = [
        [None if (isinstance(val, float) and np.isnan(val)) else val for val in row]
        for row in cleaned_df.to_numpy()
    ]
    
    total = len(records)
    print(f"Loading {total} records into '{table_name}'...")

    for i in range(0, total, batch_size):
        batch = records[i : i + batch_size]
        cursor.executemany(query, batch)
        conn.commit()

    cursor.close()
    print(f"Successfully loaded '{table_name}'.")

def main():
    conn = get_connection()
    try:
        df_crashes = pd.read_csv(os.path.join(DATA_DIR, "crashes.csv"), low_memory=False)
        insert_dataframe(conn, "crashes", df_crashes)

        df_vehicles = pd.read_csv(os.path.join(DATA_DIR, "vehicles.csv"), low_memory=False)
        insert_dataframe(conn, "vehicles", df_vehicles)

        df_people = pd.read_csv(os.path.join(DATA_DIR, "people.csv"), low_memory=False)
        insert_dataframe(conn, "people", df_people)

    finally:
        conn.close()

if __name__ == "__main__":
    main()