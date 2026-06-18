# Lessons Learned

This document tracks key insights, architectural decisions, and mistakes made during the development of our Orbit Wars agent. Review this before implementing new strategies to avoid repeating past errors.

## Performance & Architecture

- **Trajectory Computation is Expensive:** O(T) predictive simulations are too slow for real-time turn limits. **Fix:** Precompute trajectories and cache them per-turn. This optimization reduced turn execution time from >1.5ms to ~0.60ms.
- **Environment Emulation:** Relying solely on Kaggle's remote environment slows down iteration. **Fix:** We vendored a local version of the Kaggle `orbit_wars` physics engine and created `arena.py` for rapid self-play benchmarking.

## Strategy & Gameplay

- **Piecemeal Attacks Fail:** Launching greedy, sequential multi-planet attacks leads to fleets arriving one by one, making them easy targets for defensive reserves. **Fix:** Implemented `v1` Synchronized Fleet Arrivals. Delaying launches from closer planets so fleets arrive simultaneously increased win-rate against the starter bot from 37% to 69%.
- **Producer Lite Threat:** Our `v1` logic currently loses to the `Producer Lite` opponent (0% win rate, -2395 average ships). Synchronized attacks alone are insufficient against its strategy.
- **The "Shiny Object" Problem (Zero ROI Awareness):** Targeting strictly by production value ignores travel distance and enemy garrison size. It leads to fleets chasing distant, heavily defended planets while ignoring cheap, close expansions, resulting in massive economic deficits. **Fix (Planned for v1_1):** Evaluate targets based on Return On Investment (ROI).
- **The "Frozen Capital" Problem (Over-defending):** Subtracting the entire incoming enemy fleet size from our available ships immediately ignores natural ship regeneration during the enemy's travel time. This paralyzes early expansion. **Fix (Planned for v1_1):** Defense reserves must subtract the planet's expected production before freezing ships.

## Tooling

- **Evaluation Bias:** Standard 1v1 matches can be skewed by starting positions. **Fix:** Implemented antithetic seat swapping in `arena.py` and Wilson score intervals for robust confidence metrics during evaluations.
- **Mermaid Rendering in IDE:** Native markdown preview fails to render diagrams if node labels contain special characters (like `:` or spaces) without quotes. **Fix:** Always wrap node labels in double quotes (e.g., `Node["label: text"]`) when creating `graph TD` diagrams.
