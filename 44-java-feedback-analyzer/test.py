import subprocess
from pathlib import Path

root = Path(__file__).parent
result = subprocess.run(
    ["java", str(root / "FeedbackAnalyzer.java"), str(root / "sample_feedback.csv")],
    capture_output=True,
    text=True,
)
assert result.returncode == 0, result.stderr
assert "Responses: 5" in result.stdout
assert "Average rating: 3.00" in result.stdout
assert "Positive: 2" in result.stdout
assert "Negative: 2" in result.stdout
print("Java feedback analyzer tests passed")
