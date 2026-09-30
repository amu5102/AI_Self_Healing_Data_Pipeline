import pandas as pd

from src.failure_detection.detector import (
    detect_duplicate_failure
)

from src.root_cause.analyzer import (
    analyze_duplicate_failure
)


file_path = "data/raw/customers_duplicates.csv"

df = pd.read_csv(file_path)

failure = detect_duplicate_failure(df)

root_cause = analyze_duplicate_failure(
    failure
)

print("\n========== DUPLICATE ROOT CAUSE ANALYSIS ==========")

if root_cause is None:

    print("No root cause analysis required.")

else:

    print(
        f"Root Cause Type : "
        f"{root_cause['root_cause_type']}"
    )

    print(
        f"Description     : "
        f"{root_cause['description']}"
    )

    print(
        f"Duplicate Count : "
        f"{root_cause['duplicate_count']}"
    )

    print(
        f"Confidence      : "
        f"{root_cause['confidence']}"
    )

print("====================================================")