from app import audit

rows = [
    {"name": "A", "email": "a@example.com", "age": "20"},
    {"name": "B", "email": "wrong", "age": "x"},
    {"name": "A", "email": "a@example.com", "age": "20"},
]
result = audit(rows, {"age"})
assert result["rows"] == 3
assert result["duplicate_rows"] == 1
assert any(issue["issue"] == "invalid email" for issue in result["issues"])
assert any(issue["issue"] == "not numeric" for issue in result["issues"])
assert any(issue["issue"] == "duplicate email" for issue in result["issues"])
print("Excel CSV auditor tests passed")
