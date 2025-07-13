import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ProgressApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager - Progress")
        self.geometry("460x350")
        self.configure(bg="#f5f7fa")

        # Initialize database
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()

        # Header
        tk.Label(self, text="📊 Task Progress", font=("Segoe UI", 16, "bold"),
                 bg="#f5f7fa", fg="#2c3e50").pack(pady=20)

        # Statistics Display
        self.stats_text = tk.Text(self, height=8, width=50, font=("Segoe UI", 10),
                                  bg="#ffffff", fg="#2c3e50", relief="flat", wrap="word")
        self.stats_text.pack(padx=20, pady=10)
        self.stats_text.configure(state="disabled")

        # Button Frame
        button_frame = tk.Frame(self, bg="#f5f7fa")
        button_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        ttk.Button(button_frame, text="🔍 Show Stats", style="Accent.TButton", width=18,
                   command=self.show_stats).pack(side="left", padx=10)
        ttk.Button(button_frame, text="❌ Close", width=18,
                   command=self.close_window).pack(side="left", padx=10)

        self.show_stats()

    def show_stats(self):
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", tk.END)

        try:
            self.cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
            results = self.cursor.fetchall()

            if not results:
                self.stats_text.insert(tk.END, "No tasks available.\n")
            else:
                total_tasks = sum([count for _, count in results])
                stats_output = "📈 Task Counts by Status:\n\n"
                for status, count in results:
                    percentage = (count / total_tasks) * 100 if total_tasks > 0 else 0
                    stats_output += f"• {status}: {count} tasks ({percentage:.1f}%)\n"

                # Add summary
                stats_output += f"\n🧮 Total Tasks: {total_tasks}"
                self.stats_text.insert(tk.END, stats_output)

        except Exception as e:
            self.stats_text.insert(tk.END, f"An error occurred: {e}")

        self.stats_text.configure(state="disabled")

    def close_window(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = ProgressApp()
    app.mainloop()
