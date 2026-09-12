import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("1. Python started")

try:

    print("2. Connecting...")

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="heartcare",
        connection_timeout=5,
        use_pure=True
    )

    print("3. CONNECTION SUCCESS!")

    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")

    result = cursor.fetchone()

    print("4. Connected database:", result)

    cursor.execute("SELECT COUNT(*) FROM patient_records")

    count = cursor.fetchone()

    print("5. Patient records:", count)

    cursor.close()

    connection.close()

    print("6. CONNECTION CLOSED")


except Exception as error:

    print("7. CONNECTION FAILED")

    print("Error type:", type(error).__name__)

    print("Error:", error)


print("8. TEST FINISHED")