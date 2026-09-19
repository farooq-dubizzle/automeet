# AutoMeet

Automatically joins your Google Calendar meetings at start time. Runs quietly in the background — system tray on Windows, menu bar on macOS.

| Platform | End-user guide | Developer guide |
|----------|----------------|-----------------|
| **Windows** | [Download & run](#for-colleagues-windows) | [Dev & release](#development-windows) |
| **macOS** | [Download & run](#for-colleagues-macos) | [README-mac.md](README-mac.md) |

---

## For colleagues (Windows)

1. Download `AutoMeet.exe` from [GitHub Releases](https://github.com/farooq-dubizzle/automeet/releases)
2. Double-click and sign in with Google when your browser opens

If sign-in fails, contact the app developer to be added as a test user (see [Google Cloud setup](#google-cloud-setup-one-time)).

## For colleagues (macOS)

1. Download `AutoMeet-mac.zip` from [GitHub Releases](https://github.com/farooq-dubizzle/automeet/releases) and unzip
2. Double-click `AutoMeet.app`
3. If macOS blocks the app (unsigned build): right-click `AutoMeet.app` → **Open** → **Open**
4. Sign in with Google when your browser opens

The app lives in the **menu bar** (top-right). It does not appear in the Dock.

If sign-in fails, contact the app developer to be added as a test user.

---

## Google Cloud setup (one time)

You need this before building or distributing AutoMeet. End users do **not** need their own credentials — they sign in through the app.

### 1. Create a Google Cloud project

1. Open [Google Cloud Console](https://console.cloud.google.com)
2. Click the project dropdown (top-left) → **New Project**
3. Name it (e.g. `AutoMeet`) → **Create**

### 2. Enable the Calendar API

1. Go to **APIs & Services → Library**
2. Search for **Google Calendar API** → click it → **Enable**

### 3. Configure the OAuth consent screen

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **Internal** (Google Workspace org) or **External** (personal Gmail / mixed users)
3. Fill in the required fields (app name, support email)
4. On **Scopes**, add: `https://www.googleapis.com/auth/calendar.readonly`
5. On **Test users** (External apps in Testing mode), add every colleague email that will use AutoMeet
6. Save

> **External + Testing:** Only emails listed as test users can sign in until the app is published. Add new users here whenever someone reports "access denied".

### 4. Create OAuth credentials

1. Go to **APIs & Services → Credentials**
2. **Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Name it (e.g. `AutoMeet Desktop`) → **Create**
5. Click **Download JSON**
6. Save the file as `credentials.json` in the **project root** (same folder as this README)

`credentials.json` is gitignored — never commit it.

### 5. Verify

```bash
# macOS
./mac/setup.sh && ./mac/run.sh

# Windows
setup.bat && run.bat
```

Sign in with a test-user account. You should see today's calendar events in the tray/menu bar.

---

## Development (Windows)

**Command Prompt:** `setup.bat` then `run.bat`

**Git Bash:** `./setup.bat` then `./run.bat`

Place `credentials.json` in the project root before running.

## Development (macOS)

```bash
./mac/setup.sh
./mac/run.sh
```

OAuth token is saved to `~/Library/Application Support/AutoMeet/automeet_token.json`.

See [README-mac.md](README-mac.md) for build, menu bar usage, and macOS-specific notes.

---

## Release

### Windows

**Command Prompt:** `build.bat`  
**Git Bash:** `./build.bat`

Upload `dist/AutoMeet.exe` to a new GitHub Release.

### macOS

On a Mac, with `credentials.json` in the project root:

```bash
./mac/build.sh
```

Output: `dist/AutoMeet.app`. Zip it and upload as `AutoMeet-mac.zip` to GitHub Releases.

When someone can't sign in, add their Google account email as a test user in GCP (**OAuth consent screen → Test users**).

---

## Tray / menu bar

**Windows:** Right-click the tray icon to see today's meetings. Uncheck any you don't want to auto-join.

**macOS:** Click the menu bar icon. Each meeting shows its time and title. Use **Join Now** to open the link immediately, or **Turn Off Auto-join** to skip auto-open at start time. **Refresh Calendar** reloads events.

Meetings with no conference link are shown but cannot be joined.
