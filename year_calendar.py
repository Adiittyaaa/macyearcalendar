import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
# The user specified 2880x400px but called it "portrait".
# However, for a macOS wallpaper, the screen is usually 16:10 or 16:9.
# I will use 2880x1800 to ensure it covers the screen, 
# and focus the content in a way that looks beautiful.
WIDTH, HEIGHT = 2880, 1800  
BG_COLOR = (0, 0, 0)        # Minimalist Black
RED = (230, 0, 0)           # A slightly more premium red
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
CIRCLE_DIA = 24
SPACING = 12
GRID_COLS = 24
GRID_ROWS = 16
# We use a static filename for the final location to keep it simple, 
# but we'll try to force a refresh via the AppleScript.
OUTPUT_PATH = os.path.expanduser("~/Pictures/year_calendar.png")

def get_day_of_year():
    now = datetime.now()
    # Force 2026 for the requested logic if the current system date is different,
    # but the prompt says Jan 13, 2026 is the current date.
    if now.year != 2026:
        # If we are not in 2026, we'll just use the current day of year
        # but the progress will be based on 2026.
        pass
    
    start_of_year = datetime(now.year, 1, 1)
    return (now - start_of_year).days + 1

def generate_wallpaper():
    day_num = get_day_of_year()
    total_days = 365 # 2026 is not a leap year
    progress_pct = (day_num / total_days) * 100
    
    # Create Canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # --- FONTS ---
    font_path = os.path.join(os.path.dirname(__file__), "fonts/Oswald.ttf")
    try:
        # User requested Oswald
        font_main = ImageFont.truetype(font_path, 32) # Smaller, minimal
    except:
        # Fallback to Helvetica Condensed if local oswald fails
        font_main = ImageFont.load_default()
        
    # --- CALCULATE POSITIONS ---
    # User requested: "XX.X% OF 365" at the BOTTOM
    banner_text = f"{progress_pct:.1f}% OF 365"
    
    # Progress Bar (Micro-line)
    bar_h = 2 
    bar_w = 200
    bar_x = (WIDTH - bar_w) // 2
    bar_y = HEIGHT - 150 # Positioned near the bottom
    
    # Text (Above Bar)
    text_bbox = draw.textbbox((0, 0), banner_text, font=font_main)
    tw = text_bbox[2] - text_bbox[0]
    draw.text(((WIDTH - tw) // 2, bar_y - 60), banner_text, font=font_main, fill=(200, 200, 200))
    
    # Track (Very subtle)
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(30, 30, 30))
    # Fill
    if day_num > 0:
        fill_w = int(bar_w * (day_num / total_days))
        draw.rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], fill=RED)
    
    # --- DRAW GRID ---
    # Centered vertically in the main area
    grid_w = GRID_COLS * CIRCLE_DIA + (GRID_COLS - 1) * SPACING
    grid_h = GRID_ROWS * CIRCLE_DIA + (GRID_ROWS - 1) * SPACING
    
    start_x = (WIDTH - grid_w) // 2
    start_y = (HEIGHT - grid_h) // 2 - 50 # Shifted up away from bottom text
    
    for i in range(total_days):
        row = i // GRID_COLS
        col = i % GRID_COLS
        
        x0 = start_x + col * (CIRCLE_DIA + SPACING)
        y0 = start_y + row * (CIRCLE_DIA + SPACING)
        x1 = x0 + CIRCLE_DIA
        y1 = y0 + CIRCLE_DIA
        
        if (i + 1) <= day_num:
            # Past/Current days: RED filled (solid)
            draw.ellipse([x0, y0, x1, y1], fill=RED)
        else:
            # Future days: Subtle gray stroke
            draw.ellipse([x0, y0, x1, y1], outline=(60, 60, 60), width=1)
            
    # --- FOOTER REMOVED AS PER USER REQUEST ---
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"Calendar Generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_wallpaper()
