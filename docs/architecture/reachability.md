---
type: Module
title: Reachability
description: Calculates the fastest credible arrival times to define defense thresholds and strike windows.
resource: v2_1/reachability.py
tags: [race, threshold, defense, v2]
timestamp: 2026-06-18
---

# Responsibility

Solves the reachability race. Determines whether a threat to a planet is "credible" by comparing the earliest enemy arrival time against our ability to reinforce or retake it. Allows the agent to avoid pouring resources into an unholdable planet (the "frozen capital" problem).

# Interface

- `reachable(P, side) -> (earliest_turn, max_force)`: Calculates the earliest turn a fleet from `side` can reach planet `P`, and the maximum aggregated force that can arrive at that time.
- Implements conservative credibility checks (a threat is credible only if it can defeat the garrison and exceeds the opponent's available uncommitted fleet).

# Invariants

- Arrival times use the size-aware `travel_time` calculations from `physics.py`.
- Computations are cached to avoid $O(P^2 \times T)$ blowup.
- Considers synchronized multi-fleet arrivals (aggregated force).

# Examples

```text
earliest_t, force = reachable(target_planet, enemy_id)
if earliest_t < my_fastest_arrival:
    # Planet is unholdable, plan a snipe instead
```
