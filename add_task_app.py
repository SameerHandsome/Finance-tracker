import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AddTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Add Task")
        self.geometry("440x350")
        self.configure(bg="#f5f7fa")

        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()

        # Header
        tk.Label(self, text="➕ Add New Task", font=("Segoe UI", 16, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=20)

        # Form Frame
        form_frame = tk.Frame(self, bg="#f5f7fa")
        form_frame.pack(pady=10)

        # Title
        tk.Label(form_frame, text="Title:", font=("Segoe UI", 10),
                 bg="#f5f7fa", anchor="w", width=18).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.title_entry = ttk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=8)

        # Priority
        tk.Label(form_frame, text="Priority:", font=("Segoe UI", 10),
                 bg="#f5f7fa", anchor="w", width=18).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.priority_var = tk.StringVar(value="Low")
        self.priority_menu = ttk.Combobox(form_frame, textvariable=self.priority_var, state="readonly", width=28)
        self.priority_menu['values'] = ("Low", "Medium", "High")
        self.priority_menu.grid(row=1, column=1, padx=5, pady=8)

        # Due Date
        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):", font=("Segoe UI", 10),
                 bg="#f5f7fa", anchor="w", width=18).grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.grid(row=2, column=1, padx=5, pady=8)

        # Button Frame
        button_frame = tk.Frame(self, bg="#f5f7fa")
        button_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        ttk.Button(button_frame, text="💾 Save Task", style="Accent.TButton", width=18,
                   command=self.save_task).pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Close", width=18,
                   command=self.close_window).pack(side="left", padx=10)

    def save_task(self):
        title = self.title_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.date_entry.get().strip()
        status = "Pending"

        if not title or not due_date:
            messagebox.showerror("Validation Error", "Title and Due Date are required.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date Format", "Please enter the date in YYYY-MM-DD format.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO tasks (title, priority, due_date, status) VALUES (?, ?, ?, ?)",
                (title, priority, due_date, status)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Task saved successfully.")
            self.title_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while saving the task:\n{e}")

    def close_window(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = AddTaskApp()
    app.mainloop()
