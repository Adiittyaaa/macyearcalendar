# 🦷 2026 Year-at-a-Glance Wallpaper

Dynamic Motivation for **Dentistry Excellence**. 
*13/365 days → revenue target progress.*

## Features
- **365-Circle Grid**: Tracks every day of 2026.
- **Auto-Update**: Updates daily at 6:00 AM via macOS Cron.
- **Progress Metrics**: Top banner shows percentage complete.
- **Minimalist Aesthetic**: Clean black background with Retina-sharp circles.

## Installation
Just run the install script:
```bash
chmod +x install.sh
./install.sh
```

## Structure
- `year_calendar.py`: The heart of the system. Generates the PNG.
- `set_wallpaper.scpt`: AppleScript to apply the wallpaper.
- `install.sh`: Setup script for scheduling.
- `~/Pictures/year_calendar.png`: The output wallpaper file.

## Customization
You can edit `year_calendar.py` to change:
- `RED`: The fill color for passed days.
- `FOOTER_TEXT`: Current clinic details.
- `CIRCLE_DIA`: Size of the calendar circles.

---
*yourclinic@kalyan.com*
