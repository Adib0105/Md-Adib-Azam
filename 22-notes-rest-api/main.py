import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class NotesStore:
    def __init__(self):
        self.notes: dict[int, dict] = {}
        self.next_id = 1

    def create(self, title: str, content: str = "") -> dict:
        if not title.strip():
            raise ValueError("title is required")
        note = {"id": self.next_id, "title": title.strip(), "content": content.strip()}
        self.notes[self.next_id] = note
        self.next_id += 1
        return note

    def update(self, note_id: int, changes: dict) -> dict | None:
        note = self.notes.get(note_id)
        if note is None:
            return None
        if "title" in changes and not str(changes["title"]).strip():
            raise ValueError("title cannot be empty")
        for key in ("title", "content"):
            if key in changes:
                note[key] = str(changes[key]).strip()
        return note


class NotesHandler(BaseHTTPRequestHandler):
    store = NotesStore()

    def log_message(self, format, *args):
        return

    def _json(self, status: int, payload) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _payload(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def _note_id(self) -> int | None:
        parts = urlparse(self.path).path.strip("/").split("/")
        return int(parts[1]) if len(parts) == 2 and parts[0] == "notes" and parts[1].isdigit() else None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/notes":
            self._json(200, list(self.store.notes.values()))
            return
        note = self.store.notes.get(self._note_id())
        self._json(200, note) if note else self._json(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/notes":
            self._json(404, {"error": "not found"})
            return
        try:
            payload = self._payload()
            self._json(201, self.store.create(str(payload.get("title", "")), str(payload.get("content", ""))))
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})

    def do_PUT(self):
        note_id = self._note_id()
        if note_id is None:
            self._json(404, {"error": "not found"})
            return
        try:
            note = self.store.update(note_id, self._payload())
            self._json(200, note) if note else self._json(404, {"error": "not found"})
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})

    def do_DELETE(self):
        note_id = self._note_id()
        if note_id is None or self.store.notes.pop(note_id, None) is None:
            self._json(404, {"error": "not found"})
            return
        self.send_response(204)
        self.end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Dependency-free Notes REST API")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    print(f"Notes API listening on http://127.0.0.1:{args.port}")
    ThreadingHTTPServer(("127.0.0.1", args.port), NotesHandler).serve_forever()


if __name__ == "__main__":
    main()
