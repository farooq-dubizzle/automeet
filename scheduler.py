import subprocess
import threading
from datetime import datetime, timezone

from calendar_client import parse_event_start
from link_extractor import extract_meeting_url
from config import CALENDAR_POLL_INTERVAL_SEC, SCHEDULER_TICK_SEC


class MeetingScheduler(threading.Thread):
    def __init__(self, calendar_client, tray_app):
        super().__init__(daemon=True, name="MeetingScheduler")
        self._calendar_client = calendar_client
        self._tray = tray_app
        self._stop_event = threading.Event()
        self._wake_event = threading.Event()  # separate event for waking the sleep
        self._force_refresh = False
        self._lock = threading.Lock()
        self._joined = set()
        self._last_fetch = 0.0

    def run(self):
        import time

        while not self._stop_event.is_set():
            now_mono = time.monotonic()

            with self._lock:
                do_refresh = self._force_refresh or (now_mono - self._last_fetch >= CALENDAR_POLL_INTERVAL_SEC)
                self._force_refresh = False

            if do_refresh:
                events = self._calendar_client.get_todays_events()
                self._tray.update_events(events)
                self._last_fetch = time.monotonic()
                print(f"[automeet] Fetched {len(events)} events for today")

            self._check_and_join()
            self._wake_event.wait(timeout=SCHEDULER_TICK_SEC)
            self._wake_event.clear()

    def _check_and_join(self):
        now = datetime.now(timezone.utc)
        for event in self._tray.get_enabled_events():
            event_id = event["id"]
            if event_id in self._joined:
                continue
            try:
                start = parse_event_start(event).astimezone(timezone.utc)
            except Exception as e:
                print(f"[automeet] Could not parse start for {event.get('summary')!r}: {e}")
                continue
            delta = (start - now).total_seconds()
            if -SCHEDULER_TICK_SEC <= delta <= SCHEDULER_TICK_SEC:
                url = extract_meeting_url(event)
                if url:
                    print(f"[automeet] Joining {event.get('summary')!r}: {url}")
                    subprocess.Popen(["cmd", "/c", "start", "", url])
                    self._joined.add(event_id)

    def force_refresh(self):
        with self._lock:
            self._force_refresh = True
        self._wake_event.set()

    def stop(self):
        self._stop_event.set()
        self._wake_event.set()  # wake immediately so stop is responsive
