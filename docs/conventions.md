---
type: Convention
title: Project Conventions
description: Non-negotiable constraints for reproducibility and validation.
tags: [reproducibility, testing, integrity]
timestamp: 2026-06-16
---

# Deterministic seeding

Every stochastic run — sampling, parameter sweep, simulation — takes its seed
from a single source, not from scattered `random.seed()` / `np.random.seed()`
calls. The reference implementation is
[`/../addons/quant/seeding.py`](/../addons/quant/seeding.py); a general project
may keep its own, but the rule holds: one seed source, passed explicitly.

# Oracle protection

Baseline validation targets are frozen truth. Tests compare against them; you
do **not** edit a baseline to make a failing test pass. Adding or changing a
baseline is a deliberate, reviewed act, separate from the change under test.
See [`/../addons/quant/oracle_baseline.py`](/../addons/quant/oracle_baseline.py).

# Knowledge before code

Each module that an agent will reason about has a doc under
[`/architecture/`](/architecture/) bound to its code path via `resource:`.
A code change that alters a module's contract updates that doc in the same
change.

# OKF conformance

`docs/` is an OKF v0.1 bundle. Every non-reserved `.md` file carries a
non-empty `type`. Run [`/../scripts/check_okf.py`](/../scripts/check_okf.py)
before committing knowledge changes.
