---
type: Tracker
title: Orbit Wars Project Tracker
description: Single source of truth for Orbit Wars Kaggle Competition project state, architecture, and decisions.
tags: [tracker, state, orbit-wars]
timestamp: 2026-06-17
---

# Orbit Wars Agent — Project Tracker & LLM Context

> **Single source of truth** for the Orbit Wars Kaggle Competition project.
> Paste this whole file into a fresh LLM conversation before working, and ask the LLM to
> return the whole updated file at the end (see the Update Protocol).

- **Last updated:** 2026-06-17 — Session 4 (Stage 0: Engine Co-arrival confirmation)
- **File version:** v1.0
- **Owner:** Gary Mei

---

## §0 — START HERE (operating instructions for the LLM)

You are helping with the Orbit Wars Kaggle Competition agent development. This file is the project's memory across many separate conversations. Read it before doing anything else.

**The three rules that matter most:**

1. **Respect the section legend.**
   - 🔒 **FROZEN** sections encode the agreed direction, rules of engagement, and architecture. **Do not silently rewrite them.** They change *only* through a dated entry in the **Decision Log (§10)** plus a minimal edit, flagged in the Changelog (§11).
   - 🟢 **LIVE** sections (§7–§9) describe the current state. Overwrite them freely to reflect reality — but truthfully (see rule 3).
   - 📜 **APPEND-ONLY** sections (§10–§11) are a permanent record. Add to the bottom; never delete or rewrite prior entries.
2. **Preserve direction.** If a request would pull the work away from the **North Star (§2)** or contradict a prior **Decision (§10)**, say so explicitly and ask before proceeding. Surface the tension; don't quietly adjust.
3. **Be honest in the live state.** Don't mark something done that isn't. Record blockers. If you are unsure a result is correct, say so. A tracker full of optimistic fiction is worse than no tracker.

**Session-start checklist (run this when you receive the file):**
read §2 (North Star) → §7 (Current Status) → §8 (Open Questions) → §9 (Next Actions), then consult `LESSONS_LEARNED.md`.

**Section legend:** 🔒 frozen · 🟢 live · 📜 append-only.

---

## §1 — Project Identity 🔒

- **One-line goal:** Build a top-tier Kaggle agent for Orbit Wars by optimizing physics predictions, synchronized fleet coordination, and efficient resource targeting.
- **Goal:** Top 400 in the Orbit Wars Kaggle Competition.
- **Secondary Goal:** Ensure the user learns as we code. Explain the *why* alongside the code.

---

## §2 — North Star & Rules of Engagement 🔒

**Rules of Engagement:**
1. **Lessons Learned:** Always consult `LESSONS_LEARNED.md` before implementing new logic to avoid repeating past mistakes.
2. **Learning:** Do not just output massive code dumps. Explain the math, strategy, or API changes simply and clearly so the user learns the competition mechanics.
3. **Ponytail:** Only build what pays off. Prove it with `sim.py` self-play.

---

## §3 — Mechanics & Architecture 🔒

- **Core Mechanics:** Continuous mathematics, logarithmic movement, sun-avoidance navigation, ROI-based targeting.
- **Physics Engine:** Exact `orbit_wars` Kaggle physics engine math extracted, verified, and integrated into `state.py`, `physics.py`, and `targeting.py`.
- **Environment:** Native Kaggle `orbit_wars` environment isolated and vendored locally for faster `sim.py` self-play.
- **Documentation:** Architecture documented via OKF concept docs in `docs/architecture/`.

---

## §4 — Tooling & Evaluation Standards 🔒

- **Evaluation Harness:** `arena.py` self-play evaluation harness with antithetic seat swapping (to counter starting position bias) and Wilson score intervals.
- **Performance Contract:** Trajectories are cached to maintain sub-millisecond execution times. O(T) predictive simulations are forbidden.

---

## §5 — Roadmap 🔒 *(check items off in place)*

