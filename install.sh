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

# 4. Setup launchd (6 AM Daily)
# launchd is more reliable on macOS than cron
echo "🗓️ Setting up launchd service..."

LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.user.calendar.plist"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_NAME"
PYTHON_PATH=$(which python3)

# 4.1 Remove existing cron job if present
(crontab -l 2>/dev/null | grep -v "$PY_SCRIPT") | crontab - 2>/dev/null
echo "🗑️ Cleaned up any existing cron jobs."

# 4.2 Create plist from template
sed "s|PYTHON_PATH|$PYTHON_PATH|g; s|PY_SCRIPT|$PY_SCRIPT|g" "$SCRIPT_DIR/com.user.calendar.plist.template" > "$PLIST_PATH"

# 4.3 Load the service
# Modern launchctl commands
launchctl bootout gui/$(id -u)/com.user.calendar 2>/dev/null
launchctl bootstrap gui/$(id -u) "$PLIST_PATH"

echo "✅ launchd service loaded and scheduled for 6:00 AM daily (and on login)."
echo "✨ Installation Complete! Your wallpaper will update automatically every day at 6 AM."
echo "Check ~/Pictures/year_calendar.png for the current file."
echo "You can manually trigger an update with: launchctl kickstart -p gui/$(id -u)/com.user.calendar"
