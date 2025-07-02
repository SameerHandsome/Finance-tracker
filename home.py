import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

class HomeApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Task Manager - Home")
        self.geometry("400x300")
        
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
        
        # UI
        tk.Label(self, text="Task Management System", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text="Welcome! Manage your tasks.", font=("Arial", 10)).pack(pady=10)
        
        # Task summary
        self.summary_label = tk.Label(self, text="Loading task summary...", font=("Arial", 10))
        self.summary_label.pack(pady=10)
        self.update_summary()
        
        # Navigation buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Add Task", width=12, command=self.open_add_task).pack(side="left", padx=5)
        tk.Button(button_frame, text="View Tasks", width=12, command=self.open_task_list).pack(side="left", padx=5)
        tk.Button(button_frame, text="Progress", width=12, command=self.open_progress).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Task", width=12, command=self.open_edit_task).pack(side="left", padx=5)
    
    def update_summary(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
        completed_tasks = self.cursor.fetchone()[0]
        summary = f"Total Tasks: {total_tasks}\nCompleted Tasks: {completed_tasks}"
        self.summary_label.config(text=summary)
    
    def open_add_task(self):
        try:
            subprocess.run(["python", "add_task_app.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "Add Task app not found!")
    
    def open_task_list(self):
        try:
            subprocess.run(["python", "task_list_app.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "Task List app not found!")
    
    def open_progress(self):
        try:
            subprocess.run(["python", "progress_app.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "Progress app not found!")
    
    def open_edit_task(self):
        try:
            subprocess.run(["python", "edit_task_app.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "Edit Task app not found!")

if __name__ == "__main__":
    app = HomeApp()
    app.mainloop()
