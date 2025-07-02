import tkinter as tk
from tkinter import messagebox
import sqlite3

class ProgressApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Task Manager - Progress")
        self.geometry("400x300")
        
        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # UI
        tk.Label(self, text="Task Progress", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.stats_text = tk.Text(self, height=5, width=40, font=("Arial", 10))
        self.stats_text.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Show Stats", width=15, command=self.show_stats).pack(side="left", padx=5)
        tk.Button(button_frame, text="Close", width=15, command=self.destroy).pack(side="left", padx=5)
        
        self.show_stats()
    
    def show_stats(self):
        self.stats_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        results = self.cursor.fetchall()
        
        if not results:
            self.stats_text.insert(tk.END, "No tasks available.")
        else:
            stats = "Task Counts by Status:\n\n"
            for status, count in results:
                stats += f"{status}: {count} tasks\n"
            self.stats_text.insert(tk.END, stats)
    
    def destroy(self):
        self.conn.close()
        super().destroy()

if _name_ == "_main_":
    app = ProgressApp()
    app.mainloop()