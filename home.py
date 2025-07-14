# Contribution by Ahmad Khawar: Verified home screen GUI structure
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess

class HomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Home")
        self.geometry("500x400")
        self.configure(bg="#f5f7fa")  # Light background color

        # Database setup
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

        # Header Section
        header = tk.Frame(self, bg="#f5f7fa")
        header.pack(pady=(20, 10))

        tk.Label(header, text="📋 Task Management System", 
                 font=("Segoe UI", 18, "bold"), bg="#f5f7fa", fg="#2c3e50").pack()
        tk.Label(header, text="Welcome! Manage your tasks effectively.",
                 font=("Segoe UI", 11), bg="#f5f7fa", fg="#34495e").pack()

        # Summary Section
        summary_frame = tk.Frame(self, bg="#f5f7fa", pady=10)
        summary_frame.pack()

        self.summary_label = tk.Label(summary_frame, 
                                      text="Loading task summary...",
                                      font=("Segoe UI", 10), 
                                      bg="#f5f7fa", fg="#2c3e50", justify="left")
        self.summary_label.pack()
        self.update_summary()

        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill='x', pady=10)

        # Navigation Buttons
        button_frame = tk.Frame(self, bg="#f5f7fa")
        button_frame.pack(pady=10)

        # Use ttk for better styling
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        # Modern buttons with uniform size
        ttk.Button(button_frame, text="➕ Add Task", width=20, command=self.open_add_task).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="📂 View Tasks", width=20, command=self.open_task_list).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="📊 Progress", width=20, command=self.open_progress).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="✏️ Edit Task", width=20, command=self.open_edit_task).grid(row=1, column=1, padx=10, pady=10)

        # Footer
        footer = tk.Label(self, text="© 2025 Task Manager", font=("Segoe UI", 9), bg="#f5f7fa", fg="#95a5a6")
        footer.pack(side="bottom", pady=10)

    def update_summary(self):
        """Update the task summary label."""
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
        completed_tasks = self.cursor.fetchone()[0]

        summary = f"📌 Total Tasks: {total_tasks}\n✅ Completed Tasks: {completed_tasks}"
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
