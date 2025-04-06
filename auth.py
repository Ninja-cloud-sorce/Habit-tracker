import hashlib
import os
import sys
from db_config import get_connection  # Use relative import if db.py is in the same package
# Adjust the import path for db module dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                       (username, hash_password(password)))
        conn.commit()
        return True
    except Exception as e:
        print("Registration Error:", e)
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password_hash FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[1] == hash_password(password):
        return result[0]  # Return user_id
    return None