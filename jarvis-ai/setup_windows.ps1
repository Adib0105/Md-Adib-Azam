$ErrorActionPreference = "Stop"

Write-Host "=== JARVIS V2 Windows Setup ==="

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.10+ was not found. Install Python first and enable 'Add Python to PATH'."
}

$PythonLauncher = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }

if (-not (Test-Path ".venv")) {
    & $PythonLauncher -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create .venv." }
}

$VenvPython = Join-Path $PWD ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    throw "Virtual environment Python was not found at $VenvPython"
}

& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }

& $VenvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed. Setup stopped; fix the error above and run this script again."
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}

Write-Host ""
Write-Host "Setup complete."
Write-Host "1) Open .env and add your OPENAI_API_KEY."
Write-Host "2) Run: .\.venv\Scripts\python.exe self_check.py"
Write-Host "3) Run GUI: .\.venv\Scripts\python.exe desktop_ui.py"
Write-Host "4) Or terminal: .\.venv\Scripts\python.exe main.py"
