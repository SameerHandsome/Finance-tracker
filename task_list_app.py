import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TaskListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Task List")
        self.geometry("700x450")
        self.configure(bg="#f5f7fa")

        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()

        # Header
        tk.Label(self, text="📋 Task List", font=("Segoe UI", 16, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=20)

        # Treeview Frame (with scrollbar)
        tree_frame = tk.Frame(self, bg="#f5f7fa")
        tree_frame.pack(padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("Title", "Priority", "Due Date", "Status"), show="headings", height=15)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")

        self.tree.column("Title", anchor="w", width=250)
        self.tree.column("Priority", anchor="center", width=100)
        self.tree.column("Due Date", anchor="center", width=120)
        self.tree.column("Status", anchor="center", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Buttons
        button_frame = tk.Frame(self, bg="#f5f7fa")
        button_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        ttk.Button(button_frame, text="🔄 Refresh List", style="Accent.TButton", width=18,
                   command=self.refresh_tasks).pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Close", width=18,
                   command=self.close_window).pack(side="left", padx=10)

        # Load tasks on start
        self.refresh_tasks()

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute("SELECT title, priority, due_date, status FROM tasks")
            tasks = self.cursor.fetchall()

            if not tasks:
                messagebox.showinfo("Info", "No tasks found.")
            else:
                for task in tasks:
                    self.tree.insert("", tk.END, values=task)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while loading tasks:\n{e}")

    def close_window(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = TaskListApp()
    app.mainloop()
