import threading
from datetime import datetime

import pystray
from PIL import Image

from calendar_client import extract_meeting_url, get_todays_events, parse_event_start
from mac.config import APP_NAME, ICON_PATH
from mac.platform import open_url


def _load_icon():
    return Image.open(ICON_PATH).convert("RGBA")


def _meeting_time(event):
    try:
        return parse_event_start(event).astimezone().strftime("%H:%M")
    except Exception:
        return "??:??"


def _meeting_summary(event):
    return (event.get("summary") or "Untitled")[:34]


def _meeting_title(event, enabled):
    title = f"{_meeting_time(event)} - {_meeting_summary(event)}"
    if enabled:
        return f"{title} (auto-join on)"
    return title


class TrayApp:
    def __init__(self):
        self._events = []
        self._enabled = {}
        self._show_all_meetings = False
        self._lock = threading.Lock()
        self._icon = None
        self._scheduler = None

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def _dispatch_menu_update(self):
        if not self._icon:
            return
        icon = self._icon

        def update():
            try:
                icon.update_menu()
            except Exception:
                pass

        try:
            from Foundation import NSOperationQueue

            NSOperationQueue.mainQueue().addOperationWithBlock_(update)
        except Exception:
            if threading.current_thread() is threading.main_thread():
                update()

    def _refresh_menu(self):
        if threading.current_thread() is threading.main_thread():
            if self._icon:
                self._icon.update_menu()
        else:
            self._dispatch_menu_update()

    def update_events(self, events):
        with self._lock:
            new_ids = {e["id"] for e in events}
            old_ids = set(self._enabled.keys())
            for eid in new_ids - old_ids:
                self._enabled[eid] = True
            for eid in old_ids - new_ids:
                del self._enabled[eid]
            self._events = sorted(events, key=lambda e: e["start"].get("dateTime", ""))
        self._refresh_menu()

    def get_enabled_events(self):
        with self._lock:
            return [e for e in self._events if self._enabled.get(e["id"], True)]

    def _visible_events(self, events):
        if self._show_all_meetings:
            return events
        now = datetime.now().astimezone()
        visible = []
        for event in events:
            try:
                if parse_event_start(event).astimezone() >= now:
                    visible.append(event)
            except Exception:
                visible.append(event)
        return visible

    def _toggle_show_filter(self, icon, item):
        with self._lock:
            self._show_all_meetings = not self._show_all_meetings
        self._refresh_menu()

    def _toggle(self, event_id):
        with self._lock:
            self._enabled[event_id] = not self._enabled.get(event_id, True)
        self._refresh_menu()

    def _make_toggle_action(self, event_id):
        def action(icon, item):
            self._toggle(event_id)

        return action

    def _make_join_action(self, event):
        def action(icon, item):
            url = extract_meeting_url(event)
            if not url:
                return
            open_url(url)
            if self._scheduler:
                self._scheduler.mark_joined(event["id"], url)

        return action

    def _build_menu_items(self):
        items = [
            pystray.MenuItem("Today's Meetings", None, enabled=False),
            pystray.Menu.SEPARATOR,
        ]

        with self._lock:
            events_snapshot = list(self._events)
            enabled_snapshot = dict(self._enabled)
            show_all = self._show_all_meetings

        if show_all:
            items.append(pystray.MenuItem("Show future meetings only", self._toggle_show_filter))
        else:
            items.append(pystray.MenuItem("Show all meetings today", self._toggle_show_filter))
        items.append(pystray.Menu.SEPARATOR)

        visible_events = self._visible_events(events_snapshot)

        if not visible_events:
            if not events_snapshot:
                empty_label = "No meetings scheduled today"
            elif show_all:
                empty_label = "No meetings scheduled today"
            else:
                empty_label = "No upcoming meetings today"
            items.append(pystray.MenuItem(empty_label, None, enabled=False))
        else:
            for index, event in enumerate(visible_events):
                eid = event["id"]
                enabled = enabled_snapshot.get(eid, True)
                url = extract_meeting_url(event)

                items.append(
                    pystray.MenuItem(
                        _meeting_title(event, enabled),
                        self._make_join_action(event) if url else None,
                        default=True,
                        enabled=bool(url),
                    )
                )

                if url:
                    items.append(pystray.MenuItem("   Join Now", self._make_join_action(event)))
                else:
                    items.append(pystray.MenuItem("   No meeting link", None, enabled=False))

                if enabled:
                    items.append(
                        pystray.MenuItem(
                            "   Turn Off Auto-join",
                            self._make_toggle_action(eid),
                        )
                    )
                else:
                    items.append(
                        pystray.MenuItem(
                            "   Turn On Auto-join",
                            self._make_toggle_action(eid),
                        )
                    )

                if index < len(visible_events) - 1:
                    items.append(pystray.Menu.SEPARATOR)

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Refresh Calendar", self._on_refresh))
        items.append(pystray.MenuItem("Quit AutoMeet", self._on_quit))
        return items

    def _build_menu(self):
        try:
            return self._build_menu_items()
        except Exception:
            return [
                pystray.MenuItem("Today's Meetings", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Could not load meetings", None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Refresh Calendar", self._on_refresh),
                pystray.MenuItem("Quit AutoMeet", self._on_quit),
            ]

    def _on_refresh(self, icon, item):
        if not self._scheduler:
            return
        try:
            events = get_todays_events(self._scheduler._service)
            self.update_events(events)
            self._scheduler.mark_fetched()
            self._scheduler.check_and_join_now()
        except Exception:
            pass

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
