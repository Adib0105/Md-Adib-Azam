from app import analyze, parse_line

line = '192.0.2.1 - - [16/Aug/2026:10:00:00 +0530] "GET /admin HTTP/1.1" 403 10'
assert parse_line(line)["status"] == 403
result = analyze([line, line, line], threshold=3)
assert result["parsed_requests"] == 3
assert len(result["alerts"]) == 2
assert result["status_counts"][403] == 3
print("Access log monitor tests passed")
