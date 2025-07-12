import tkinter as tk
from tkinter import messagebox
import sqlite3

class ProgressApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Progress")
        self.geometry("400x300")
        
        # Connect to database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        
        # Title Label
        title_label = tk.Label(self, text="Task Progress", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Text area for statistics
        self.output_text = tk.Text(self, height=6, width=45, font=("Arial", 10))
        self.output_text.pack(pady=10)
        
        # Button Frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        show_button = tk.Button(button_frame, text="Show Stats", width=15, command=self.show_stats)
        show_button.pack(side="left", padx=5)
        
        close_button = tk.Button(button_frame, text="Close", width=15, command=self.close_app)
        close_button.pack(side="left", padx=5)
        
        self.show_stats()

    def show_stats(self):
        self.output_text.delete("1.0", tk.END)
        self.cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
        results = self.cursor.fetchall()
        
        if not results:
            self.output_text.insert(tk.END, "No tasks available.")
        else:
            self.output_text.insert(tk.END, "Task Counts by Status:\n\n")
            for status, count in results:
                self.output_text.insert(tk.END, f"{status}: {count} task(s)\n")

    def close_app(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = ProgressApp()
    app.mainloop()
