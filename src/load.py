import sqlite3
import pandas as pd


DATABASE_PATH = "data/processed/customer_database.db"


def load_to_database(df):
    """
    Load transformed customer data into SQLite database.
    """

    print("\n========== SQL DATABASE LOADING ==========")

    # Create database connection
    connection = sqlite3.connect(DATABASE_PATH)

    # Load DataFrame into SQL table
    df.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into SQLite database")
    print(f"Database: {DATABASE_PATH}")
    print("Table   : customers")
    print(f"Rows    : {len(df)}")

    connection.close()

    print("==========================================")

    return True


if __name__ == "__main__":

    file_path = "data/raw/customers.csv"

    df = pd.read_csv(file_path)

    load_to_database(df)