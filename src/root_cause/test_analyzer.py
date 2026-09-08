from src.failure_detection.detector import (
    detect_schema_failure,
    print_failure_report
)

from src.root_cause.analyzer import (
    analyze_schema_failure,
    print_root_cause_report
)


expected_columns = [
    "customer_id",
    "customer_name",
    "email",
    "city",
    "age"
]

actual_columns = [
    "cust_id",
    "customer_name",
    "email",
    "city",
    "age"
]


# Step 1: Detect failure
failure = detect_schema_failure(
    expected_columns,
    actual_columns
)

print_failure_report(failure)


# Step 2: Analyze root cause
root_cause = analyze_schema_failure(failure)

print_root_cause_report(root_cause)