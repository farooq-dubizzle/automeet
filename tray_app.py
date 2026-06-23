import os
import threading

import pystray
from PIL import Image, ImageDraw

from calendar_client import parse_event_start
from link_extractor import extract_meeting_url
from config import ICON_PATH, APP_NAME


def _load_icon():
    if os.path.exists(ICON_PATH):
        return Image.open(ICON_PATH).convert("RGBA")
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=(34, 197, 94, 255))  # green circle
    draw.text((18, 18), "M", fill=(255, 255, 255, 255))
    return img


def _format_title(event):
    try:
        start_dt = parse_event_start(event).astimezone()
        time_str = start_dt.strftime("%H:%M")
    except Exception:
        time_str = "??:??"
    summary = (event.get("summary") or "Untitled")[:40]
    has_url = extract_meeting_url(event) is not None
    suffix = "" if has_url else " (no link)"
    return f"{time_str}  {summary}{suffix}"


class TrayApp:
    def __init__(self):
        self._events = []
        self._enabled = {}  # event_id -> bool
        self._lock = threading.Lock()
        self._icon = None
        self._scheduler = None  # set by main.py after construction

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def update_events(self, events):
        with self._lock:
            new_ids = {e["id"] for e in events}
            old_ids = set(self._enabled.keys())
            for eid in new_ids - old_ids:
                self._enabled[eid] = True
            for eid in old_ids - new_ids:
                del self._enabled[eid]
            self._events = sorted(events, key=lambda e: e["start"].get("dateTime", ""))
        if self._icon:
            self._icon.update_menu()

    def get_enabled_events(self):
        with self._lock:
            return [e for e in self._events if self._enabled.get(e["id"], True)]

    def _toggle(self, event_id):
        with self._lock:
            self._enabled[event_id] = not self._enabled.get(event_id, True)
        if self._icon:
            self._icon.update_menu()

    def _make_action(self, eid):
        def action(icon, item):
            self._toggle(eid)
        return action

    def _make_checked(self, eid):
        def checked(item):
            return self._enabled.get(eid, True)
        return checked

    def _build_menu(self):
        items = []
        with self._lock:
            events_snapshot = list(self._events)

        if not events_snapshot:
            items.append(pystray.MenuItem("No meetings today", None, enabled=False))
        else:
            for event in events_snapshot:
                eid = event["id"]
                title = _format_title(event)
                items.append(
                    pystray.MenuItem(
                        title,
                        action=self._make_action(eid),
                        checked=self._make_checked(eid),
                    )
                )

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Refresh", self._on_refresh))
        items.append(pystray.MenuItem("Quit", self._on_quit))
        return items

    def _on_refresh(self, icon, item):
        if self._scheduler:
            self._scheduler.force_refresh()

    def _on_quit(self, icon, item):
        icon.stop()

    def run(self):
        self._icon = pystray.Icon(
            APP_NAME,
            _load_icon(),
            APP_NAME,
            menu=pystray.Menu(self._build_menu),
        )
        self._icon.run()
