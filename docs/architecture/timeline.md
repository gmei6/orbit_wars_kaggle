---
type: Module
title: Timeline
description: Forecasts future state by folding arriving fleets chronologically.
resource: v1_1/timeline.py
tags: [forecast, state, v2]
timestamp: 2026-06-18
---

# Responsibility

Implements the v2 Information Model's event timeline. Forecasts the future state of planets by applying committed straight-line fleet arrivals chronologically. Eliminates the need to track dense, per-turn state matrices.

# Interface

- `PlanetTimeline`: Core structure representing the timeline of events for a single planet.
- `arrivals`: Sorted list of projected fleet arrivals.
- `garrison_at(T) -> int`: The expected number of ships garrisoned at turn `T`.
- `owner_at(T) -> int`: The expected owner at turn `T`.

# Invariants

- State is fully deterministic based on currently in-flight fleets.
- New launches perturb the timeline rather than requiring a full recalculation.
- Same-owner co-arrivals stack additively. Multi-owner contention is resolved via Kaggle engine rules (top two contend).

# Examples

```text
tl = timeline_cache[planet.id]
future_garrison = tl.garrison_at(state.turn + 10)
```
