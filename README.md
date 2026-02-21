# ⬡ TDS Modifier Tracker

A premium, cyberpunk-themed HTML-based GUI designed to track current and future modifier trials in the Roblox experience **Tower Defense Simulator (TDS)**.

![Aesthetic Preview](https://via.placeholder.com/800x450/05070a/00d4ff?text=TDS+Modifier+Tracker+v2.1)

## 🌟 Features

- **Global Synchronization**: Uses a UTC-based anchor to ensure the rotation is identical for every user worldwide.
- **Local Timezone Intelligence**: Automatically detects the viewer's local timezone and displays window starts and countdowns relative to their local clock.
- **Tactical Filtering**: Select specific modifiers to track (Speedy, Glass, Hidden, etc.) and see their next 5 appearances.
- **Cyberpunk Aesthetics**: Featuring glassmorphism, neon accents, and a "Rotation Intelligence" interface built with modern CSS.
- **Persistent Settings**: Your tactical filter selections are saved locally in your browser.

## 🛠️ Technology Stack

- **Core**: Semantic HTML5 & Vanilla JavaScript
- **Styling**: Modern CSS3 (Grid, Flexbox, Clip-paths)
- **Icons**: SVG Data URIs for zero-latency loading.
- **Deployment**: Single-file architecture (HTML) for easy portability.

## 🚀 Usage

Simply open `index.html` in any modern web browser. 

1. **Clock**: The top-right shows your current local time and timezone offset.
2. **Filters**: Use the sidebar to toggle specific modifiers you want to monitor.
3. **Timeline**: The main table shows exactly when your selected modifiers will go live, including a live countdown.

## 📡 Rotation Logic

The site follows a strict 3-hour rotation pattern synchronized to a global UTC anchor. This ensures that when the site says a modifier is "Live," it is live for everyone in the game simultaneously.

---

*Developed for the TDS Community.*
