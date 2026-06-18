---
type: Module
title: Targeting
description: Legacy mathematical oracle. Primarily provides global trajectory caching.
resource: v1_1/targeting.py
tags: [math, oracle, legacy]
timestamp: 2026-06-18
---

# Responsibility

Legacy pure mathematical calculator. Precomputes global game trajectories (`get_trajectory_cache`) to avoid O(T) predictive simulations during real-time evaluation. In v1_1, offensive and defensive math has been migrated to `reachability.py` and `physics.py`.

# Interface

`get_trajectory_cache(state)`

# Invariants

- Pure functions with no internal decision-making.
- Global trajectory cache is computed once per game and referenced continuously to maintain sub-millisecond execution times.

# Examples

```text
cache = get_trajectory_cache(state)
```
