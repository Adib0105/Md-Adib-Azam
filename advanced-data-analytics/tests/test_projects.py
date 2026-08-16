from __future__ import annotations

import importlib.util
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_all_twenty_projects_run(tmp_path):
    apps = sorted((ROOT / "projects").glob("*/app.py"))
    assert len(apps) == 20
    for app in apps:
        spec = importlib.util.spec_from_file_location(app.parent.name.replace("-", "_"), app)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        metrics = module.run(tmp_path / app.parent.name)
        assert len(metrics) >= 4
        for value in metrics.values():
            if isinstance(value, float):
                assert math.isfinite(value)
        assert (tmp_path / app.parent.name / "metrics.json").exists()
        assert (tmp_path / app.parent.name / "decision_brief.md").exists()
