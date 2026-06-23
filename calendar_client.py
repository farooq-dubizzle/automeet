from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarClient:
    def __init__(self, credentials):
        self.service = build("calendar", "v3", credentials=credentials)
        self._cached_events = []

    def get_todays_events(self):
        now_local = datetime.now().astimezone()
        start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        try:
            result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_of_day.isoformat(),
                    timeMax=end_of_day.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = [e for e in result.get("items", []) if "dateTime" in e.get("start", {})]
            self._cached_events = events
            return events
        except HttpError as e:
            print(f"Calendar API error: {e}")
            return self._cached_events
        except Exception as e:
            print(f"Unexpected error fetching calendar: {e}")
            return self._cached_events


def parse_event_start(event):
    """Return timezone-aware datetime for event start."""
    return datetime.fromisoformat(event["start"]["dateTime"])
