"""
Loads the cleaned dataset into a local SQLite database so the queries in sql/*.sql can run.

The database file itself is not committed (see .gitignore) — it's a disposable build
artifact, trivial to regenerate from data/processed/banking_customer_journeys_clean.csv,
which is the actual source of truth.

Usage (from the project root):
    python sql/load_to_sqlite.py
"""

import os
import sqlite3

import pandas as pd

CSV_PATH = os.path.join("data", "processed", "banking_customer_journeys_clean.csv")
DB_PATH = os.path.join("sql", "novabank.db")
TABLE_NAME = "journeys"


def main():
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {len(df):,} rows into {DB_PATH} (table: {TABLE_NAME})")


if __name__ == "__main__":
    main()
