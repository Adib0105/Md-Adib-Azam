import argparse
import json
from pathlib import Path


def load_contacts(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_contacts(path: Path, contacts: list[dict]) -> None:
    path.write_text(json.dumps(contacts, indent=2), encoding="utf-8")


def add_contact(contacts: list[dict], name: str, phone: str, email: str = "") -> list[dict]:
    entry = {"name": name.strip(), "phone": phone.strip(), "email": email.strip()}
    for index, contact in enumerate(contacts):
        if contact["name"].casefold() == entry["name"].casefold():
            contacts[index] = entry
            return contacts
    contacts.append(entry)
    return contacts


def search_contacts(contacts: list[dict], query: str) -> list[dict]:
    needle = query.casefold()
    return [c for c in contacts if needle in " ".join(c.values()).casefold()]


def delete_contact(contacts: list[dict], name: str) -> list[dict]:
    return [c for c in contacts if c["name"].casefold() != name.casefold()]


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON contact book")
    parser.add_argument("--file", type=Path, default=Path("contacts.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("name")
    add.add_argument("phone")
    add.add_argument("--email", default="")
    commands.add_parser("list")
    find = commands.add_parser("search")
    find.add_argument("query")
    delete = commands.add_parser("delete")
    delete.add_argument("name")
    args = parser.parse_args()

    contacts = load_contacts(args.file)
    if args.command == "add":
        save_contacts(args.file, add_contact(contacts, args.name, args.phone, args.email))
        print("Contact saved.")
    elif args.command == "delete":
        save_contacts(args.file, delete_contact(contacts, args.name))
        print("Contact deleted if it existed.")
    else:
        rows = contacts if args.command == "list" else search_contacts(contacts, args.query)
        for row in rows:
            print(f"{row['name']}: {row['phone']} {row['email']}".rstrip())


if __name__ == "__main__":
    main()
