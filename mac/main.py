import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _show_error(msg):
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("AutoMeet", msg)
        root.destroy()
    except Exception:
        print(f"ERROR: {msg}", file=sys.stderr)


def main():
    from mac.auth import get_credentials
    from mac.config import ACCESS_DENIED_MSG, FROZEN
    from mac.platform import ensure_single_instance

    ensure_single_instance()

    try:
        creds = get_credentials()
    except FileNotFoundError as e:
        _show_error(str(e))
        sys.exit(1)
    except Exception:
        _show_error(ACCESS_DENIED_MSG if FROZEN else "Google authentication failed.")
        sys.exit(1)

    from calendar_client import build_service
    from mac.scheduler import MeetingScheduler
    from mac.tray_app import TrayApp

    service = build_service(creds)
    tray = TrayApp()
    scheduler = MeetingScheduler(service, tray)
    tray.set_scheduler(scheduler)

    scheduler.start()
    tray.run()

    scheduler.stop()
    scheduler.join(timeout=5)


if __name__ == "__main__":
    main()
