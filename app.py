import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user

root = tk.Tk()
root.title("Habit Tracker")

def register():
    uname, pwd = username.get(), password.get()
    success = register_user(uname, pwd)
    msg = "Registered!" if success else "Username exists!"
    messagebox.showinfo("Register", msg)

def login():
    uname, pwd = username.get(), password.get()
    success = login_user(uname, pwd)
    msg = "Logged in!" if success else "Login Failed!"
    messagebox.showinfo("Login", msg)

tk.Label(root, text="Username").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root, text="Password").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()

root.mainloop()