import re

_URL_PATTERNS = [
    re.compile(r"https://[a-z0-9]+\.zoom\.us/j/[^\s<>\"']+"),
    re.compile(r"https://teams\.microsoft\.com/l/meetup-join/[^\s<>\"']+"),
    re.compile(r"https://meet\.google\.com/[a-z\-]+"),
]

_TRAILING_JUNK = re.compile(r"[,.;)>]+$")


def extract_meeting_url(event):
    # 1. hangoutLink (Google Meet, most reliable)
    url = event.get("hangoutLink")
    if url:
        return url

    # 2. conferenceData entryPoints (Meet and add-on integrations like Zoom/Teams)
    conference = event.get("conferenceData", {})
    for ep in conference.get("entryPoints", []):
        if ep.get("entryPointType") == "video":
            uri = ep.get("uri")
            if uri:
                return uri

    # 3. Scan description and location for known URL patterns
    for field in ("description", "location"):
        text = event.get(field, "") or ""
        for pattern in _URL_PATTERNS:
            m = pattern.search(text)
            if m:
                return _TRAILING_JUNK.sub("", m.group(0))

    return None
