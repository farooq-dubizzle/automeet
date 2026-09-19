import os
import sys

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

FROZEN = getattr(sys, "frozen", False)
_MAC_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_MAC_DIR)

APP_DATA_DIR = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "AutoMeet")
os.makedirs(APP_DATA_DIR, exist_ok=True)
TOKEN_FILE = os.path.join(APP_DATA_DIR, "automeet_token.json")
LOCK_FILE = os.path.join(APP_DATA_DIR, ".automeet.lock")

_BASE = getattr(sys, "_MEIPASS", _ROOT)
ICON_PATH = os.path.join(_BASE, "assets", "icon.png")
APP_NAME = "AutoMeet"

CALENDAR_POLL_INTERVAL_SEC = 60
SCHEDULER_TICK_SEC = 10
JOIN_WINDOW_BEFORE_SEC = 10
JOIN_WINDOW_AFTER_SEC = 120

ACCESS_DENIED_MSG = (
    "You don't have access to AutoMeet yet.\n"
    "Contact the app developer to be added."
)

if FROZEN:
    CREDENTIALS_FILE = os.path.join(_BASE, "credentials.json")
else:
    CREDENTIALS_FILE = os.path.join(_ROOT, "credentials.json")
