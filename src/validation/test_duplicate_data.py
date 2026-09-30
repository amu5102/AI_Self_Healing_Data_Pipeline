import pandas as pd

from src.validation.validate import validate_data


file_path = "data/raw/customers_duplicates.csv"

df = pd.read_csv(file_path)

print("\n========== DUPLICATE DATA TEST ==========")

print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

validate_data(df)

print("=========================================")