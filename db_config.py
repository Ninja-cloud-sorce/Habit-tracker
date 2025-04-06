import mysql.connector  # Ensure the mysql-connector-python package is installed

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root1234',  # Change to your password
    'database': 'habit_tracker'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)