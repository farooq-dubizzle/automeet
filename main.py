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

    try:
        creds = get_credentials()
    except FileNotFoundError as e:
        _show_error(str(e))
        sys.exit(1)
    except Exception as e:
        _show_error(f"Google authentication failed:\n{e}")
        sys.exit(1)

    from calendar_client import CalendarClient
    from tray_app import TrayApp
    from scheduler import MeetingScheduler

    client = CalendarClient(creds)
    tray = TrayApp()
    scheduler = MeetingScheduler(client, tray)
    tray.set_scheduler(scheduler)

    scheduler.start()
    tray.run()  # blocks until Quit

    scheduler.stop()
    scheduler.join(timeout=5)


if __name__ == "__main__":
    main()
