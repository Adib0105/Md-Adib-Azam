@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
if not exist "%~dp0setup_windows.cmd" goto missing_files

call "%~dp0setup_windows.cmd" --from-launcher
if errorlevel 1 goto failed

echo.
echo Starting JobMatch. Open the local address printed below in your browser.
echo Keep this window open. Press Ctrl+C to stop the app.
"%~dp0venv\Scripts\python.exe" "%~dp0app.py"
if errorlevel 1 goto failed
exit /b 0

:missing_files
echo App files are missing. Use Extract All on the ZIP before running this file.

:failed
echo.
echo JobMatch stopped. Read the error above and DOWNLOAD_RUN_GUIDE.txt.
pause
exit /b 1
