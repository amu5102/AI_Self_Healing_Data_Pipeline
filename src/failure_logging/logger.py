import sqlite3


DATABASE_PATH = "data/processed/customer_database.db"


def log_failure(
    failure,
    root_cause,
    healing_action,
    status
):
    """
    Store pipeline failure information
    in the SQLite failure_logs table.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # Create failure log table if it does not exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS failure_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            failure_id TEXT,
            failure_type TEXT,
            severity TEXT,
            root_cause_type TEXT,
            confidence TEXT,
            healing_action TEXT,
            status TEXT,
            detected_at TEXT
        )
        """
    )

    # Extract root cause information
    root_cause_type = None
    confidence = None

    if root_cause is not None:
        root_cause_type = root_cause.get(
            "root_cause_type"
        )

        confidence = root_cause.get(
            "confidence"
        )

    # Insert failure record
    cursor.execute(
        """
        INSERT INTO failure_logs (
            failure_id,
            failure_type,
            severity,
            root_cause_type,
            confidence,
            healing_action,
            status,
            detected_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            failure.get("failure_id"),
            failure.get("failure_type"),
            failure.get("severity"),
            root_cause_type,
            confidence,
            healing_action,
            status,
            failure.get("detected_at")
        )
    )

    connection.commit()
    connection.close()

    print("\nFailure information logged successfully.")