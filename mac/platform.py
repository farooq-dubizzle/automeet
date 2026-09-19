import fcntl
import os
import subprocess
import sys

from mac.config import CALENDAR_POLL_INTERVAL_SEC, LOCK_FILE


def open_url(url):
    subprocess.run(["open", url], check=False)


def ensure_single_instance():
    fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        sys.exit(0)
    return fd


def should_refresh_after_wake(last_mono, now_mono):
    return (now_mono - last_mono) > (CALENDAR_POLL_INTERVAL_SEC * 2)
