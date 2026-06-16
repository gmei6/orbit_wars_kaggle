---
type: Module
title: Strategy
description: Per-turn policy that produces the agent's launch commands.
resource: src/strategy.py
tags: [policy, strategy]
timestamp: 2026-06-16
---

# Responsibility

Owns the turn-level policy: given a [state](/architecture/state.md), return the
launch commands. v0 delegates to [targeting](/architecture/targeting.md); this
is the seam where defence, comet rushes, or multi-target allocation get added.

# Interface

`decide(state) -> [[source_id, angle, ships], ...]`.

# Invariants

- Output is exactly the action space: `[source_planet_id, angle, ships]` rows.
- Pure function of state — no hidden turn-to-turn memory in v0.

# Examples

```text
decide(state) == plan(state)   # v0 is a thin pass-through
```
