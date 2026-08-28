from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location("app",ROOT/"app.py");app=importlib.util.module_from_spec(spec);spec.loader.exec_module(app)
result=app.analyze(json.loads((ROOT/"sample.json").read_text()))
assert isinstance(result,dict) and result
print("PASS")
