import sqlite3
import threading
from datetime import datetime, timezone

from config import MEMORY_DB


class Memory:
    def __init__(self):
        self.lock = threading.RLock()
        self.conn = sqlite3.connect(MEMORY_DB, check_same_thread=False)
        with self.lock:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS memories ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, created_at TEXT)"
            )
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS facts ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, fact TEXT UNIQUE, created_at TEXT)"
            )
            self.conn.commit()

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    def add(self, role: str, content: str):
        with self.lock:
            self.conn.execute(
                "INSERT INTO memories(role, content, created_at) VALUES (?, ?, ?)",
                (role, str(content), self._now()),
            )
            self.conn.commit()

    def recent(self, limit: int = 20):
        limit = max(1, min(100, int(limit)))
        with self.lock:
            rows = self.conn.execute(
                "SELECT role, content FROM memories ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return list(reversed(rows))

    def remember_fact(self, fact: str):
        fact = " ".join(str(fact).split()).strip()
        if not fact:
            return "Nothing to remember."
        with self.lock:
            self.conn.execute(
                "INSERT OR IGNORE INTO facts(fact, created_at) VALUES (?, ?)",
                (fact, self._now()),
            )
            self.conn.commit()
        return "Remembered."

    def recall(self, query: str, limit: int = 8):
        query = str(query).strip()
        limit = max(1, min(20, int(limit)))
        pattern = f"%{query}%"
        with self.lock:
            facts = self.conn.execute(
                "SELECT fact FROM facts WHERE fact LIKE ? ORDER BY id DESC LIMIT ?",
                (pattern, limit),
            ).fetchall()
            chats = self.conn.execute(
                "SELECT role, content FROM memories WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                (pattern, limit),
            ).fetchall()
        results = [f"FACT: {row[0]}" for row in facts]
        results.extend(f"{role.upper()}: {content}" for role, content in chats)
        return results[:limit]

    def clear_conversation(self):
        with self.lock:
            self.conn.execute("DELETE FROM memories")
            self.conn.commit()

    def clear(self):
        self.clear_conversation()
