import os
import platform
import subprocess
from pathlib import Path
import pyautogui

SAFE_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
}

class ComputerController:
    def system_info(self):
        return {
            "os": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def open_app(self, app: str):
        app = app.lower().strip()
        if app not in SAFE_APPS:
            return f"App '{app}' allowlist me nahi hai."
        subprocess.Popen(SAFE_APPS[app])
        return f"Opened {app}."

    def type_text(self, text: str):
        pyautogui.write(text, interval=0.02)
        return "Text typed."

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return f"Pressed {'+'.join(keys)}."

    def screenshot(self):
        out = Path(__file__).resolve().parent / "latest_screenshot.png"
        pyautogui.screenshot(str(out))
        return str(out)

    def lock_pc(self):
        if os.name == "nt":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
            return "PC locked."
        return "Lock command is currently configured for Windows only."
