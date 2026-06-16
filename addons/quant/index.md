---
type: Reference
title: Quant / Numeric Add-on
description: Optional helpers for stochastic and numerical work; not part of the general base.
tags: [optional, numeric, reproducibility]
timestamp: 2026-06-16
---

# Scope

Opt-in helpers for projects with randomness or numerical baselines. A general
coding project can delete this whole folder without touching the base template.

# Contents

- [`seeding.py`](seeding.py) — single source of randomness. Import
  `seed_everything` / `get_rng`; never scatter `random.seed()` calls. Enforces
  the deterministic-seeding rule in [`/../../docs/conventions.md`](/../../docs/conventions.md).
- [`oracle_baseline.py`](oracle_baseline.py) — compare outputs against frozen
  baselines. Baselines are truth; tests bend to them, not the reverse.

# ponytail note

Both files are stdlib-first: numpy is used when present, with a `random`
fallback, and there are no other dependencies. Each has a runnable self-check
under `__main__`.
