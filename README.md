# AutoMeet

Automatically joins your Google Calendar meetings at start time. Lives in the system tray.

Windows only.

1. Download `AutoMeet.exe` from GitHub Releases
2. Double-click and sign in with Google when your browser opens

If sign-in fails, contact the app developer to be added.

## Maintainer setup (one time)

1. [Google Cloud Console](https://console.cloud.google.com) → create a project
2. Enable **Google Calendar API**
3. **Credentials → Create Credentials → OAuth 2.0 Client ID → Desktop app**
4. Download JSON → save as `credentials.json` in this folder (gitignored)
5. **OAuth consent screen → Test users** → add colleague emails as they're onboarded

## Development

**Command Prompt:** `setup.bat` then `run.bat`

**Git Bash:** `./setup.bat` then `./run.bat`

Place `credentials.json` in the project root before running.

## Release

**Command Prompt:** `build.bat`

**Git Bash:** `./build.bat`

Upload `dist/AutoMeet.exe` to a new GitHub Release. Paste the "For colleagues" section above into the release description.

When someone can't sign in, add their Google account email as a test user in GCP.

## Tray menu

Right-click the tray icon to see today's meetings. Uncheck any you don't want to auto-join. Meetings with no conference link show as `(no link)` and are skipped.
