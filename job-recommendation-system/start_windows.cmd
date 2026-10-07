@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
  echo First complete the setup commands in START_HERE_HINGLISH.md.
  pause
  exit /b 1
)
venv\Scripts\python.exe app.py
if errorlevel 1 pause
