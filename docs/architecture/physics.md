---
type: Module
title: Physics
description: Frozen Orbit Wars constants and formulas — the oracle the bot and simulator both obey.
resource: src/physics.py
tags: [physics, oracle, geometry, combat]
timestamp: 2026-06-16
---

# Responsibility

Owns every game-rule constant and formula: fleet speed, planet radius, sun
collision, transit time, arrival garrison, and combat resolution. Owns *the
rules*, not strategy — no targeting or policy lives here. These values are
oracle-protected (see [conventions](/conventions.md)) and pinned to
[`baselines.json`](/../addons/quant/baselines.json) by
[`tests/test_physics.py`](../../tests/test_physics.py).

# Interface

# Schema — constants

| Name | Value | Meaning |
|------|-------|---------|
| `SUN` | (50.0, 50.0) | sun centre |
| `SUN_RADIUS` | 10.0 | trajectories within this are destroyed |
| `BOARD` | 100.0 | square board edge |
| `MAX_SPEED` | 6.0 | speed at ~1000 ships |
| `SPEED_REF_SHIPS` | 1000 | ships for max speed |
| `SPEED_EXP` | 1.5 | exponent in the speed curve |
| `TOTAL_TURNS` | 500 | game length |
| `COMET_SPAWN_TURNS` | 50,150,250,350,450 | comet spawn turns |

Functions: `fleet_speed(ships)`, `planet_radius(production)`,
`transit_turns(distance, ships)`, `arrival_garrison(garrison, production, turns)`,
`seg_within(x0,y0,x1,y1,cx,cy,r)`, `hits_sun(x0,y0,x1,y1)`,
`required_to_capture(garrison, production, turns)`,
`resolve_combat(attackers, garrison) -> (captured, ships_left)`.

# Invariants

- `speed = 1 + (MAX_SPEED-1)·(ln(ships)/ln(1000))^1.5`, clamped to MAX_SPEED;
  `fleet_speed(1)=1.0`, `fleet_speed(1000)=6.0`, monotone in ships.
- `planet_radius(p) = 1 + ln(p)`.
- Sun and arrival tests are continuous along the path segment, never
  endpoint-only.
- Capture needs strictly more than the arrival garrison (tie = mutual
  destruction): `required_to_capture = floor(arrival_garrison) + 1`.
- Editing any constant or formula here is an oracle change: update the baseline
  in the same reviewed commit, never to make a failing test pass.

# Examples

```text
fleet_speed(1) == 1.0
fleet_speed(1000) == 6.0
hits_sun(0, 50, 100, 50) is True          # crosses the sun
required_to_capture(10, 3, 5) == 26       # arrival garrison 25
resolve_combat([30, 10], 15) == (True, 5) # 20 beats 15, 5 survive
```
