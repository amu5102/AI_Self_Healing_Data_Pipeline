from src.failure_detection.detector import (
    detect_schema_failure,
    print_failure_report
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


failure = detect_schema_failure(
    expected_columns,
    actual_columns
)

print_failure_report(failure)