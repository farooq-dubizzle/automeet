# AutoMeet
Automatically joins your Google Calendar meetings at start time. Lives in the system tray.

## Setup

### 1. Google Cloud credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a project
2. Enable the **Google Calendar API**
3. Go to **Credentials → Create Credentials → OAuth 2.0 Client ID** → Desktop app
4. Download the JSON and save it somewhere safe (e.g. `Documents/automeet_creds.json`)
5. Go to **OAuth consent screen → Test users** and add the Google account whose calendar you want to use

### 2. Configure
Edit `config.py` and set `CREDENTIALS_FILE` to the path of your credentials JSON:
```python
CREDENTIALS_FILE = r"C:\path\to\your\credentials.json"
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python main.py
```
A browser window will open for Google sign-in on first run. After that it's silent.

---

## Build an exe
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name AutoMeet --icon=assets/icon.ico --add-data "assets;assets" main.py
```
The exe will be at `dist/AutoMeet.exe`. To auto-start with Windows, drop it in your Startup folder (`Win+R` → `shell:startup`).

---

## Tray menu
Right-click the tray icon to see today's meetings. Uncheck any you don't want to auto-join. Meetings with no conference link are shown as `(no link)` and are skipped.
