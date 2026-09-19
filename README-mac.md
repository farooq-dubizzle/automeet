# AutoMeet for macOS

Automatically joins your Google Calendar meetings at start time. Lives in the menu bar.

macOS only. See [README.md](README.md) for Windows and Google Cloud setup.

## For colleagues

1. Download `AutoMeet-mac.zip` from [GitHub Releases](https://github.com/farooq-dubizzle/automeet/releases) and unzip
2. Double-click `AutoMeet.app`
3. If macOS blocks the app (unsigned build): right-click `AutoMeet.app` → **Open** → **Open**
4. Sign in with Google when your browser opens

If sign-in fails, contact the app developer to be added as a test user.

The app runs from the **menu bar** (top-right). It does not appear in the Dock.

## Google Cloud setup

Follow the step-by-step guide in [README.md → Google Cloud setup](README.md#google-cloud-setup-one-time). You need `credentials.json` in the project root before building.

## Development

```bash
./mac/setup.sh
./mac/run.sh
```

OAuth token is saved to `~/Library/Application Support/AutoMeet/automeet_token.json`.

## Build release app

Run on a Mac with `credentials.json` in the project root:

```bash
./mac/build.sh
```

Output: `dist/AutoMeet.app`

Zip and upload to GitHub Releases as `AutoMeet-mac.zip`.

## Menu bar

Click the menu bar icon to see today's meetings:

```
Today's Meetings
─────────────────
Show all meetings today
─────────────────
16:30 - Team Standup (auto-join on)
   Join Now
   Turn Off Auto-join
─────────────────
Refresh Calendar
Quit AutoMeet
```

- **Show all meetings today** / **Show future meetings only** — toggle between all of today's events and upcoming only (default: future only)
- Click the meeting title or **Join Now** to open the link immediately
- **Turn Off Auto-join** skips auto-open at the scheduled time
- **Refresh Calendar** reloads events (picks up link changes, e.g. Meet → Zoom)

Meetings with no link show **No meeting link** and are skipped for auto-join.

## Notes

- The app must stay running to auto-join meetings. Quitting stops auto-join until you launch again.
- Auto-join window: 10 seconds before to 120 seconds after the scheduled start.
- Meetings missed while the Mac is asleep are not recovered.
- Launching the app twice starts only one instance (single-instance lock).
