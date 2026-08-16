from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).parent


def main():
    results = {}
    for app in sorted((ROOT / "projects").glob("*/app.py")):
        spec = importlib.util.spec_from_file_location(app.parent.name.replace("-", "_"), app)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        results[app.parent.name] = module.run()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
