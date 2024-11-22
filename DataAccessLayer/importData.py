"""import mysql.connector
from mysql.connector import Error
try:
    connection = mysql.connector.connect(
        host="localhost",  # Default XAMPP MySQL host
        user="root",       # Default XAMPP MySQL username
        password="",       # Default XAMPP MySQL password (empty by default)
        database="hadithiq"  # Replace with your database name
    )
    if connection.is_connected():
        print("Connected to MySQL database")
except Error as e:
    print(f"Error: {e}")
finally:
        print("MySQL connection is closed")"""

from DbConnection import DbConnection
connection = DbConnection()
print(connection.getConnection())
