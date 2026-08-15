from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    course TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    subject TEXT NOT NULL,
    marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100),
    attendance REAL NOT NULL CHECK(attendance BETWEEN 0 AND 100),
    UNIQUE(student_id, subject)
);
"""


def connect(path: Path | str) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def seed(connection: sqlite3.Connection) -> None:
    students = [(1, "Asha", "CST"), (2, "Ravi", "CST"), (3, "Mina", "CST")]
    results = [
        (1, 1, "Python", 88, 94), (2, 1, "Database", 81, 91),
        (3, 2, "Python", 72, 78), (4, 2, "Database", 76, 82),
        (5, 3, "Python", 93, 97), (6, 3, "Database", 90, 95),
    ]
    connection.executemany(
        "INSERT OR REPLACE INTO students(id,name,course) VALUES(?,?,?)",
        students,
    )
    connection.executemany(
        "INSERT OR REPLACE INTO results(id,student_id,subject,marks,attendance) VALUES(?,?,?,?,?)",
        results,
    )
    connection.commit()


def class_report(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT s.id, s.name, ROUND(AVG(r.marks), 1) AS average_marks,
               ROUND(AVG(r.attendance), 1) AS attendance,
               CASE
                 WHEN AVG(r.marks) >= 85 THEN 'A'
                 WHEN AVG(r.marks) >= 70 THEN 'B'
                 WHEN AVG(r.marks) >= 55 THEN 'C'
                 ELSE 'Needs support'
               END AS grade
        FROM students s JOIN results r ON r.student_id = s.id
        GROUP BY s.id, s.name ORDER BY average_marks DESC
        """
    ).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("students.db"))
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    with connect(args.database) as connection:
        if args.seed:
            seed(connection)
        if args.report:
            print("Student performance report")
            for row in class_report(connection):
                print(f"{row['name']:<10} marks={row['average_marks']:>5} attendance={row['attendance']:>5}% grade={row['grade']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
