import sqlite3


DATABASE_PATH = "data/processed/customer_database.db"


def view_failure_logs():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            failure_id,
            failure_type,
            severity,
            root_cause_type,
            confidence,
            healing_action,
            status,
            detected_at
        FROM failure_logs
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    print("\n========== FAILURE HISTORY ==========")

    if not rows:
        print("No failure logs found.")

    for row in rows:
        print(f"\nLog ID          : {row[0]}")
        print(f"Failure ID      : {row[1]}")
        print(f"Failure Type    : {row[2]}")
        print(f"Severity        : {row[3]}")
        print(f"Root Cause      : {row[4]}")
        print(f"Confidence      : {row[5]}")
        print(f"Healing Action  : {row[6]}")
        print(f"Status          : {row[7]}")
        print(f"Detected At     : {row[8]}")

    connection.close()

    print("\n====================================")


if __name__ == "__main__":
    view_failure_logs()