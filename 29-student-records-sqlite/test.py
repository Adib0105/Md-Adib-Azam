from app import class_report, connect, seed

with connect(":memory:") as database:
    seed(database)
    rows = class_report(database)
    assert len(rows) == 3
    assert rows[0]["name"] == "Mina"
    assert rows[0]["grade"] == "A"
    assert rows[-1]["attendance"] == 80.0

print("Student records tests passed")
