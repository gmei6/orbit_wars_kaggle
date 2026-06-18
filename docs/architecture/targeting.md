---
type: Module
title: Targeting
description: Mathematical oracle for trajectories, travel times, and defense/attack calculations.
resource: v1_1/targeting.py
tags: [math, oracle, calculation]
timestamp: 2026-06-16
---

# Responsibility

Pure mathematical calculator. Precomputes game trajectories, calculates incoming enemy attacks (`calculate_defense_needs`), and calculates required ships/travel time for potential attacks (`calculate_attack_options`). It makes NO strategic decisions.

# Interface

`calculate_attack_options(state, target, delta_t)`, `calculate_defense_needs(state, cache)`.

# Invariants

- Pure functions with no internal decision-making.
- Never routes a fleet whose straight path crosses the sun (`hits_sun`).
- Sizes attacks against the *arrival* garrison, not the launch garrison.

# Examples

```text
calculate_attack_options(state, target_planet, 10) -> (24, (50.5, 30.2)) # Need 24 ships, expected at (50.5, 30.2)
```
