import argparse
import sqlite3
from pathlib import Path


def init_db(connection: sqlite3.Connection) -> None:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS products (sku TEXT PRIMARY KEY, name TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity >= 0), price REAL NOT NULL CHECK(price >= 0))"
    )
    connection.commit()


def add_product(connection: sqlite3.Connection, sku: str, name: str, quantity: int, price: float) -> None:
    if quantity < 0 or price < 0:
        raise ValueError("Quantity and price must be non-negative")
    connection.execute(
        "INSERT INTO products(sku, name, quantity, price) VALUES (?, ?, ?, ?) ON CONFLICT(sku) DO UPDATE SET name=excluded.name, quantity=excluded.quantity, price=excluded.price",
        (sku, name, quantity, price),
    )
    connection.commit()


def adjust_stock(connection: sqlite3.Connection, sku: str, change: int) -> int:
    row = connection.execute("SELECT quantity FROM products WHERE sku = ?", (sku,)).fetchone()
    if row is None:
        raise KeyError(f"Unknown SKU: {sku}")
    new_quantity = row[0] + change
    if new_quantity < 0:
        raise ValueError("Stock cannot become negative")
    connection.execute("UPDATE products SET quantity = ? WHERE sku = ?", (new_quantity, sku))
    connection.commit()
    return new_quantity


def low_stock(connection: sqlite3.Connection, threshold: int) -> list[tuple]:
    return connection.execute(
        "SELECT sku, name, quantity, price FROM products WHERE quantity <= ? ORDER BY quantity, name", (threshold,)
    ).fetchall()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQLite inventory manager")
    parser.add_argument("--db", type=Path, default=Path("inventory.db"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("sku")
    add.add_argument("name")
    add.add_argument("quantity", type=int)
    add.add_argument("--price", type=float, required=True)
    adjust = commands.add_parser("adjust")
    adjust.add_argument("sku")
    adjust.add_argument("change", type=int)
    low = commands.add_parser("low-stock")
    low.add_argument("--threshold", type=int, default=5)
    args = parser.parse_args()

    with sqlite3.connect(args.db) as connection:
        init_db(connection)
        if args.command == "add":
            add_product(connection, args.sku, args.name, args.quantity, args.price)
            print("Product saved.")
        elif args.command == "adjust":
            print("New quantity:", adjust_stock(connection, args.sku, args.change))
        else:
            for row in low_stock(connection, args.threshold):
                print(row)


if __name__ == "__main__":
    main()
