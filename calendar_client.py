import re
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_URL_PATTERNS = [
    re.compile(r"https://[a-z0-9]+\.zoom\.us/j/[^\s<>\"']+"),
    re.compile(r"https://teams\.microsoft\.com/l/meetup-join/[^\s<>\"']+"),
    re.compile(r"https://meet\.google\.com/[a-z\-]+"),
]
_TRAILING_JUNK = re.compile(r"[,.;)>]+$")


def build_service(credentials):
    return build("calendar", "v3", credentials=credentials)


def get_todays_events(service):
    now_local = datetime.now().astimezone()
    start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    try:
        result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return [e for e in result.get("items", []) if "dateTime" in e.get("start", {})]
    except (HttpError, Exception):
        return []


def parse_event_start(event):
    return datetime.fromisoformat(event["start"]["dateTime"])


def extract_meeting_url(event):
    url = event.get("hangoutLink")
    if url:
        return url

    for ep in event.get("conferenceData", {}).get("entryPoints", []):
        if ep.get("entryPointType") == "video" and ep.get("uri"):
            return ep["uri"]

    for field in ("description", "location"):
        text = event.get(field, "") or ""
        for pattern in _URL_PATTERNS:
            m = pattern.search(text)
            if m:
                return _TRAILING_JUNK.sub("", m.group(0))

    return None
