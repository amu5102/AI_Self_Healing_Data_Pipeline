import sqlite3


DATABASE_PATH = "data/processed/customer_database.db"


def test_database():

    print("\n========== DATABASE VERIFICATION ==========")

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # Check number of records
    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    count = cursor.fetchone()[0]

    print(f"Total records: {count}")

    # Display customer records
    cursor.execute(
        """
        SELECT customer_id,
               customer_name,
               email,
               city,
               age
        FROM customers
        """
    )

    rows = cursor.fetchall()

    print("\nCustomer Records:")

    for row in rows:
        print(row)

    connection.close()

    print("\nDatabase verification completed")
    print("===========================================")


if __name__ == "__main__":
    test_database()