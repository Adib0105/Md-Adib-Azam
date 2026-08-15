import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

root = Path(__file__).parent
with TemporaryDirectory() as folder:
    binary = Path(folder) / "employee_records"
    compile_result = subprocess.run(
        ["gcc", "-std=c11", "-Wall", "-Wextra", str(root / "employee_records.c"), "-o", str(binary)],
        capture_output=True,
        text=True,
    )
    assert compile_result.returncode == 0, compile_result.stderr
    result = subprocess.run(
        [str(binary), str(root / "sample_employees.csv"), "Support"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Records: 3" in result.stdout
    assert "Top performer: Mina (93.0)" in result.stdout

print("C employee records tests passed")
