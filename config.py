import os
import sys

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = r"C:\Users\farooq.mirza\Documents\automeet_creds.json"
# When frozen as exe, store token next to the exe. Otherwise next to main.py.
_APP_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(_APP_DIR, "automeet_token.json")

CALENDAR_POLL_INTERVAL_SEC = 60  # 1 minute
SCHEDULER_TICK_SEC = 10
JOIN_WINDOW_SEC = 0  # join within ±30s of exact start time

# Resolve asset paths correctly both when running as script and as PyInstaller exe
_BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ICON_PATH = os.path.join(_BASE, "assets", "icon.png")
APP_NAME = "AutoMeet"
