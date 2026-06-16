---
type: Module
title: Agent
description: Kaggle entry point — wires observation parsing to the policy each turn.
resource: src/agent.py
tags: [entrypoint, kaggle]
timestamp: 2026-06-16
---

# Responsibility

The function the Kaggle environment calls every turn. Owns only the wiring:
`obs -> parse -> decide -> commands`. Keep it one line of logic; everything real
lives in the modules it calls.

# Interface

`act(obs, config=None) -> [[source_id, angle, ships], ...]`.

# Invariants

- The signature and obs access are the contract with the live environment; if
  Kaggle's shape differs, change it here and in [state.parse](/architecture/state.md).
- Returns the action-space list unchanged from [strategy](/architecture/strategy.md).

# Examples

```text
act(obs) -> [[0, 1.57, 12], [3, -0.5, 40]]
```
