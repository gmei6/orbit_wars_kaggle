---
type: Module
title: Economy
description: Evaluates target ROI and tracks the production-integral metric.
resource: v1_1/economy.py
tags: [macro, value, ROI, v2]
timestamp: 2026-06-18
---

# Responsibility

The economic scoreboard and target valuation layer. Shifts the agent's objective from winning individual tactical skirmishes to maximizing the overall production-integral (total ships generated) over the remaining turns of the game.

# Interface

- `value(P) -> float`: Calculates the Return On Investment (ROI) of capturing planet `P` based on its production rate, capture cost, and hold probability.
- `production_integral()`: Tracks and projects the total economic output of both players.

# Invariants

- Offensive value is windowed (an inner planet is only valuable while it is holdable and in range).
- Valuation penalizes chasing distant, expensive targets to avoid macroeconomic deficits against opponents like `Producer Lite`.

# Examples

```text
target_roi = value(candidate_planet)
if target_roi > best_roi:
    best_target = candidate_planet
```
