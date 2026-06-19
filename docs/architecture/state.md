---
type: Module
title: State
description: Decode the raw Orbit Wars observation into typed planets, comets, and fleets.
resource: v2_1/state.py
tags: [observation, parsing]
timestamp: 2026-06-16
---

# Responsibility

Turns the raw per-turn observation into typed objects (`Planet`, `Comet`,
`Fleet`, `State`) with `mine()` / `targets()` helpers. Owns parsing only — no
physics, no decisions. `parse` is the single integration seam with the Kaggle
environment.

# Interface

# Schema

| Entity | Fields |
|--------|--------|
| Planet | id, owner, x, y, radius, ships, production |
| Comet  | id, owner, x, y, ships, production(=1) |
| Fleet  | id, owner, x, y, angle, source, ships |
| State  | turn, me, planets[], comets[], fleets[] |

`parse(obs) -> State`; `State.mine()` / `State.targets()` split planets by owner.

# Invariants

- owner: 0–3 players, -1 neutral; `me` is this agent's id.
- Field order matches the observation row order exactly — if the env reorders
  columns, fix it here and nowhere else.
- Pure transform: `parse` has no side effects and no game logic.

# Examples

```text
s = parse({"turn":1,"my_id":0,"planets":[[0,0,10,10,1.0,20,3],[1,-1,90,90,1.0,5,2]]})
s.mine()[0].id == 0
s.targets()[0].id == 1
```
