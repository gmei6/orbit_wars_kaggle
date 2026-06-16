"""Oracle protection.

Baselines are frozen truth. Tests compare against them; you do NOT edit a
baseline to make a failing test pass. Changing a baseline is a deliberate,
reviewed act, kept separate from the change under test.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

BASELINE = Path(__file__).with_name("baselines.json")


def load_baselines() -> dict:
    return json.loads(BASELINE.read_text()) if BASELINE.exists() else {}


def check(name: str, value: float, *, rtol: float = 1e-9) -> None:
    """Assert `value` matches the frozen baseline for `name`."""
    base = load_baselines()
    if name not in base:
        raise KeyError(
            f"no baseline for {name!r}; add it deliberately via update_baseline(), "
            "not to make a test pass"
        )
    assert math.isclose(value, base[name], rel_tol=rtol), (
        f"{name}: {value} != baseline {base[name]}"
    )


def update_baseline(name: str, value: float) -> None:
    """Deliberate, reviewed write. Keep this out of the code path under test."""
    base = load_baselines()
    base[name] = value
    BASELINE.write_text(json.dumps(base, indent=2, sort_keys=True))


if __name__ == "__main__":
    # ponytail: self-check against a throwaway baseline file, then clean up.
    import tempfile
    BASELINE = Path(tempfile.mkdtemp()) / "baselines.json"
    update_baseline("pi", 3.14159)
    check("pi", 3.14159)
    try:
        check("pi", 3.14)
    except AssertionError:
        pass
    else:
        raise SystemExit("oracle should have rejected a drifted value")
    print("oracle self-check passed")
