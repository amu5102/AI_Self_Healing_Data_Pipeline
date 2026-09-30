import sqlite3

from src.failure_logging.logger import log_failure


DATABASE_PATH = "data/processed/customer_database.db"


failure = {
    "failure_id": "TEST-001",
    "failure_type": "SCHEMA_CHANGE",
    "severity": "HIGH",
    "detected_at": "2026-09-30T16:00:00"
}


root_cause = {
    "root_cause_type": "POSSIBLE_COLUMN_RENAME",
    "confidence": "MEDIUM"
}


log_failure(
    failure,
    root_cause,
    "cust_id -> customer_id",
    "HEALED"
)


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT
        failure_id,
        failure_type,
        severity,
        root_cause_type,
        confidence,
        healing_action,
        status
    FROM failure_logs
    """
)

rows = cursor.fetchall()

print("\n========== FAILURE LOGS ==========")

for row in rows:
    print(row)

connection.close()

print("==================================")