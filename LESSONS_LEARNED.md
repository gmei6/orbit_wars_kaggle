# Lessons Learned

This document tracks key insights, architectural decisions, and mistakes made during the development of our Orbit Wars agent. Review this before implementing new strategies to avoid repeating past errors.

## Performance & Architecture

- **Trajectory Computation is Expensive:** O(T) predictive simulations are too slow for real-time turn limits. **Fix:** Precompute trajectories and cache them per-turn. This optimization reduced turn execution time from >1.5ms to ~0.60ms.
- **Environment Emulation:** Relying solely on Kaggle's remote environment slows down iteration. **Fix:** We vendored a local version of the Kaggle `orbit_wars` physics engine and created `arena.py` for rapid self-play benchmarking.
- **Rigid Body Rotation:** Inner planets rotate at a shared angular velocity, maintaining constant relative distances over time. We can precompute and cache their travel times to avoid per-turn dynamic intercept math for inner-inner pairs.

## Strategy & Gameplay

- **Piecemeal Attacks Fail:** Launching greedy, sequential multi-planet attacks leads to fleets arriving one by one, making them easy targets for defensive reserves. **Fix:** Implemented `v1` Synchronized Fleet Arrivals. Delaying launches from closer planets so fleets arrive simultaneously increased win-rate against the starter bot from 37% to 69%.
- **Producer Lite Threat:** Our `v1` logic currently loses to the `Producer Lite` opponent (0% win rate, -2395 average ships). Synchronized attacks alone are insufficient against its strategy.
- **The "Shiny Object" Problem (Zero ROI Awareness):** Targeting strictly by production value ignores travel distance and enemy garrison size. It leads to fleets chasing distant, heavily defended planets while ignoring cheap, close expansions, resulting in massive economic deficits. **Fix (Planned for v1_1):** Evaluate targets based on Return On Investment (ROI).
- **The "Frozen Capital" Problem (Over-defending):** Subtracting the entire incoming enemy fleet size from our available ships immediately ignores natural ship regeneration during the enemy's travel time. This paralyzes early expansion. **Fix (Planned for v1_1):** Defense reserves must subtract the planet's expected production before freezing ships.
- **Same-owner Fleet Stacking:** The engine groups fleets arriving on the same turn by owner before resolving combat. This means fleets arriving simultaneously combine their force rather than being defeated sequentially, confirming our Synchronized Arrivals logic works correctly at the engine level.
- **Determinism = store the baseline, perturb it:** Orbits, comet paths, and any in-flight fleet are fully deterministic — fleets are committed straight-line projectiles that cannot redirect, so the only unknown is each player's *next* launch. Store the forecastable baseline as a per-planet **event timeline** (production rate + sorted arrival events) and treat candidate launches as cheap perturbations rather than recomputing. The old `calculate_defense_needs` just summed incoming enemy ships, ignoring arrival order and ownership flips — the timeline (v2 Stage 1) fixes that.
- **Economy is the scoreboard:** the loss to `Producer Lite` is a macro/economy deficit, not a tactics problem. Optimize the production-integral (total ships generated over the remaining turns), not individual fights.


## Tooling

- **Evaluation Bias:** Standard 1v1 matches can be skewed by starting positions. **Fix:** Implemented antithetic seat swapping in `arena.py` and Wilson score intervals for robust confidence metrics during evaluations.
- **Mermaid Rendering in IDE:** Native markdown preview fails to render diagrams if node labels contain special characters (like `:` or spaces) without quotes. **Fix:** Always wrap node labels in double quotes (e.g., `Node["label: text"]`) when creating `graph TD` diagrams.
- **Doc drift after a refactor:** when `src/` became `v1/` + `v1_1/` and the strategy/targeting roles swapped, the per-module docs were updated but the index/README layer (`README.md`, `docs/architecture/index.md`, `v1_1/README.md`) was not — they still describe the old `src/` world. Conventions require updating the doc in the same change; the habit to build is checking the index/README layer, not just module docs.
- **Python Imports in Tests:** We constantly fail to run test scripts (like `pytest`) because of `ModuleNotFoundError`. **Fix:** Always prefix python execution commands with `PYTHONPATH=. ` (e.g., `PYTHONPATH=. pytest tests/...`) to ensure local modules resolve correctly.
