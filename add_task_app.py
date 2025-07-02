import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AddTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Add Task")
        self.geometry("400x300")
        
        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # UI
        tk.Label(self, text="Add New Task", font=("Arial", 14, "bold")).pack(pady=10)
        
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
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Save Task", width=15, command=self.save_task).pack(side="left", padx=5)
        tk.Button(button_frame, text="Close", width=15, command=self.destroy).pack(side="left", padx=5)
    
    def save_task(self):
        title = self.title_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.date_entry.get().strip()
        status = "Pending"
        
        if not title or not due_date:
            messagebox.showerror("Error", "Title and Due Date are required!")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            self.cursor.execute(
                "INSERT INTO tasks (title, priority, due_date, status) VALUES (?, ?, ?, ?)",
                (title, priority, due_date, status)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Task saved successfully!")
            self.title_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
    
    def destroy(self):
        self.conn.close()
        super().destroy()

if __name__ == "__main__":
    app = AddTaskApp()
    app.mainloop()
