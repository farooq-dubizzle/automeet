@echo off
python --version >nul 2>&1 || (echo Install Python 3.10+ from https://python.org & exit /b 1)
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo Done. Place credentials.json here, then run run.bat
