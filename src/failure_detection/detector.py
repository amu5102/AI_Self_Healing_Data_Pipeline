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

    # Schema failure details
    if failure["failure_type"] == "SCHEMA_CHANGE":

        print(
            f"Missing       : "
            f"{failure['missing_columns']}"
        )

        print(
            f"Extra         : "
            f"{failure['extra_columns']}"
        )

    # NULL failure details
    elif failure["failure_type"] == "NULL_DATA":

        print(
            f"NULL Columns  : "
            f"{failure['null_columns']}"
        )

    print(
        f"Detected At   : "
        f"{failure['detected_at']}"
    )

    print("======================================\n")

    
def detect_null_failure(df):
    """
    Detect columns containing NULL values.
    """

    null_counts = df.isnull().sum()

    null_columns = {
        column: int(count)
        for column, count in null_counts.items()
        if count > 0
    }

    if not null_columns:
        return None

    failure = {
        "failure_id": f"F-NULL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "failure_type": "NULL_DATA",
        "severity": "MEDIUM",
        "null_columns": null_columns,
        "detected_at": datetime.now().isoformat()
    }

    return failure

def detect_duplicate_failure(df):
    """
    Detect duplicate records in the dataset.
    """

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count == 0:
        return None

    failure = {
        "failure_id": f"F-DUP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "failure_type": "DUPLICATE_DATA",
        "severity": "MEDIUM",
        "duplicate_count": duplicate_count,
        "detected_at": datetime.now().isoformat()
    }

    return failure