- [x] **v0 Baseline:** Project initialization, strict oracle physics, greedy targeting.
- [x] **v0 Completions:** Comet rushes, predictive defense reserves, greedy sequential multi-planet attacks.
- [x] **Local Arena:** Vendor Kaggle environment, set up `arena.py` with antithetic seat swapping.
- [x] **Performance Optimization:** Global trajectory caching per-game instead of per-turn.
- [x] **v1 Development:** Synchronized fleet arrivals (preventing piecemeal defeat).
- [ ] **v2 Development:** Analyze and counter `Producer Lite` strategy.
- [ ] **v3 Development:** Advanced sun-avoidance heuristics and late-game resource starvation.

---

## §6 — Risks & Mitigations 🔒

- **Risk: Performance bottlenecks.** O(T) physics predictions can exceed real-time turn limits. **Mitigation:** Precompute and cache trajectories per turn (achieved 0.60ms/turn).
- **Risk: Starting position bias.** Win-rates in 1v1 matches can be skewed by spawns. **Mitigation:** Antithetic seat swapping implemented in `arena.py`.
- **Risk: Piecemeal interception.** Sequential multi-planet attacks arrive separately, getting picked off by defenses. **Mitigation:** Synchronized fleet arrivals (delaying close launches) implemented in v1.

---

## §7 — Current Status 🟢 *(overwrite each session to reflect reality)

- **Phase:** v2 Development (Information Model & Strategy)
- **State of the Code:** 
  - V2 Information Model & Strategy design documented.
  - Benchmarked `v1` vs `Producer Lite`: 0% win-rate, proving we have a massive macroeconomic deficit (-2395 avg ships).
  - **Major Refactor (v1_1)**: `src` folder renamed to `v1` (baseline). Duplicated to `v1_1` for active development. Cleanly separated decision-making logic from math. `targeting.py` is now purely a math oracle; `strategy.py` is the "brain".
  - Benchmarking scripts (`arena.py`, `sim.py`) moved to a global `scripts/` folder to clean up the agent directories.
  - **Stage 0 Complete:** Read Kaggle engine logic and confirmed the same-owner co-arrival stacking rule. Updated `v1_1/physics.py` to mirror this logic and pinned it with `tests/test_v1_1_physics.py`.
  - **Stage 1 Complete:** Created `v1_1/timeline.py` to fold per-planet arrivals from `state.fleets` into a deterministic forecast. Retired naive `calculate_defense_needs` in `targeting.py` and `incoming_enemy_ships` in `state.py`. Verified via `tests/test_v1_1_timeline.py`.
  - **Stage 2 Complete:** Travel/intercept math consolidated into `v1_1/physics.py`, eliminating duplicates in `targeting.py`. Precomputed distance table added for rigid-body inner planet co-rotation and stationary outer planets.
  - **Stage 3 Complete:** Implemented reachability race logic (`v1_1/reachability.py`). Added `reachable(P, side)` which iterates backwards to find maximum force arriving at any given turn, defining "credible" conservatively as defeating the garrison and exceeding the opponent's total uncommitted fleet size. Validated with `tests/test_v1_1_reachability.py`.
  - **Stage 4 Complete:** Created `v1_1/economy.py` with `production_integral` for macro-forecasting and `value(P)` for target valuation based on ROI (production / cost). Included a `reachable_cache` to mitigate $O(P^2 \times T)$ performance risks. Verified with `tests/test_v1_1_economy.py`. Watchlist established in `/docs/watchlist`.
  - **Stage 5 Complete:** Rewrote `v1_1/strategy.py` to use the v2 information model. Implemented "capital unfreezing" by calculating safe `min_garrison` from the timeline, added ROI-based target valuation, and logic to evacuate unholdable planets.
  - **Stage 5 Patch (Piecemeal Defeat & Expansion):** Added `RESERVATIONS` to `strategy.py` to persist synchronized delays across turns, and injected them into the timeline to prevent double-counting. Relaxed reachability race logic so the agent takes strategic risks rather than ceding the board. Achieved rapid early game expansion parity, but still loses 0-20 to Producer Lite (-4163 margin) due to later game scaling/target-selection issues.
  - Created `scripts/visualize.py` to generate and view local HTML replays of `kaggle_environments` matches, aiding visual debugging against `Producer Lite`.

