# A global list to hold habits for demonstration.
# Each habit is stored as a tuple: (habit_id, habit_name, count)
habits = []

def add_habit(user_id, habit_name):
    new_id = len(habits) + 1
    habits.append((new_id, habit_name, 0))
    print(f"Adding habit '{habit_name}' for user {user_id}")

def get_user_habits(user_id):
    return habits

def mark_habit_done(habit_id):
    for index, habit in enumerate(habits):
        if habit[0] == habit_id:
            count = habit[2]
            # Increase the count if not reached 21 days
            if count < 21:
                count += 1
            habits[index] = (habit[0], habit[1], count)
            print(f"Habit '{habit[1]}' count increased to {count}")
            break