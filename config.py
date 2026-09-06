import os
import sys

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

FROZEN = getattr(sys, "frozen", False)
_APP_DIR = os.path.dirname(sys.executable) if FROZEN else os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(_APP_DIR, "automeet_token.json")

_BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ICON_PATH = os.path.join(_BASE, "assets", "icon.png")
APP_NAME = "AutoMeet"

CALENDAR_POLL_INTERVAL_SEC = 60
SCHEDULER_TICK_SEC = 10

ACCESS_DENIED_MSG = (
    "You don't have access to AutoMeet yet.\n"
    "Contact the app developer to be added."
)

if FROZEN:
    CREDENTIALS_FILE = os.path.join(_BASE, "credentials.json")
else:
    CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
