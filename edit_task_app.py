import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class EditTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Edit Task")
        self.geometry("480x420")
        self.configure(bg="#f5f7fa")

        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()

        # Header
        tk.Label(self, text="✏️ Edit Task", font=("Segoe UI", 16, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=20)

        # Task Selection
        tk.Label(self, text="Select Task:", font=("Segoe UI", 10),
                 bg="#f5f7fa").pack()
        self.task_var = tk.StringVar()
        self.task_dropdown = ttk.Combobox(self, textvariable=self.task_var, width=45, state="readonly")
        self.task_dropdown.pack(pady=5)
        self.task_dropdown.bind("<<ComboboxSelected>>", self.load_task_details)

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

        # Status
        tk.Label(form_frame, text="Status:", font=("Segoe UI", 10),
                 bg="#f5f7fa", anchor="w", width=18).grid(row=3, column=0, padx=10, pady=8, sticky="e")
        self.status_var = tk.StringVar(value="Pending")
        self.status_menu = ttk.Combobox(form_frame, textvariable=self.status_var, state="readonly", width=28)
        self.status_menu['values'] = ("Pending", "Completed")
        self.status_menu.grid(row=3, column=1, padx=5, pady=8)

        # Buttons
        button_frame = tk.Frame(self, bg="#f5f7fa")
        button_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        ttk.Button(button_frame, text="🔄 Update Task", style="Accent.TButton", width=18,
                   command=self.update_task).pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Close", width=18,
                   command=self.close_window).pack(side="left", padx=10)

        # Load tasks into dropdown
        self.load_task_options()

    def load_task_options(self):
        self.cursor.execute("SELECT id, title FROM tasks")
        tasks = self.cursor.fetchall()
        if tasks:
            self.task_dropdown["values"] = [f"{task[0]}: {task[1]}" for task in tasks]
            self.task_var.set(self.task_dropdown["values"][0])
            self.load_task_details(None)
        else:
            self.task_dropdown["values"] = []
            self.task_var.set("")
            messagebox.showinfo("Info", "No tasks available to edit.")

    def load_task_details(self, event):
        if not self.task_var.get():
            return
        task_id = self.task_var.get().split(":")[0]
        self.cursor.execute("SELECT title, priority, due_date, status FROM tasks WHERE id = ?", (task_id,))
        task = self.cursor.fetchone()
        if task:
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, task[0])
            self.priority_var.set(task[1])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, task[2])
            self.status_var.set(task[3])

    def update_task(self):
        if not self.task_var.get():
            messagebox.showerror("Error", "No task selected!")
            return

        task_id = self.task_var.get().split(":")[0]
        title = self.title_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.date_entry.get().strip()
        status = self.status_var.get()

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
                "UPDATE tasks SET title = ?, priority = ?, due_date = ?, status = ? WHERE id = ?",
                (title, priority, due_date, status, task_id)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Task updated successfully.")
            self.load_task_options()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred:\n{e}")

    def close_window(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = EditTaskApp()
    app.mainloop()
