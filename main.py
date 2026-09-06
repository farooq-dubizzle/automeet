import sys


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
    from auth import get_credentials
    from config import FROZEN, ACCESS_DENIED_MSG

    try:
        creds = get_credentials()
    except FileNotFoundError as e:
        _show_error(str(e))
        sys.exit(1)
    except Exception:
        _show_error(ACCESS_DENIED_MSG if FROZEN else "Google authentication failed.")
        sys.exit(1)

    from calendar_client import build_service
    from tray_app import TrayApp
    from scheduler import MeetingScheduler

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
