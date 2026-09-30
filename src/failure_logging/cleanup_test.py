import sqlite3


DATABASE_PATH = "data/processed/customer_database.db"


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

cursor.execute(
    """
    DELETE FROM failure_logs
    WHERE failure_id = 'TEST-001'
    """
)

connection.commit()

print("Test failure record removed.")

connection.close()