---

## §8 — Open Questions & Blockers 🟢 *(overwrite each session)*

- **Blockers:** None currently.
- **Q1 (Strategy):** Why exactly does `Producer Lite` defeat `v2_macro`? We achieved early game expansion parity (Turn 50: 7 planets vs 13 planets), but Producer Lite's scaling is drastically higher (Turn 150: 5000+ ships). Does Producer Lite prioritize comets or specific geometry?
- **Q2 (Engine):** Same-owner co-arrival rule is RESOLVED (fleets stack).

---

## §9 — Next Actions 🟢 *(overwrite each session)

1. Use `scripts/visualize.py` to visually analyze `Producer Lite`'s mid-game scaling (Turn 50-100). Are we ignoring comets?
2. Implement comet-specific valuation or aggressive sun-avoidance routing if needed to counter Producer Lite.

---

## §10 — Decision Log 📜 *(APPEND-ONLY)*

> Format: `D-NNN | YYYY-MM-DD | Decision | Rationale | Affects §`

- `D-001 | 2026-06-16 | Replaced slow O(T) predictive simulation with a precomputed trajectory cache. | Predictive physics calculations were too slow for competition limits. Caching reduced time from >1.5ms to 0.60ms. | §4, §6`
- `D-002 | 2026-06-16 | Implement antithetic seat swapping and Wilson score intervals in arena.py. | Ensure robust confidence metrics and eliminate starting-position bias. | §4, §6`
- `D-003 | 2026-06-17 | Shift from greedy multi-planet attacks to Synchronized Fleet Arrivals (v1). | Greedy attacks resulted in fleets arriving sequentially, getting easily destroyed by defensive reserves. Synchronizing arrivals prevents piecemeal defeat. | §5, §6`
- `D-004 | 2026-06-17 | Refactor PROJECT_TRACKER.md into Two-Channel Cascade Model template. | The previous tracker lacked structured governance (Frozen vs Live sections). Adopting this template enforces a single source of truth for LLM context, ensuring the North Star and architectural decisions are preserved across sessions. | All`
- `D-005 | 2026-06-17 | Refactor v1 architecture: split Strategy and Targeting. | targeting.py was too cluttered with decision logic. Isolating the math allows us to rebuild the macro strategy cleanly in strategy.py. Created v1_1 for active dev. | §3, §7`
- `D-006 | 2026-06-17 | Move arena.py and sim.py to scripts/. | Keep the agent directory clean by removing non-agent code. | §4`
- `D-007 | 2026-06-17 | Update v1_1/physics.py resolve_combat to stack fleets by owner. | Kaggle engine interpreter groups fleets by owner before resolving combat. Updating physics allows correct calculation of synchronized multi-fleet arrivals. | §7`
- `D-008 | 2026-06-17 | V2 Information Model | Moved from per-turn dense snapshot to event-based timeline forecast. Implemented rigid-body inner planet rotation distance caching. | Replaces naive sum-based defense calculation. Frees up 'frozen capital'. | §3, §7`
- `D-009 | 2026-06-17 | Replace naive dense state with sparse timeline. | The turn-by-turn state projection fails on flips mid-window. Timeline correctly folds chronologically ordered arrivals. Removed calculate_defense_needs and incoming_enemy_ships. | §7`
- `D-010 | 2026-06-17 | Evaluate targets via ROI (production / cost) and cache reachability. | Prevents chasing distant, expensive targets. Caching mitigates the O(P^2 * T) complexity of reachability checks. | §7`
- `D-011 | 2026-06-18 | Inject RESERVATIONS into predictive timelines | Delayed fleet launches for synchronized attacks were "invisible" to the agent on subsequent turns, causing it to double-book attacks on the same target. Injecting them fixes double-counting. | §7`
- `D-012 | 2026-06-18 | Relax overly conservative reachability logic | Assuming the enemy will perfectly capture any planet they are closer to paralyzed our agent's expansion. Taking strategic risks is required for macro scale. | §7`
- `D-013 | 2026-06-18 | Created scripts/visualize.py for local HTML replays | Allows rapid visual debugging of mid-game scaling and positional logic without relying purely on text logs or the Kaggle web UI. | §4`

