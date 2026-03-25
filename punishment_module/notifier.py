# punishment_module/notifier.py

import tkinter as tk
from tkinter import ttk
import threading

def show_popup_notification(reminders=None, strikes=None, duration=20):
    """
    Show a cross-platform popup window with reminder and strike task info.
    This runs in a separate thread and auto-closes after `duration` seconds.
    """
    reminders = reminders or []
    strikes = strikes or []

    def _build_popup():
        root = tk.Tk()
        root.title("LazyBomb Notification")
        root.attributes("-topmost", True)
        root.geometry("400x500")

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10), anchor="w", justify="left")

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        if reminders:
            ttk.Label(frame, text="🔔 Upcoming Tasks (Due < 15 min):", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))
            for task in reminders:
                text = f"- {task.get('task')} (due: {task.get('deadline')})"
                ttk.Label(frame, text=text, foreground="blue").pack(anchor="w")

        if strikes:
            ttk.Label(frame, text="☠️ Overdue Tasks (Missed > 15 min):", font=("Segoe UI", 11, "bold"), padding=(0, 10, 0, 0)).pack(anchor="w")
            for task in strikes:
                text = f"- {task.get('task')} (due: {task.get('deadline')})"
                ttk.Label(frame, text=text, foreground="red").pack(anchor="w")

        # Auto-close after duration seconds
        root.after(duration * 1000, root.destroy)
        root.mainloop()

    # Run in a thread so it doesn't block APScheduler or main app
    threading.Thread(target=_build_popup, daemon=True).start()
