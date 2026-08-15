# 12 — Contact Book CLI

A JSON-backed contact manager with add, list, search, and delete commands. Duplicate names are updated instead of silently duplicated.

```bash
python main.py --file contacts.json add "Aman" "9876543210" --email aman@example.com
python main.py --file contacts.json list
python test_main.py
```

**Skills:** CRUD operations, JSON persistence, argparse subcommands, testing.
