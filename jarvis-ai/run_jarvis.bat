@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo JARVIS environment not found.
  echo Run setup_windows.ps1 first.
  pause
  exit /b 1
)

if not exist ".env" (
  echo .env not found. Copy .env.example to .env and add OPENAI_API_KEY.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" desktop_ui.py
if errorlevel 1 pause
