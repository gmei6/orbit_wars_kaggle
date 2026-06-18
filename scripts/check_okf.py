#!/usr/bin/env python3
"""OKF v0.1 conformance check (spec sections 4 and 9).

A bundle is conformant if every non-reserved `.md` file has a parseable YAML
frontmatter block whose `type` is non-empty. `index.md` and `log.md` are
reserved and exempt (only the bundle-root `index.md` may carry frontmatter,
and only `okf_version`).

Usage:  python scripts/check_okf.py docs
Exits non-zero and lists every violation if the bundle is non-conformant.
ponytail: stdlib only — no yaml dependency, we just need the `type:` line.
"""
from __future__ import annotations

import sys
from pathlib import Path

RESERVED = {"index.md", "log.md"}
EXCLUDED_DIRS = {".venv", "vendor", ".agents", ".claude", "github-steals", ".pytest_cache"}


def frontmatter(text: str) -> dict | None:
    """Return the frontmatter as a flat dict, or None if absent/malformed.

    Minimal parser: top-level `key: value` lines only, which is all OKF
    requires us to inspect (the `type` field).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    out: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, val = line.partition(":")
            out[key.strip()] = val.strip()
    return out


def violations(bundle: Path) -> list[str]:
    problems: list[str] = []
    md_files = sorted(bundle.rglob("*.md"))
    if not md_files:
        return [f"no .md files under {bundle}"]
    for path in md_files:
        if path.name in RESERVED:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        fm = frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(bundle)
        if fm is None:
            problems.append(f"{rel}: missing or malformed frontmatter block")
        elif not fm.get("type"):
            problems.append(f"{rel}: missing required non-empty `type` field")
    return problems


def main(argv: list[str]) -> int:
    bundle = Path(argv[1]) if len(argv) > 1 else Path("docs")
    if not bundle.is_dir():
        print(f"not a directory: {bundle}", file=sys.stderr)
        return 2
    problems = violations(bundle)
    if problems:
        print(f"OKF: {len(problems)} violation(s) in {bundle}/")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"OKF: {bundle}/ is conformant")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
