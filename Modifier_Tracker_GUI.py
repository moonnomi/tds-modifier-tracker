import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# The Master List
MODIFIERS = [
    "Speedy", "Glass", "Quarantine", "Fog", "Limit", 
    "Flying", "Jailed", "Exploding", "Inflation", "Commited", 
    "Hidden", "Broke", "Healthy"
]

# Your provided anchor
ANCHOR_TIME = datetime(2026, 2, 20, 19, 0)
ANCHOR_MODIFIER = "Exploding"
INTERVAL_HOURS = 3

class ModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modifier Trial Scheduler")
        self.root.geometry("700x500")
        
        # Track which modifiers are selected via BooleanVars
        self.selection_vars = {mod: tk.BooleanVar(value=(mod in ["Commited", "Glass", "Quarantine"])) 
                              for mod in MODIFIERS}
        
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # Main Layout: Left Sidebar for selection, Right for Results
        sidebar = ttk.LabelFrame(self.root, text=" Select Modifiers ", padding="10")
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        for mod in MODIFIERS:
            cb = ttk.Checkbutton(sidebar, text=mod, variable=self.selection_vars[mod], command=self.refresh_data)
            cb.pack(anchor=tk.W, pady=2)

        content = ttk.Frame(self.root, padding="10")
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(content, text="Upcoming Occurrences (Next 5 Each)", font=('Segoe UI', 11, 'bold')).pack(pady=(0, 10))
        
        # Table Styling
        self.tree = ttk.Treeview(content, columns=("Modifier", "Time", "Status"), show='headings')
        self.tree.heading("Modifier", text="Modifier")
        self.tree.heading("Time", text="Date & Time")
        self.tree.heading("Status", text="Status")
        self.tree.column("Modifier", width=100)
        self.tree.column("Time", width=180)
        self.tree.column("Status", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(content, text="Manual Refresh", command=self.refresh_data).pack(pady=10)

    def get_rotation_data(self):
        now = datetime.now()
        # Calculate how many seconds have passed since the anchor
        diff_seconds = (now - ANCHOR_TIME).total_seconds()
        
        # Total 3-hour slots since anchor
        total_slots_passed = int(diff_seconds // (INTERVAL_HOURS * 3600))
        
        # Current index in the list
        anchor_idx = MODIFIERS.index(ANCHOR_MODIFIER)
        current_idx = (anchor_idx + total_slots_passed) % len(MODIFIERS)
        
        # Find when the CURRENT slot ends
        seconds_into_current = diff_seconds % (INTERVAL_HOURS * 3600)
        seconds_remaining = (INTERVAL_HOURS * 3600) - seconds_into_current
        current_slot_end = now + timedelta(seconds=seconds_remaining)
        current_slot_start = now - timedelta(seconds=seconds_into_current)
        
        return current_idx, current_slot_start

    def refresh_data(self):
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        current_idx, current_start = self.get_rotation_data()
        active_targets = [mod for mod, var in self.selection_vars.items() if var.get()]
        
        if not active_targets:
            return

        results = []
        # Look ahead 200 slots to ensure we find 5 occurrences for even the rarest selection
        for i in range(200):
            check_idx = (current_idx + i) % len(MODIFIERS)
            mod_name = MODIFIERS[check_idx]
            
            if mod_name in active_targets:
                occurrence_start = current_start + timedelta(hours=i * INTERVAL_HOURS)
                
                status = "Upcoming"
                if i == 0:
                    status = "LIVE NOW"
                
                results.append((mod_name, occurrence_start, status))

        # Filter to only show the next 5 for each selected modifier
        final_list = []
        counts = {mod: 0 for mod in active_targets}
        
        for mod, time, status in results:
            if counts[mod] < 5:
                final_list.append((mod, time, status))
                counts[mod] += 1
        
        # Sort the final filtered list by time so it's chronological
        final_list.sort(key=lambda x: x[1])

        for mod, time, status in final_list:
            tag = 'live' if status == "LIVE NOW" else ''
            self.tree.insert("", tk.END, values=(mod, time.strftime("%b %d, %H:%M"), status), tags=(tag,))
        
        self.tree.tag_configure('live', foreground='green', font=('Segoe UI', 10, 'bold'))

if __name__ == "__main__":
    root = tk.Tk()
    # Set a modern theme if available
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = ModifierApp(root)
    root.mainloop()