import os
import threading
from datetime import datetime, timezone

from calendar_client import event_join_key, extract_meeting_url, get_todays_events, parse_event_start
from config import CALENDAR_POLL_INTERVAL_SEC, SCHEDULER_TICK_SEC


class MeetingScheduler(threading.Thread):
    def __init__(self, calendar_service, tray_app):
        super().__init__(daemon=True, name="MeetingScheduler")
        self._service = calendar_service
        self._tray = tray_app
        self._stop_event = threading.Event()
        self._wake_event = threading.Event()
        self._force_refresh = False
        self._lock = threading.Lock()
        self._joined = {}
        self._last_fetch = 0.0

    def run(self):
        import time

        while not self._stop_event.is_set():
            now_mono = time.monotonic()

            with self._lock:
                do_refresh = self._force_refresh or (now_mono - self._last_fetch >= CALENDAR_POLL_INTERVAL_SEC)
                self._force_refresh = False

            if do_refresh:
                events = get_todays_events(self._service)
                self._tray.update_events(events)
                self.prune_joined(events)
                self._last_fetch = time.monotonic()

            self._check_and_join()
            self._wake_event.wait(timeout=SCHEDULER_TICK_SEC)
            self._wake_event.clear()

    def _check_and_join(self):
        now = datetime.now(timezone.utc)
        for event in self._tray.get_enabled_events():
            try:
                start = parse_event_start(event).astimezone(timezone.utc)
            except Exception:
                continue
            delta = (start - now).total_seconds()
            if -SCHEDULER_TICK_SEC <= delta <= SCHEDULER_TICK_SEC:
                url = extract_meeting_url(event)
                if not url:
                    continue
                key = event_join_key(event)
                if self._joined.get(key):
                    continue
                try:
                    os.startfile(url)
                except OSError:
                    continue
                self._joined[key] = True

    def prune_joined(self, events):
        valid = {event_join_key(e) for e in events}
        with self._lock:
            self._joined = {k: v for k, v in self._joined.items() if k in valid}

    def force_refresh(self):
        with self._lock:
            self._force_refresh = True
        self._wake_event.set()

    def stop(self):
        self._stop_event.set()
        self._wake_event.set()
