# Lessons Learned

This document tracks key insights, architectural decisions, and mistakes made during the development of our Orbit Wars agent. Review this before implementing new strategies to avoid repeating past errors.

## Performance & Architecture

- **Trajectory Computation is Expensive:** O(T) predictive simulations are too slow for real-time turn limits. **Fix:** Precompute trajectories and cache them per-turn. This optimization reduced turn execution time from >1.5ms to ~0.60ms.
- **Environment Emulation:** Relying solely on Kaggle's remote environment slows down iteration. **Fix:** We vendored a local version of the Kaggle `orbit_wars` physics engine and created `arena.py` for rapid self-play benchmarking.

## Strategy & Gameplay

- **Piecemeal Attacks Fail:** Launching greedy, sequential multi-planet attacks leads to fleets arriving one by one, making them easy targets for defensive reserves. **Fix:** Implemented `v1` Synchronized Fleet Arrivals. Delaying launches from closer planets so fleets arrive simultaneously increased win-rate against the starter bot from 37% to 69%.
- **Producer Lite Threat:** Our `v1` logic currently loses to the `Producer Lite` opponent. Synchronized attacks alone are insufficient against its strategy. Further optimization is required for `v2`.

## Tooling

- **Evaluation Bias:** Standard 1v1 matches can be skewed by starting positions. **Fix:** Implemented antithetic seat swapping in `arena.py` and Wilson score intervals for robust confidence metrics during evaluations.
- **Mermaid Rendering in IDE:** Native markdown preview fails to render diagrams if node labels contain special characters (like `:` or spaces) without quotes. **Fix:** Always wrap node labels in double quotes (e.g., `Node["label: text"]`) when creating `graph TD` diagrams.
