import tempfile
import unittest
from pathlib import Path

from main import add_contact, delete_contact, load_contacts, save_contacts, search_contacts


class ContactTests(unittest.TestCase):
    def test_crud_and_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "contacts.json"
            contacts = add_contact([], "Aman", "123", "a@example.com")
            save_contacts(path, contacts)
            loaded = load_contacts(path)
            self.assertEqual(search_contacts(loaded, "example")[0]["name"], "Aman")
            self.assertEqual(delete_contact(loaded, "aman"), [])


if __name__ == "__main__":
    unittest.main()
