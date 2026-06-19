---
type: Module
title: Economy
description: Evaluates target ROI and tracks the production-integral metric.
resource: v2_1/economy.py
tags: [macro, value, ROI, v2]
timestamp: 2026-06-18
---

# Responsibility

The economic scoreboard and target valuation layer. Shifts the agent's objective from winning individual tactical skirmishes to maximizing the overall production-integral (total ships generated) over the remaining turns of the game.

# Interface

- `value(P) -> float`: Return On Investment of capturing planet `P`, scored **per turn of travel**. ROI = (production over the remaining holdable window − capture cost) ÷ `t_me`, where `t_me` is the reachability race's earliest credible-capture turn (size- and position-aware). Returns `0.0` when `P` is unreachable (`t_me is None`) or ROI ≤ 0, then scales by a hold multiplier (0.5 / 1.0 / 1.5) from the race. (D-016)
- `production_integral()`: Tracks and projects the total economic output of both players.

# Invariants

- Offensive value is windowed (an inner planet is only valuable while it is holdable and in range).
- Valuation penalizes chasing distant, expensive targets to avoid macroeconomic deficits against opponents like `Producer Lite`.
- Travel time is measured in **turns, not raw distance**: the time term reuses `reachable()`'s size-aware `t_me` (D-016), so fleet speed (which scales with fleet size) and rotating inner-planet positions are respected — replacing the earlier raw-Euclidean distance taken off a stale `initial_planets` position.

# Examples

```text
target_roi = value(candidate_planet)
if target_roi > best_roi:
    best_target = candidate_planet
```
