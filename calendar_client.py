import re
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_URL_PATTERNS = [
    re.compile(r"https://(?:[a-z0-9-]+\.)?zoom\.us/j/[^\s<>\"']+"),
    re.compile(r"https://teams\.microsoft\.com/l/meetup-join/[^\s<>\"']+"),
    re.compile(r"https://meet\.google\.com/[a-z\-]+"),
]
_TRAILING_JUNK = re.compile(r"[,.;)>]+$")


def build_service(credentials):
    return build("calendar", "v3", credentials=credentials)


def _list_events(service, start_of_day, end_of_day, conference_data_version=None):
    kwargs = {
        "calendarId": "primary",
        "timeMin": start_of_day.isoformat(),
        "timeMax": end_of_day.isoformat(),
        "singleEvents": True,
        "orderBy": "startTime",
    }
    if conference_data_version is not None:
        kwargs["conferenceDataVersion"] = conference_data_version
    return service.events().list(**kwargs).execute()


def get_todays_events(service):
    now_local = datetime.now().astimezone()
    start_of_day = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    try:
        try:
            result = _list_events(service, start_of_day, end_of_day, conference_data_version=1)
        except (HttpError, TypeError):
            # TypeError: older googleapiclient builds omit conferenceDataVersion
            result = _list_events(service, start_of_day, end_of_day)
        return [e for e in result.get("items", []) if "dateTime" in e.get("start", {})]
    except Exception:
        return []


def parse_event_start(event):
    return datetime.fromisoformat(event["start"]["dateTime"])


def _url_from_conference_data(event):
    for ep in event.get("conferenceData", {}).get("entryPoints", []):
        if ep.get("entryPointType") == "video" and ep.get("uri"):
            return ep["uri"]
    return None


def _url_from_text_fields(event):
    for field in ("description", "location"):
        text = event.get(field, "") or ""
        for pattern in _URL_PATTERNS:
            m = pattern.search(text)
            if m:
                return _TRAILING_JUNK.sub("", m.group(0))
    return None


def extract_meeting_url(event):
    # Prefer conferenceData — reflects the active provider (Zoom, Meet, Teams)
    # after the user switches conferencing. hangoutLink can stay stale on Meet.
    url = _url_from_conference_data(event)
    if url:
        return url

    text_url = _url_from_text_fields(event)
    hangout = event.get("hangoutLink")
    if text_url and hangout and "meet.google.com" in hangout and "zoom.us" in text_url:
        # Zoom link in location/description; stale Meet hangoutLink left behind
        return text_url

    if hangout:
        return hangout

    return text_url


def event_join_key(event):
    """Unique key per scheduled occurrence — reschedules get a new start time."""
    return (
        event.get("id", ""),
        event.get("start", {}).get("dateTime", ""),
        extract_meeting_url(event) or "",
    )
