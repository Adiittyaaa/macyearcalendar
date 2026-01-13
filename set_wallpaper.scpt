-- set_wallpaper.scpt
set wallpaperPath to (POSIX path of (path to home folder)) & "Pictures/year_calendar.png"
tell application "System Events"
    repeat with aDesktop in desktops
        set picture of aDesktop to wallpaperPath
    end repeat
end tell
