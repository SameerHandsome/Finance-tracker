import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class EditTaskApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Task Manager - Edit Task")
        self.geometry("400x350")
        
        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # UI
        tk.Label(self, text="Edit Task", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Task selection
        tk.Label(self, text="Select Task:", font=("Arial", 10)).pack(pady=5)
        self.task_var = tk.StringVar()
        self.task_dropdown = ttk.Combobox(self, textvariable=self.task_var, width=30, state="readonly")
        self.task_dropdown.pack(pady=5)
        self.task_dropdown.bind("<<ComboboxSelected>>", self.load_task_details)
        self.load_task_options()
        
        # Input fields
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Title:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Priority:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Low")
        tk.OptionMenu(form_frame, self.priority_var, "Low", "Medium", "High").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=30)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Status:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.status_var = tk.StringVar(value="Pending")
        tk.OptionMenu(form_frame, self.status_var, "Pending", "Completed").grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Update Task", width=15, command=self.update_task).pack(side="left", padx=5)
        tk.Button(button_frame, text="Close", width=15, command=self.destroy).pack(side="left", padx=5)
    
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
            messagebox.showerror("Error", "Title and Due Date are required!")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            self.cursor.execute(
                "UPDATE tasks SET title = ?, priority = ?, due_date = ?, status = ? WHERE id = ?",
                (title, priority, due_date, status, task_id)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Task updated successfully!")
            self.load_task_options()  # Refresh dropdown
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
    
    def destroy(self):
        self.conn.close()
        super().destroy()

if _name_ == "_main_":
    app = EditTaskApp()
    app.mainloop()