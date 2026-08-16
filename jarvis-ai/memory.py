import sqlite3
from datetime import datetime
from config import MEMORY_DB

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(MEMORY_DB)
        self.conn.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, created_at TEXT)")
        self.conn.commit()

    def add(self, role: str, content: str):
        self.conn.execute("INSERT INTO memories(role, content, created_at) VALUES (?, ?, ?)", (role, content, datetime.utcnow().isoformat()))
        self.conn.commit()

    def recent(self, limit: int = 12):
        rows = self.conn.execute("SELECT role, content FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return list(reversed(rows))

    def clear(self):
        self.conn.execute("DELETE FROM memories")
        self.conn.commit()
