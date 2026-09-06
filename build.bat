@echo off
if not exist credentials.json (
    echo ERROR: credentials.json not found in project root.
    echo Download from Google Cloud Console and save it here before building.
    exit /b 1
)
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
pip install pyinstaller
pyinstaller AutoMeet.spec
if errorlevel 1 exit /b 1
echo.
echo Built dist\AutoMeet.exe
