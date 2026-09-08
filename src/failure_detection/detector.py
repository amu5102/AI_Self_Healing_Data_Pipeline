from datetime import datetime


def detect_schema_failure(
    expected_columns,
    actual_columns
):
    """
    Detect schema-related failures by comparing
    expected and actual columns.
    """

    missing_columns = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    extra_columns = [
        column
        for column in actual_columns
        if column not in expected_columns
    ]

    if not missing_columns and not extra_columns:
        return None

    failure = {
        "failure_id": f"F-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "failure_type": "SCHEMA_CHANGE",
        "severity": "HIGH",
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "detected_at": datetime.now().isoformat()
    }

    return failure


def print_failure_report(failure):
    """Display a readable failure report."""

    if failure is None:
        print("\nNo failure detected.")
        return

    print("\n========== FAILURE DETECTED ==========")

    print(f"Failure ID    : {failure['failure_id']}")
    print(f"Failure Type  : {failure['failure_type']}")
    print(f"Severity      : {failure['severity']}")
    print(f"Missing       : {failure['missing_columns']}")
    print(f"Extra         : {failure['extra_columns']}")
    print(f"Detected At   : {failure['detected_at']}")

    print("======================================\n")