import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from main import NotesHandler, NotesStore


class NotesApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        NotesHandler.store = NotesStore()
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), NotesHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, path, method="GET", payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        request = Request(self.base + path, data=data, method=method, headers={"Content-Type": "application/json"})
        with urlopen(request) as response:
            return response.status, json.loads(response.read() or b"null")

    def test_crud_flow(self):
        status, created = self.request("/notes", "POST", {"title": "Learn HTTP", "content": "Build an API"})
        self.assertEqual(status, 201)
        note_id = created["id"]
        self.assertEqual(self.request(f"/notes/{note_id}")[1]["title"], "Learn HTTP")
        self.assertEqual(self.request(f"/notes/{note_id}", "PUT", {"title": "Learn APIs"})[1]["title"], "Learn APIs")
        request = Request(self.base + f"/notes/{note_id}", method="DELETE")
        with urlopen(request) as response:
            self.assertEqual(response.status, 204)
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base + f"/notes/{note_id}")
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
