import pandas as pd

from src.validation.validate import validate_data


def extract_data(file_path):
    """Read customer data from a CSV file."""

    df = pd.read_csv(file_path)

    print("Data extracted successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":

    file_path = "data/raw/customers_schema_changed.csv"

    df = extract_data(file_path)

    print("\nFirst 5 records:")
    print(df.head())

    validate_data(df)