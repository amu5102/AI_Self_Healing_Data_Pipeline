import pandas as pd

from src.failure_detection.detector import (
    detect_null_failure
)

from src.root_cause.analyzer import (
    analyze_null_failure
)

from src.self_healing.healer import (
    apply_null_healing,
    verify_null_healing
)


file_path = "data/raw/customers_null.csv"

df = pd.read_csv(file_path)

print("\n========== BEFORE NULL HEALING ==========")

print(df)

# Detect failure
failure = detect_null_failure(df)

# Analyze root cause
root_cause = analyze_null_failure(
    failure
)

# Apply healing
df, healed = apply_null_healing(
    df,
    root_cause
)

print("\n========== AFTER NULL HEALING ==========")

print(df)

print(
    f"\nHealing successful: {healed}"
)
verification = verify_null_healing(df)

print(
    f"\nHealing verification: {verification}"
)

print("\nRemaining NULL values:")

print(df.isnull().sum())

print("=========================================")