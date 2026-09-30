import pandas as pd

from src.failure_detection.detector import (
    detect_null_failure
)

from src.root_cause.analyzer import (
    analyze_null_failure
)


file_path = "data/raw/customers_null.csv"

df = pd.read_csv(file_path)

failure = detect_null_failure(df)

root_cause = analyze_null_failure(
    failure
)

print("\n========== NULL ROOT CAUSE ANALYSIS ==========")

print(
    f"Root Cause Type : "
    f"{root_cause['root_cause_type']}"
)

print(
    f"Description     : "
    f"{root_cause['description']}"
)

print(
    f"Affected Columns: "
    f"{root_cause['affected_columns']}"
)

print(
    f"NULL Counts     : "
    f"{root_cause['null_counts']}"
)

print(
    f"Total NULLs     : "
    f"{root_cause['total_nulls']}"
)

print(
    f"Confidence      : "
    f"{root_cause['confidence']}"
)

print("==============================================")