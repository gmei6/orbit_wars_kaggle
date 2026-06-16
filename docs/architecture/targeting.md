---
type: Module
title: Targeting
description: Choose targets and size attack fleets using arrival-garrison math.
resource: src/targeting.py
tags: [targeting, fleet-sizing]
timestamp: 2026-06-16
---

# Responsibility

For each owned planet, pick the best affordable, sun-safe target and compute the
ships needed to capture it on arrival. Owns target selection and fleet sizing;
defers all rules to [physics](/architecture/physics.md) and consumes typed
[state](/architecture/state.md).

# Interface

`plan(state) -> [[source_id, angle, ships], ...]`; `angle_to(src, dst) -> radians`.

# Invariants

- Never routes a fleet whose straight path crosses the sun (`hits_sun`).
- Sizes attacks against the *arrival* garrison, not the launch garrison
  (travel-time blindness): `required_to_capture(ships, production, transit)`.
- Never commands more ships than the source garrison.
- Greedy: score = production / distance. ponytail: upgrade to real allocation
  only if self-play shows it pays.

# Examples

```text
plan(state) -> [[0, 0.785, 24]]   # planet 0 sends 24 ships toward 45 degrees
```
