import threading
from datetime import datetime, timezone

from calendar_client import extract_meeting_url, get_todays_events, parse_event_start
from mac.config import (
    CALENDAR_POLL_INTERVAL_SEC,
    JOIN_WINDOW_AFTER_SEC,
    JOIN_WINDOW_BEFORE_SEC,
    SCHEDULER_TICK_SEC,
)
from mac.platform import open_url, should_refresh_after_wake


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
        self._last_tick = 0.0

    def run(self):
        import time

        self._last_tick = time.monotonic()

        while not self._stop_event.is_set():
            now_mono = time.monotonic()

            if should_refresh_after_wake(self._last_tick, now_mono):
                with self._lock:
                    self._force_refresh = True

            self._last_tick = now_mono

            with self._lock:
                do_refresh = self._force_refresh or (now_mono - self._last_fetch >= CALENDAR_POLL_INTERVAL_SEC)
                self._force_refresh = False

            if do_refresh:
                self._tray.update_events(get_todays_events(self._service))
                self._last_fetch = time.monotonic()

            self._check_and_join()
            self._wake_event.wait(timeout=SCHEDULER_TICK_SEC)
            self._wake_event.clear()

    def _check_and_join(self):
        now = datetime.now(timezone.utc)
        for event in self._tray.get_enabled_events():
            event_id = event["id"]
            try:
                start = parse_event_start(event).astimezone(timezone.utc)
            except Exception:
                continue
            delta = (start - now).total_seconds()
            if -JOIN_WINDOW_AFTER_SEC <= delta <= JOIN_WINDOW_BEFORE_SEC:
                url = extract_meeting_url(event)
                if not url:
                    continue
                if self._joined.get(event_id) == url:
                    continue
                try:
                    open_url(url)
                except OSError:
                    continue
                self._joined[event_id] = url

    def check_and_join_now(self):
        self._check_and_join()

    def mark_fetched(self):
        import time

        self._last_fetch = time.monotonic()

    def mark_joined(self, event_id, url=None):
        if url:
            self._joined[event_id] = url
        else:
            self._joined[event_id] = True

    def force_refresh(self):
        with self._lock:
            self._force_refresh = True
        self._wake_event.set()

    def stop(self):
        self._stop_event.set()
        self._wake_event.set()
