import random
import pandas as pd

OUTPUT_FILE = "data/processed/ml_failure_history.csv"

random.seed(42)

records = []

failure_types = [
    "SCHEMA_CHANGE",
    "NULL_DATA",
    "DUPLICATE_DATA"
]

for _ in range(200):

    failure_type = random.choice(failure_types)

    if failure_type == "SCHEMA_CHANGE":
        severity = random.choice(["HIGH", "MEDIUM"])
        root_cause_type = random.choice([
            "POSSIBLE_COLUMN_RENAME",
            "SCHEMA_MISMATCH"
        ])
        confidence = random.choice(["HIGH", "MEDIUM"])
        duplicate_count = random.choice([0, 0, 0, 1, 2])
        null_count = random.choice([0, 0, 1, 2])
        schema_change = random.choice([1, 1, 1, 0])

    elif failure_type == "NULL_DATA":
        severity = random.choice(["MEDIUM", "LOW", "HIGH"])
        root_cause_type = random.choice([
            "MISSING_DATA",
            "INCOMPLETE_DATA"
        ])
        confidence = random.choice(["HIGH", "MEDIUM"])
        duplicate_count = random.choice([0, 0, 1, 2])
        null_count = random.choice([1, 2, 3, 5, 8, 10])
        schema_change = random.choice([0, 0, 0, 1])

    else:
        severity = random.choice(["MEDIUM", "LOW", "HIGH"])
        root_cause_type = random.choice([
            "DUPLICATE_RECORDS",
            "REPEATED_DATA"
        ])
        confidence = random.choice(["HIGH", "MEDIUM"])
        duplicate_count = random.choice([1, 2, 3, 4, 5, 8])
        null_count = random.choice([0, 0, 1, 2])
        schema_change = random.choice([0, 0, 0, 1])

    records.append({
        "severity": severity,
        "root_cause_type": root_cause_type,
        "confidence": confidence,
        "duplicate_count": duplicate_count,
        "null_count": null_count,
        "schema_change": schema_change,
        "failure_type": failure_type
    })


df = pd.DataFrame(records)

df.to_csv(OUTPUT_FILE, index=False)

print("\n==========================================")
print("   IMPROVED ML TRAINING DATASET CREATED")
print("==========================================")

print(f"\nRows: {len(df)}")

print("\nFailure Type Distribution:")
print(df["failure_type"].value_counts())

print("\nSample Records:")
print(df.head(10).to_string(index=False))

print("\nDataset saved to:")
print(OUTPUT_FILE)

print("==========================================")