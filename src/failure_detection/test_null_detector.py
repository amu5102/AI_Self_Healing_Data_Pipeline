import pandas as pd

from src.failure_detection.detector import (
    detect_null_failure
)


file_path = "data/raw/customers_null.csv"

df = pd.read_csv(file_path)

failure = detect_null_failure(df)

print("\n========== NULL FAILURE DETECTION ==========")

if failure is None:
    print("No NULL failure detected.")

else:
    print(f"Failure ID   : {failure['failure_id']}")
    print(f"Failure Type : {failure['failure_type']}")
    print(f"Severity     : {failure['severity']}")
    print(f"NULL Columns : {failure['null_columns']}")
    print(f"Detected At  : {failure['detected_at']}")

print("============================================")