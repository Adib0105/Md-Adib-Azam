import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.1")
JARVIS_NAME = os.getenv("JARVIS_NAME", "JARVIS")
CREATOR_NAME = os.getenv("CREATOR_NAME", "Adib Azam")
USER_NAME = os.getenv("USER_NAME", "Adib")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "hinglish")
MEMORY_DB = ROOT / "jarvis_memory.db"
SCREENSHOT_DIR = ROOT / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
ENABLE_SCREEN_VISION = os.getenv("ENABLE_SCREEN_VISION", "true").lower() == "true"
MAX_TOOL_STEPS = int(os.getenv("MAX_TOOL_STEPS", "8"))
WAKE_WORDS = tuple(
    w.strip().lower()
    for w in os.getenv("WAKE_WORDS", "jarvis,hey jarvis,ok jarvis").split(",")
    if w.strip()
)

_raw_roots = os.getenv("ALLOWED_FILE_ROOTS", "").strip()
if _raw_roots:
    ALLOWED_FILE_ROOTS = tuple(Path(p.strip()).expanduser() for p in _raw_roots.split(";") if p.strip())
else:
    ALLOWED_FILE_ROOTS = tuple(Path.home() / name for name in ("Desktop", "Documents", "Downloads"))
