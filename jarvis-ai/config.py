import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
JARVIS_NAME = os.getenv("JARVIS_NAME", "JARVIS")
CREATOR_NAME = os.getenv("CREATOR_NAME", "Adib Azam")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "hinglish")
MEMORY_DB = ROOT / "jarvis_memory.db"
REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
