import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk  # For progress bars
from auth import register_user, login_user
try:
    from habit import add_habit, get_user_habits, mark_habit_done
except ImportError:
    raise ImportError("The 'habit' module could not be found. Ensure 'habit.py' exists in the same directory as 'main.py'.")

class HabitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("21-Day Habit Tracker")
        self.root.geometry("500x550")
        self.custom_font = font.Font(family="Helvetica", size=12)
        self.init_widgets()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def init_widgets(self):
        # Login/Register Screen
        self.clear()
        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        title = tk.Label(main_frame, text="Welcome to Habit Tracker", 
                         font=("Helvetica", 18, "bold"), bg="#F5F5F5", fg="black")
        title.pack(pady=(0,20))

        form_frame = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
        form_frame.pack(pady=10, padx=10)

        # Username row  
        tk.Label(form_frame, text="Username", font=self.custom_font, bg="white", fg="black")\
            .grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.username_entry = tk.Entry(form_frame, font=self.custom_font, fg="black", bg="white", insertbackground="black")
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password row  
        tk.Label(form_frame, text="Password", font=self.custom_font, bg="white", fg="black")\
            .grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.password_entry = tk.Entry(form_frame, font=self.custom_font, show="*", fg="black", bg="white", insertbackground="black")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(main_frame, bg="#F5F5F5")
        btn_frame.pack(pady=20)

        login_button = tk.Button(btn_frame, text="Login", command=self.login, 
                                 font=self.custom_font, bg="#4CAF50", fg="black", activeforeground="black", padx=15, pady=8)
        login_button.grid(row=0, column=0, padx=10)

        register_button = tk.Button(btn_frame, text="Register", command=self.register, 
                                    font=self.custom_font, bg="#2196F3", fg="black", activeforeground="black", padx=15, pady=8)
        register_button.grid(row=0, column=1, padx=10)
    
    def register(self):
        uname, pwd = self.username_entry.get(), self.password_entry.get()
        if register_user(uname, pwd):
            messagebox.showinfo("Success", "User registered!")
        else:
            messagebox.showerror("Error", "Username may already exist.")
    
    def login(self):
        uname, pwd = self.username_entry.get(), self.password_entry.get()
        user_id = login_user(uname, pwd)
        if user_id:
            messagebox.showinfo("Login", "Logged in successfully!")
            self.user_id = user_id
            self.username = uname  # Save username for display in header
            self.habit_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
    
    def habit_screen(self):
        self.clear()
        
        # Main frame for the habit screen
        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header frame: Displays logged-in username and Back to Login button.
        header_frame = tk.Frame(main_frame, bg="#F5F5F5")
        header_frame.pack(fill="x")
        welcome_label = tk.Label(header_frame, text=f"Welcome, {self.username}", 
                                   font=("Helvetica", 16, "bold"), bg="#F5F5F5", fg="black")
        welcome_label.pack(side="left", padx=10, pady=10)
        logout_button = tk.Button(header_frame, text="Back to Login", command=self.init_widgets,
                                  font=self.custom_font, bg="#FF5722", fg="black", activeforeground="black", 
                                  padx=10, pady=4)
        logout_button.pack(side="right", padx=10, pady=10)
        
        # Title for the habit section
        title = tk.Label(main_frame, text="Your 21-Day Habit Tracker", 
                         font=("Helvetica", 18, "bold"), bg="#F5F5F5", fg="black")
        title.pack(pady=(10,20))
        
        # Content frame for ongoing habits list
        content_frame = tk.Frame(main_frame, bg="#F5F5F5")
        content_frame.pack(fill="x", pady=10)
        
        habits = get_user_habits(self.user_id)  # Expected: list of tuples (id, habit_name, count)
        ongoing_exists = False
        if habits:
            for idx, habit in enumerate(habits):
                if habit[2] < 21:
                    ongoing_exists = True
                    habit_row = tk.Frame(content_frame, bg="#F5F5F5")
                    habit_row.grid(row=idx, column=0, pady=5, padx=10, sticky="ew")
                    habit_row.columnconfigure(1, weight=1)
                    
                    # Habit name label
                    tk.Label(habit_row, text=habit[1], font=self.custom_font, bg="#F5F5F5", fg="black")\
                        .grid(row=0, column=0, padx=10, sticky="w")
                    # Display count label: habit[2] / 21
                    tk.Label(habit_row, text=f"{habit[2]} / 21", font=self.custom_font, bg="#F5F5F5", fg="black")\
                        .grid(row=0, column=1, padx=10, sticky="w")
                    # Mark as Done button
                    tk.Button(habit_row, text="Mark as Done", 
                              command=lambda h_id=habit[0]: self.mark_habit_done_by_id(h_id),
                              font=self.custom_font, bg="#4CAF50", fg="black", activeforeground="black",
                              padx=10, pady=4)\
                        .grid(row=0, column=2, padx=10, sticky="e")
        
        if not ongoing_exists:
            tk.Label(content_frame, text="No ongoing habits. Add a new habit below.", 
                     font=self.custom_font, bg="#F5F5F5", fg="black").pack(pady=5)
        
        # Frame for adding a new habit
        add_frame = tk.Frame(main_frame, bg="#F5F5F5")
        add_frame.pack(fill="x", pady=10)
        tk.Label(add_frame, text="New Habit:", font=self.custom_font, bg="#F5F5F5", fg="black")\
            .grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_habit_entry = tk.Entry(add_frame, font=self.custom_font, fg="black", bg="white", insertbackground="black")
        self.new_habit_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        add_frame.columnconfigure(1, weight=1)
        tk.Button(add_frame, text="Create Habit", command=self.create_habit,
                  font=self.custom_font, bg="#2196F3", fg="black", activeforeground="black")\
            .grid(row=0, column=2, padx=5, pady=5)
        
        # Completed Habits Section (placed after the New Habit bar)
        completed_habits = [habit for habit in habits if habit[2] >= 21] if habits else []
        if completed_habits:
            completed_frame = tk.Frame(main_frame, bg="#F5F5F5")
            completed_frame.pack(fill="x", pady=10)
            tk.Label(completed_frame, text="Completed Habits:", 
                     font=("Helvetica", 16, "bold"), bg="#F5F5F5", fg="black")\
                .pack(anchor="w", padx=10)
            for comp in completed_habits:
                tk.Label(completed_frame, text=f"• {comp[1]}", font=self.custom_font, bg="#F5F5F5", fg="black")\
                    .pack(anchor="w", padx=20)
    
    def create_habit(self):
        habit_name = self.new_habit_entry.get().strip()
        if habit_name:
            add_habit(self.user_id, habit_name)
            messagebox.showinfo("Habit", f"Habit '{habit_name}' created!")
            self.new_habit_entry.delete(0, tk.END)
            self.habit_screen()  # Refresh the habit screen.
        else:
            messagebox.showerror("Error", "Please enter a habit name.")
    
    def mark_habit_done_by_id(self, habit_id):
        mark_habit_done(habit_id)
        # After marking, check if this habit is now complete (i.e., count >= 21)
        updated_habits = get_user_habits(self.user_id)
        for habit in updated_habits:
            if habit[0] == habit_id and habit[2] >= 21:
                self.congrats_screen(habit)
                return
        messagebox.showinfo("Habit", "Habit marked as done!")
        self.habit_screen()  # Refresh to update progress.
    
    def congrats_screen(self, habit):
        # Clear the screen and show a congratulatory message after completion.
        self.clear()
        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        message = f"Congratulations!\nYou have completed 21 days of '{habit[1]}'!"
        message_label = tk.Label(main_frame, text=message, 
                                 font=("Helvetica", 18, "bold"), bg="#F5F5F5", fg="black")
        message_label.pack(pady=20)
        
        # Button to return to tracker
        tracker_button = tk.Button(main_frame, text="Back to Tracker", command=self.habit_screen,
                                   font=self.custom_font, bg="#2196F3", fg="black", activeforeground="black", padx=15, pady=8)
        tracker_button.pack(pady=10)
        # Optionally, add a button to log out and go back to login
        logout_button = tk.Button(main_frame, text="Back to Login", command=self.init_widgets,
                                  font=self.custom_font, bg="#FF5722", fg="black", activeforeground="black", padx=15, pady=8)
        logout_button.pack(pady=10)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitApp(root)
    root.mainloop()