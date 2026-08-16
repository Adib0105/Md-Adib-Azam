from dataclasses import dataclass
from typing import Callable

from config import REQUIRE_CONFIRMATION


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    reason: str = ""


class PermissionGate:
    """Central policy layer for local computer actions.

    JARVIS intentionally does not expose arbitrary shell execution, credential
    extraction, file deletion, software installation, or security-setting
    changes as tools. Interactive desktop actions are confirmation-gated.
    """

    ALWAYS_ALLOWED = {
        "get_system_info",
        "open_app",
        "screenshot",
        "inspect_screen",
        "recall_memory",
        "remember_fact",
        "read_clipboard",
        "volume_control",
    }

    CONFIRM_REQUIRED = {
        "open_url",
        "type_text",
        "press_hotkey",
        "mouse_click",
        "mouse_scroll",
        "write_clipboard",
        "lock_pc",
    }

    def __init__(self, confirm_callback: Callable[[str, dict], bool] | None = None):
        self.confirm_callback = confirm_callback

    def check(self, tool_name: str, arguments: dict) -> PermissionDecision:
        if tool_name in self.ALWAYS_ALLOWED:
            return PermissionDecision(True)

        if tool_name in self.CONFIRM_REQUIRED:
            if not REQUIRE_CONFIRMATION:
                return PermissionDecision(True)
            if self.confirm_callback and self.confirm_callback(tool_name, arguments):
                return PermissionDecision(True)
            return PermissionDecision(False, "User approval was not granted.")

        return PermissionDecision(False, f"Tool '{tool_name}' is not permitted by policy.")
