import pandas as pd

from src.failure_detection.detector import (
    detect_schema_failure
)

from src.root_cause.analyzer import (
    analyze_schema_failure
)

from src.self_healing.healer import (
    apply_schema_healing,
    verify_healing
)


# Create test data with the changed column
data = {
    "cust_id": [1, 2, 3],
    "customer_name": [
        "Amruta",
        "Kunal",
        "Priya"
    ],
    "email": [
        "amruta@gmail.com",
        "kunal@gmail.com",
        "priya@gmail.com"
    ],
    "city": [
        "Pune",
        "Mumbai",
        "Nashik"
    ],
    "age": [24, 28, 26]
}

df = pd.DataFrame(data)


expected_columns = [
    "customer_id",
    "customer_name",
    "email",
    "city",
    "age"
]

actual_columns = list(df.columns)


print("\n========== BEFORE HEALING ==========")

print("Columns:")
print(list(df.columns))


# Step 1: Detect failure
failure = detect_schema_failure(
    expected_columns,
    actual_columns
)


# Step 2: Root cause analysis
root_cause = analyze_schema_failure(
    failure
)


# Step 3: Apply self-healing
df, healed = apply_schema_healing(
    df,
    root_cause
)


print("\n========== AFTER HEALING ==========")

print("Columns:")
print(list(df.columns))

print(f"\nHealing successful: {healed}")

if healed:
    
    verification_result = verify_healing(
        df,
        expected_columns
    )

    print(
        f"\nFinal pipeline status: "
        f"{'SUCCESS' if verification_result else 'FAILED'}"
    )