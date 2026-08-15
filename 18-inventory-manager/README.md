# 18 — SQLite Inventory Manager

A command-line stock manager backed by SQLite. It supports product upserts, safe stock adjustments, and low-stock reporting.

```bash
python main.py --db inventory.db add SKU-01 "Notebook" 25 --price 120
python main.py --db inventory.db low-stock --threshold 5
python test_main.py
```

**Skills:** SQLite, transactions, CRUD, validation, CLI subcommands.
