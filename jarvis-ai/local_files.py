from pathlib import Path

from config import ALLOWED_FILE_ROOTS


class LocalFileAccess:
    """Read-only, privacy-conscious access to user-approved folders."""

    BLOCKED_PARTS = {
        ".git",
        ".ssh",
        ".gnupg",
        "appdata",
        "node_modules",
        "credentials",
        "secrets",
    }
    BLOCKED_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519"}
    READABLE_EXTENSIONS = {
        ".txt", ".md", ".py", ".json", ".csv", ".log", ".ini", ".cfg",
        ".yaml", ".yml", ".html", ".css", ".js", ".ts", ".tsx", ".jsx",
        ".java", ".c", ".cpp", ".h", ".sql", ".ps1", ".bat",
    }
    SEARCHABLE_EXTENSIONS = READABLE_EXTENSIONS | {
        ".pdf", ".docx", ".xlsx", ".pptx", ".jpg", ".jpeg", ".png", ".webp"
    }

    def __init__(self):
        self.roots = tuple(root.resolve() for root in ALLOWED_FILE_ROOTS if root.exists())

    def _is_blocked(self, path: Path) -> bool:
        parts = {part.lower() for part in path.parts}
        return bool(parts & self.BLOCKED_PARTS) or path.name.lower() in self.BLOCKED_NAMES

    def _inside_allowed_root(self, path: Path) -> bool:
        resolved = path.resolve()
        for root in self.roots:
            try:
                resolved.relative_to(root)
                return True
            except ValueError:
                continue
        return False

    def search(self, query: str, max_results: int = 20):
        query = query.lower().strip()
        if not query:
            return []
        max_results = max(1, min(50, int(max_results)))
        results = []
        for root in self.roots:
            try:
                iterator = root.rglob("*")
                for path in iterator:
                    if len(results) >= max_results:
                        return results
                    if not path.is_file() or self._is_blocked(path):
                        continue
                    if path.suffix.lower() not in self.SEARCHABLE_EXTENSIONS:
                        continue
                    if query in path.name.lower():
                        try:
                            results.append({
                                "path": str(path),
                                "size": path.stat().st_size,
                                "extension": path.suffix.lower(),
                            })
                        except OSError:
                            continue
            except (PermissionError, OSError):
                continue
        return results

    def read_text(self, file_path: str, max_chars: int = 20000):
        path = Path(file_path).expanduser().resolve()
        if not self._inside_allowed_root(path):
            return "Access denied: file is outside approved roots."
        if self._is_blocked(path):
            return "Access denied: protected path or secret-like filename."
        if path.suffix.lower() not in self.READABLE_EXTENSIONS:
            return "This file type is not enabled for direct text reading."
        if not path.is_file():
            return "File not found."
        if path.stat().st_size > 2_000_000:
            return "File is too large for direct reading (2 MB limit)."
        max_chars = max(1000, min(50000, int(max_chars)))
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return f"Could not read file: {exc}"
        return text[:max_chars]

    def roots_info(self):
        return [str(root) for root in self.roots]
