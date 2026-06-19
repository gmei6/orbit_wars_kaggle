---
type: Module
title: Strategy
description: The primary decision-making brain: chooses targets, distributes fleets, and synchronizes arrivals.
resource: v2_1/strategy.py
tags: [policy, strategy, macro]
timestamp: 2026-06-16
---

# Responsibility

The true "brain" of the agent. Owns target selection, ROI scoring, defense reserve allocation, and synchronized fleet launch delays. It relies on [targeting](/architecture/targeting.md) for pure mathematical calculations.

# Interface

`decide(state) -> [[source_id, angle, ships], ...]`.

# Invariants

- Output is exactly the action space: `[source_planet_id, angle, ships]` rows.
- Controls economy expansion rate by deciding how many ships to retain vs send.
- Synchronizes launches to prevent piecemeal defeat.

# Examples

```text
decide(state) -> [[0, 0.785, 24]]   # planet 0 sends 24 ships toward 45 degrees
```
