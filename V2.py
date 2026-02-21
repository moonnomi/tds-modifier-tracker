import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# THE CORRECTED SEQUENCE
MODIFIERS = [
    "Speedy", "Glass", "Quarantine", "Fog", "Limit", 
    "Flying", "Jailed", "Exploding", "Inflation", 
    "Commited", "Hidden", "Broke", "Healthy"
]

ANCHOR_TIME = datetime(2026, 2, 20, 19, 0)
ANCHOR_MODIFIER = "Exploding"
INTERVAL_HOURS = 3

class ModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modifier Trial Scheduler")
        self.root.geometry("850x500")
        
        self.selection_vars = {mod: tk.BooleanVar(value=(mod in ["Commited", "Glass", "Quarantine"])) 
                              for mod in MODIFIERS}
        
        self.setup_ui()
        self.auto_refresh()

    def setup_ui(self):
        sidebar = ttk.LabelFrame(self.root, text=" Target Modifiers ", padding="10")
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        for mod in MODIFIERS:
            ttk.Checkbutton(sidebar, text=mod, variable=self.selection_vars[mod], 
                            command=self.refresh_data).pack(anchor=tk.W, pady=2)

        content = ttk.Frame(self.root, padding="10")
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_now = ttk.Label(content, text="", font=('Segoe UI', 10, 'italic'))
        self.label_now.pack(pady=(0, 10))
        
        self.tree = ttk.Treeview(content, columns=("Modifier", "Time", "Countdown", "Status"), show='headings')
        self.tree.heading("Modifier", text="Modifier")
        self.tree.heading("Time", text="Date & Time")
        self.tree.heading("Countdown", text="Starts In")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Modifier", width=100)
        self.tree.column("Time", width=150)
        self.tree.column("Countdown", width=150)
        self.tree.column("Status", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def get_rotation_data(self):
        now = datetime.now()
        diff_seconds = (now - ANCHOR_TIME).total_seconds()
        
        total_slots_passed = int(diff_seconds // (INTERVAL_HOURS * 3600))
        anchor_idx = MODIFIERS.index(ANCHOR_MODIFIER)
        current_idx = (anchor_idx + total_slots_passed) % len(MODIFIERS)
        
        seconds_into_current = diff_seconds % (INTERVAL_HOURS * 3600)
        current_slot_start = now - timedelta(seconds=seconds_into_current)
        
        return current_idx, current_slot_start

    def format_countdown(self, target_time):
        now = datetime.now()
        if target_time <= now:
            return "Active"
        
        diff = target_time - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Build string dynamically to avoid "0d" clutter if you prefer
        parts = []
        if days > 0: parts.append(f"{days}d")
        if hours > 0 or days > 0: parts.append(f"{hours}h")
        parts.append(f"{minutes}m")
        
        return " ".join(parts)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        now = datetime.now()
        self.label_now.config(text=f"Current Time: {now.strftime('%b %d, %H:%M:%S')}")
        
        current_idx, current_start = self.get_rotation_data()
        active_targets = [mod for mod, var in self.selection_vars.items() if var.get()]
        
        results = []
        # Check far enough ahead to find 5 instances (13 mods * 5 * 3 hrs = ~200 slots)
        for i in range(250): 
            check_idx = (current_idx + i) % len(MODIFIERS)
            mod_name = MODIFIERS[check_idx]
            
            if mod_name in active_targets:
                occurrence_start = current_start + timedelta(hours=i * INTERVAL_HOURS)
                status = "Upcoming"
                if i == 0: status = "LIVE NOW"
                results.append((mod_name, occurrence_start, status))

        counts = {mod: 0 for mod in active_targets}
        final_list = []
        for mod, time, status in results:
            if counts[mod] < 5:
                final_list.append((mod, time, status))
                counts[mod] += 1
        
        final_list.sort(key=lambda x: x[1])

        for mod, time, status in final_list:
            countdown = self.format_countdown(time)
            tag = 'live' if status == "LIVE NOW" else ''
            self.tree.insert("", tk.END, values=(mod, time.strftime("%b %d, %H:%M"), countdown, status), tags=(tag,))
        
        self.tree.tag_configure('live', foreground='#2ecc71', font=('Segoe UI', 10, 'bold'))

    def auto_refresh(self):
        self.refresh_data()
        self.root.after(30000, self.auto_refresh)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names(): style.theme_use("clam")
    app = ModifierApp(root)
    root.mainloop()