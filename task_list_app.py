import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TaskListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Task List")
        self.geometry("600x400")
        
        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # UI
        tk.Label(self, text="Task List", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.tree = ttk.Treeview(self, columns=("Title", "Priority", "Due Date", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        self.tree.column("Title", width=200)
        self.tree.column("Priority", width=100)
        self.tree.column("Due Date", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack(pady=10, fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Refresh List", width=15, command=self.refresh_tasks).pack(side="left", padx=5)
        tk.Button(button_frame, text="Close", width=15, command=self.destroy).pack(side="left", padx=5)
        
        self.refresh_tasks()
    
    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.cursor.execute("SELECT title, priority, due_date, status FROM tasks")
        tasks = self.cursor.fetchall()
        if not tasks:
            messagebox.showinfo("Info", "No tasks found.")
        else:
            for task in tasks:
                self.tree.insert("", tk.END, values=task)
    
    def destroy(self):
        self.conn.close()
        super().destroy()

if __name__ == "__main__":
    app = TaskListApp()
    app.mainloop()
