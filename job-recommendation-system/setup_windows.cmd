@echo off
setlocal EnableExtensions DisableDelayedExpansion
set "JOBMATCH_SETUP_DIR=%~dp0"
cd /d "%~dp0"
if not exist "%~dp0app.py" goto missing_files
if not exist "%~dp0requirements.txt" goto missing_files
if not exist "%~dp0scripts\seed_database.py" goto missing_files

if exist "%~dp0venv\Scripts\python.exe" goto verify_python
echo [1/3] Creating the local Python environment...
call :create_venv
if errorlevel 1 goto failed

:verify_python
"%~dp0venv\Scripts\python.exe" -c "import struct, sys; sys.exit(0 if sys.version_info[:2] in ((3, 11), (3, 12)) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if errorlevel 1 goto unsupported_venv

echo [2/3] Installing the required packages. First setup needs internet...
"%~dp0venv\Scripts\python.exe" -m pip --disable-pip-version-check install -r "%~dp0requirements.txt"
if errorlevel 1 goto failed

echo [3/3] Preparing the demo jobs...
"%~dp0venv\Scripts\python.exe" "%~dp0scripts\seed_database.py"
if errorlevel 1 goto failed

echo Setup complete.
if /I not "%~1"=="--from-launcher" pause
exit /b 0

:create_venv
py -3.12 -c "import struct; raise SystemExit(struct.calcsize('P') != 8)" >nul 2>&1
if not errorlevel 1 (
    py -3.12 -m venv "%JOBMATCH_SETUP_DIR%venv"
    if errorlevel 1 exit /b 1
    exit /b 0
)
py -3.11 -c "import struct; raise SystemExit(struct.calcsize('P') != 8)" >nul 2>&1
if not errorlevel 1 (
    py -3.11 -m venv "%JOBMATCH_SETUP_DIR%venv"
    if errorlevel 1 exit /b 1
    exit /b 0
)
python -c "import struct, sys; sys.exit(0 if sys.version_info[:2] in ((3, 11), (3, 12)) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if errorlevel 1 (
    echo Install 64-bit Python 3.11 or 3.12, then run start_windows.cmd again.
    echo Enable Add python.exe to PATH during installation.
    exit /b 1
)
python -m venv "%JOBMATCH_SETUP_DIR%venv"
if errorlevel 1 exit /b 1
exit /b 0

:unsupported_venv
echo The existing venv needs 64-bit Python 3.11 or 3.12.
echo Close the app, rename the venv folder to venv_old, and run start_windows.cmd again.
goto failed

:missing_files
echo App files are missing. Use Extract All on the ZIP before running this file.
echo Run this file from the folder containing app.py and requirements.txt.

:failed
echo Setup stopped because a step failed. Fix the error above, then try again.
if /I not "%~1"=="--from-launcher" pause
exit /b 1
