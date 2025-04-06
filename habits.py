from db_config import get_connection
from datetime import date

def add_habit(user_id, habit_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO habits (user_id, name) VALUES (%s, %s)", (user_id, habit_name))
    conn.commit()
    conn.close()

def get_user_habits(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT habit_id, name FROM habits WHERE user_id=%s", (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits

def mark_habit_done(habit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO completions (habit_id, completion_date) VALUES (%s, %s)", 
                   (habit_id, date.today()))
    conn.commit()
    conn.close()