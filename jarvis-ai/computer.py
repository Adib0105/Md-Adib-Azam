import os
import platform
import subprocess
import webbrowser
from datetime import datetime
from urllib.parse import urlparse

import pyautogui
import pyperclip

from config import SCREENSHOT_DIR

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.08

APP_COMMANDS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"],
    "task_manager": ["taskmgr.exe"],
    "powershell": ["powershell.exe"],
    "command prompt": ["cmd.exe"],
    "cmd": ["cmd.exe"],
}


class ComputerController:
    """Allowlisted Windows desktop controller.

    There is deliberately no generic shell/command-execution tool here. That
    keeps the agent useful for desktop automation without silently turning a
    model response into arbitrary OS commands.
    """

    def system_info(self):
        return {
            "os": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        }

    def open_app(self, app: str):
        key = app.lower().strip()
        command = APP_COMMANDS.get(key)
        if not command:
            return f"App '{app}' allowlist me nahi hai. Available: {', '.join(sorted(APP_COMMANDS))}"
        subprocess.Popen(command)
        return f"Opened {app}."

    def open_url(self, url: str):
        parsed = urlparse(url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return "Only valid http/https URLs are allowed."
        webbrowser.open(url, new=2)
        return f"Opened {url} in the default browser."

    def type_text(self, text: str):
        pyautogui.write(str(text), interval=0.015)
        return "Text typed into the active window."

    def hotkey(self, keys):
        if isinstance(keys, str):
            keys = [k.strip() for k in keys.split("+") if k.strip()]
        keys = [str(k).lower() for k in keys]
        if not keys or len(keys) > 4:
            return "Hotkey must contain 1 to 4 keys."
        pyautogui.hotkey(*keys)
        return f"Pressed {'+'.join(keys)}."

    def mouse_click(self, x: int, y: int, button: str = "left"):
        if button not in {"left", "right", "middle"}:
            return "Unsupported mouse button."
        pyautogui.click(x=int(x), y=int(y), button=button)
        return f"Clicked {button} at ({x}, {y})."

    def mouse_scroll(self, amount: int):
        amount = max(-20, min(20, int(amount)))
        pyautogui.scroll(amount)
        return f"Scrolled {amount}."

    def volume_control(self, action: str):
        action = action.lower().strip()
        keymap = {"up": "volumeup", "down": "volumedown", "mute": "volumemute"}
        key = keymap.get(action)
        if not key:
            return "Volume action must be up, down, or mute."
        pyautogui.press(key)
        return f"Volume {action}."

    def read_clipboard(self):
        text = pyperclip.paste()
        return text[:8000]

    def write_clipboard(self, text: str):
        pyperclip.copy(str(text))
        return "Clipboard updated."

    def screenshot(self):
        filename = datetime.now().strftime("screen_%Y%m%d_%H%M%S.png")
        out = SCREENSHOT_DIR / filename
        pyautogui.screenshot(str(out))
        return str(out)

    def lock_pc(self):
        if os.name == "nt":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
            return "PC locked."
        return "Lock command is configured for Windows only."
