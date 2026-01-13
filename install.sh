#!/bin/bash

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PY_SCRIPT="$SCRIPT_DIR/year_calendar.py"
APPLE_SCRIPT="$SCRIPT_DIR/set_wallpaper.scpt"

echo "🚀 Installing Dynamic Year Calendar Wallpaper System..."

# 1. Install Dependencies
echo "📦 Checking Pillow..."
python3 -m pip install Pillow --quiet

# 2. Run first generation
echo "🖼️ Generating first wallpaper..."
python3 "$PY_SCRIPT"

# 3. Set wallpaper immediately
echo "🖥️ Setting desktop picture..."
osascript "$APPLE_SCRIPT"

# 4. Setup Cron Job (6 AM Daily)
# We use absolute paths for cron reliability
PYTHON_PATH=$(which python3)
CRON_CMD="0 6 * * * $PYTHON_PATH $PY_SCRIPT && /usr/bin/osascript $APPLE_SCRIPT"

# Check if cron already exists
(crontab -l 2>/dev/null | grep -F "$PY_SCRIPT") > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Cron job already exists."
else
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "📅 Cron job scheduled for 6:00 AM daily."
fi

echo "✨ Installation Complete! Your wallpaper will update automatically every day at 6 AM."
echo "Check ~/Pictures/year_calendar.png for the current file."
