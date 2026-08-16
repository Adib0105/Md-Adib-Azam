import json

from config import ENABLE_SCREEN_VISION
from permissions import PermissionGate
from vision import ScreenVision


class ToolRegistry:
    def __init__(self, computer, memory, confirm_callback=None):
        self.computer = computer
        self.memory = memory
        self.permissions = PermissionGate(confirm_callback)
        self.vision = ScreenVision() if ENABLE_SCREEN_VISION else None

    def schemas(self):
        return [
            {
                "type": "function",
                "name": "get_system_info",
                "description": "Get basic information about the user's local computer and Python runtime.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
            {
                "type": "function",
                "name": "open_app",
                "description": "Open an allowlisted Windows application.",
                "parameters": {
                    "type": "object",
                    "properties": {"app": {"type": "string"}},
                    "required": ["app"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "open_url",
                "description": "Open an http or https URL in the default browser. Requires user approval.",
                "parameters": {
                    "type": "object",
                    "properties": {"url": {"type": "string"}},
                    "required": ["url"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "type_text",
                "description": "Type text into the currently focused window. Requires user approval.",
                "parameters": {
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "press_hotkey",
                "description": "Press a keyboard shortcut in the active window. Requires user approval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keys": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 4}
                    },
                    "required": ["keys"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "mouse_click",
                "description": "Click an exact screen coordinate. Use screen inspection first when location is uncertain. Requires approval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "integer"},
                        "y": {"type": "integer"},
                        "button": {"type": "string", "enum": ["left", "right", "middle"]},
                    },
                    "required": ["x", "y", "button"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "mouse_scroll",
                "description": "Scroll the active window by a small amount. Requires approval.",
                "parameters": {
                    "type": "object",
                    "properties": {"amount": {"type": "integer", "minimum": -20, "maximum": 20}},
                    "required": ["amount"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "volume_control",
                "description": "Change Windows media volume up/down or toggle mute.",
                "parameters": {
                    "type": "object",
                    "properties": {"action": {"type": "string", "enum": ["up", "down", "mute"]}},
                    "required": ["action"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "screenshot",
                "description": "Capture the current screen and return the saved local image path.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
            {
                "type": "function",
                "name": "inspect_screen",
                "description": "Capture and visually analyze the current screen to answer a question about visible UI/content.",
                "parameters": {
                    "type": "object",
                    "properties": {"question": {"type": "string"}},
                    "required": ["question"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "read_clipboard",
                "description": "Read text currently stored in the local clipboard.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
            {
                "type": "function",
                "name": "write_clipboard",
                "description": "Replace local clipboard text. Requires user approval.",
                "parameters": {
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "remember_fact",
                "description": "Store a useful non-secret user preference or fact in JARVIS local long-term memory.",
                "parameters": {
                    "type": "object",
                    "properties": {"fact": {"type": "string"}},
                    "required": ["fact"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "recall_memory",
                "description": "Search JARVIS local memory for relevant previous facts or conversation snippets.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
            {
                "type": "function",
                "name": "lock_pc",
                "description": "Lock the Windows workstation. Requires user approval.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
        ]

    def call(self, name: str, arguments: dict) -> str:
        decision = self.permissions.check(name, arguments)
        if not decision.allowed:
            return json.dumps({"ok": False, "error": decision.reason})

        try:
            handlers = {
                "get_system_info": lambda: self.computer.system_info(),
                "open_app": lambda: self.computer.open_app(arguments["app"]),
                "open_url": lambda: self.computer.open_url(arguments["url"]),
                "type_text": lambda: self.computer.type_text(arguments["text"]),
                "press_hotkey": lambda: self.computer.hotkey(arguments["keys"]),
                "mouse_click": lambda: self.computer.mouse_click(arguments["x"], arguments["y"], arguments["button"]),
                "mouse_scroll": lambda: self.computer.mouse_scroll(arguments["amount"]),
                "volume_control": lambda: self.computer.volume_control(arguments["action"]),
                "screenshot": lambda: self.computer.screenshot(),
                "inspect_screen": lambda: self._inspect_screen(arguments["question"]),
                "read_clipboard": lambda: self.computer.read_clipboard(),
                "write_clipboard": lambda: self.computer.write_clipboard(arguments["text"]),
                "remember_fact": lambda: self.memory.remember_fact(arguments["fact"]),
                "recall_memory": lambda: self.memory.recall(arguments["query"]),
                "lock_pc": lambda: self.computer.lock_pc(),
            }
            handler = handlers.get(name)
            if not handler:
                return json.dumps({"ok": False, "error": f"Unknown tool: {name}"})
            result = handler()
            return json.dumps({"ok": True, "result": result}, ensure_ascii=False, default=str)
        except Exception as exc:
            return json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False)

    def _inspect_screen(self, question: str):
        if not self.vision:
            return "Screen vision is disabled."
        image_path = self.computer.screenshot()
        return self.vision.inspect(image_path, question)
