import pandas as pd

from src.failure_detection.detector import (
    detect_duplicate_failure
)


file_path = "data/raw/customers_duplicates.csv"

df = pd.read_csv(file_path)

failure = detect_duplicate_failure(df)

print("\n========== DUPLICATE FAILURE DETECTION ==========")

if failure is None:

    print("No duplicate failure detected.")

else:

    print(f"Failure ID      : {failure['failure_id']}")
    print(f"Failure Type    : {failure['failure_type']}")
    print(f"Severity        : {failure['severity']}")
    print(f"Duplicate Count : {failure['duplicate_count']}")
    print(f"Detected At     : {failure['detected_at']}")

print("=================================================")