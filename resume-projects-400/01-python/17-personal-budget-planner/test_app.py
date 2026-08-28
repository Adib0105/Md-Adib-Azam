from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("project_app", ROOT / "app.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)

class ProjectTest(unittest.TestCase):
    def test_sample_produces_nonempty_mapping(self):
        data = json.loads((ROOT / "sample.json").read_text(encoding="utf-8"))
        result = module.solve(data)
        self.assertIsInstance(result, dict)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
