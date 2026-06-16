# Project Tracker

**Goal:** Top 400 in the Orbit Wars Kaggle Competition.
**Secondary Goal:** Ensure the user learns as we code. Explain the *why* alongside the code.

## Current State

- `v0` baseline implemented (greedy targeting, strict oracle physics).
- `v0` iterations completed: comet rushes, predictive defense reserves, and greedy sequential multi-planet attacks.
- Exact `orbit_wars` Kaggle physics engine math extracted, verified, and integrated into `state.py`, `physics.py`, and `targeting.py`.
- Native Kaggle `orbit_wars` environment isolated and vendored locally for faster `sim.py` self-play.
- Architecture documented via OKF concept docs in `docs/architecture/`.

## Active Session

- `v0` complete and tested locally.
- Up Next: Profile `v0` performance, establish win-rate baselines, and plan `v1` optimizations.

## Rules of Engagement

1. **Alignment:** Read this file at the start of every session to pick up where we left off.
2. **Learning:** Do not just output massive code dumps. Explain the math, strategy, or API changes simply and clearly so the user learns the competition mechanics.
3. **Ponytail:** Only build what pays off. Prove it with `sim.py` self-play.

## CHANGELOG

- **2026-06-16:** Created `arena.py` self-play evaluation harness with antithetic seat swapping and Wilson score intervals.
- **2026-06-16:** Replaced slow O(T) predictive simulation with a precomputed trajectory cache per turn, achieving 4x speedup (0.65ms per game turn).
- **2026-06-16:** Implemented `v0` logic completions: comet interception, incoming fleet trajectory raycasting (defense), and greedy multi-planet sequential attacks.
- **2026-06-16:** Project initialization and environment set up.
