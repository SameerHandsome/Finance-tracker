import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TaskListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Task List")
        self.geometry("600x400")
        
        # Connect to database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # Title Label
        title_label = tk.Label(self, text="Task List", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Treeview setup
        self.task_view = ttk.Treeview(self, columns=("Title", "Priority", "Due Date", "Status"), show="headings")
        headings = [("Title", 200), ("Priority", 100), ("Due Date", 100), ("Status", 100)]
        for col_name, col_width in headings:
            self.task_view.heading(col_name, text=col_name)
            self.task_view.column(col_name, width=col_width)

        self.task_view.pack(pady=10, fill="both", expand=True)
        
        # Button Frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        refresh_btn = tk.Button(button_frame, text="Refresh List", width=15, command=self.load_tasks)
        refresh_btn.pack(side="left", padx=5)

        close_btn = tk.Button(button_frame, text="Close", width=15, command=self.close_app)
        close_btn.pack(side="left", padx=5)
        
        self.load_tasks()
    
    def load_tasks(self):
        # Clear existing entries
        for item in self.task_view.get_children():
            self.task_view.delete(item)
        
        self.cursor.execute("SELECT title, priority, due_date, status FROM tasks")
        tasks = self.cursor.fetchall()
        
        if not tasks:
            messagebox.showinfo("Info", "No tasks found.")
        else:
            for task in tasks:
                self.task_view.insert("", tk.END, values=task)
    
    def close_app(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = TaskListApp()
    app.mainloop()
