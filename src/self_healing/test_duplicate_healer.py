import pandas as pd

from src.failure_detection.detector import (
    detect_duplicate_failure
)

from src.root_cause.analyzer import (
    analyze_duplicate_failure
)

from src.self_healing.healer import (
    apply_duplicate_healing,
    verify_duplicate_healing
)


file_path = "data/raw/customers_duplicates.csv"

df = pd.read_csv(file_path)

print("\n========== BEFORE DUPLICATE HEALING ==========")

print(df)

failure = detect_duplicate_failure(df)

root_cause = analyze_duplicate_failure(
    failure
)

df, healed = apply_duplicate_healing(
    df,
    root_cause
)

print("\n========== AFTER DUPLICATE HEALING ==========")

print(df)

print(
    f"\nHealing successful: {healed}"
)

verification = verify_duplicate_healing(
    df
)

print(
    f"\nHealing verification: {verification}"
)

print("\nRemaining duplicate records:")
print(df.duplicated().sum())

print("==============================================")