from app import add_months, analyze, linear_forecast, moving_average

assert linear_forecast([10, 20, 30, 40], 2) == [50.0, 60.0]
assert moving_average([10, 20, 30, 40], 3) == 30.0
assert add_months("2026-12", 1) == "2027-01"
rows = [{"month": f"2026-0{i}", "sales": str(i * 100)} for i in range(1, 7)]
result = analyze(rows, 2)
assert result["forecast"][0]["sales"] == 700.0
assert result["holdout_mae"] == 0.0
print("Sales forecast tests passed")
