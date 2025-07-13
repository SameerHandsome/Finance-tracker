import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

class HomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Home")
        self.geometry("420x320")  # Slightly increased window size for better spacing

        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                priority TEXT,
                due_date TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

        # UI elements
        tk.Label(self, text="Task Management System", font=("Arial", 16, "bold")).pack(pady=(20, 5))
        tk.Label(self, text="Welcome! Manage your tasks.", font=("Arial", 10)).pack(pady=(0, 10))

        # Task summary section
        self.summary_label = tk.Label(self, text="Loading task summary...", font=("Arial", 10))
        self.summary_label.pack(pady=10)
        self.update_summary()

        # Navigation buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Buttons with blue background and white text
        button_style = {"width": 12, "bg": "blue", "fg": "white"}
        tk.Button(button_frame, text="Add Task", command=self.open_add_task, **button_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="View Tasks", command=self.open_task_list, **button_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="Progress", command=self.open_progress, **button_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Task", command=self.open_edit_task, **button_style).pack(side="left", padx=5)

    def update_summary(self):
        """Update the task summary label."""
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
        completed_tasks = self.cursor.fetchone()[0]

        summary = f"Total Tasks: {total_tasks}\nCompleted Tasks: {completed_tasks}"
        self.summary_label.config(text=summary)

    def open_add_task(self):
        try:
            subprocess.run(["python", "add_task_app.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Add Task app!\n{e}")

    def open_task_list(self):
        try:
            subprocess.run(["python", "task_list_app.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Task List app!\n{e}")

    def open_progress(self):
        try:
            subprocess.run(["python", "progress_app.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Progress app!\n{e}")

    def open_edit_task(self):
        try:
            subprocess.run(["python", "edit_task_app.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Edit Task app!\n{e}")

if __name__ == "__main__":
    app = HomeApp()
    app.mainloop()
