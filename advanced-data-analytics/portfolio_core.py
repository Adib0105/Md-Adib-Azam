from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


def py(value: Any) -> Any:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def save_result(project: str, metrics: dict[str, Any], actions: list[str], output_dir=None):
    clean = {key: py(value) for key, value in metrics.items()}
    target = Path(output_dir) if output_dir else Path(__file__).parent / "artifacts" / project
    target.mkdir(parents=True, exist_ok=True)
    (target / "metrics.json").write_text(json.dumps(clean, indent=2, sort_keys=True), encoding="utf-8")
    brief = [f"# Decision brief: {project}", "", "## Metrics", ""]
    brief += [f"- **{key.replace('_', ' ').title()}**: {value}" for key, value in clean.items()]
    brief += ["", "## Recommended actions", ""] + [f"- {action}" for action in actions]
    (target / "decision_brief.md").write_text("\n".join(brief) + "\n", encoding="utf-8")
    return clean