---

## §11 — Session Changelog 📜 *(APPEND-ONLY)*

> Format: `S-NNN | YYYY-MM-DD | Version | Notes`

- `S-001 | 2026-06-16 | v0 | Project initialization, environment setup, v0 baseline completions (comet interception, raycasting defense).`
- `S-002 | 2026-06-17 | v0.1 | Integrated Producer Lite, implemented v1 synchronized arrivals, implemented Trajectory caching. Moved benchmark.py to tests/.`
- `S-003 | 2026-06-17 | v1.0 | Project Tracker reformatted using the "Two-Channel Cascade" template structure to better track LLM context.`
- `S-004 | 2026-06-17 | v1.0 | Deep-dived v1 synchronized fleet arrivals logic. Added Mermaid diagrams to src/README.md for state and targeting architecture. Created session-wrapup skill.`
- `S-005 | 2026-06-17 | v1.0 | Represented incoming danger on Planet state via incoming_enemy_ships. Updated README architecture diagram to explicitly map nodes to source files.`
- `S-006 | 2026-06-17 | v1.1 | Benchmarked v1 vs Producer Lite (0% win rate). Refactored src/ into v1/ and v1_1/. Separated math into targeting.py and decision logic into strategy.py. Moved sim/arena out to scripts/. Updated OKF docs.`
- `S-007 | 2026-06-17 | v1.1 | Completed v2 Information Model Stage 0: confirmed Kaggle engine same-owner combat stacking logic. Wrote test_v1_1_physics.py to pin it.`
- `S-008 | 2026-06-17 | v1.1 | Completed Stage 2: Consolidated travel_time and lane_clear into physics.py. Added stationary distance table. Verified parity vs v1.`
- `S-009 | 2026-06-17 | v1.1 | Completed Stage 1 of v2 Information Model. Created timeline.py, implemented PlanetTimeline and chronological event folding. Removed obsolete state/targeting code. Passed timeline parity tests.`
- `S-009 | 2026-06-17 | v1.1 | Authored docs/design/v2-information-model.md (written design + 6-stage plan + doctrine behind D-008); registered it in docs/index.md and synced it to Stage 0/2 results. Flagged stale index/README docs + missing root CLAUDE.md. Formalized session-start / session-wrapup as Cowork skills; rebuilt session-wrapup as a generic packaged skill.`
- `S-010 | 2026-06-17 | v1.1 | Completed Stages 3, 4, and 5 of the v2 Information Model. Added reachability.py and economy.py. Rewrote strategy.py to use timeline-based capital unfreezing and ROI valuation. Achieved 100% win rate against v1, but 0% against Producer Lite.`
- `S-011 | 2026-06-18 | v2_macro | Fixed piecemeal defeat and paralyzed expansion. Implemented cross-turn RESERVATIONS memory, injected reservations into predictive timelines to prevent double-counting targets, and relaxed reachability race constraints. Early game parity achieved but mid-game macro deficit persists against Producer Lite.`
- `S-012 | 2026-06-18 | v2_macro | Authored scripts/visualize.py for generating local HTML replays via kaggle_environments. Confirmed Player A (0) is blue/bottom-left, B (1) is orange/top-right.`
