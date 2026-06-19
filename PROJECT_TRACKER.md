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

- **Last updated:** 2026-06-18 — Session 7 (doc-drift reconcile v1_1→v2_1 across CLAUDE/docs/README; garrison-release plan drafted)
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

- **Phase:** v2 Development — macro tuning in **`v2_1/`** (active dev dir). Travel-time valuation landed (D-016, beats `v2_macro` 57%). This session reconciled the doc drift (D-018) and **drafted the garrison-release plan** (`docs/design/garrison-release-plan.md`); implementing it is the next step (see §9).
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
  - **Session 5 — Replay diagnosis (loss vs `Producer Lite`).** Parsed an uploaded HTML replay and verified it against the frozen engine math (`fleet_speed`, `resolve_combat`). Findings: (1) the proposed "snipe planet 13" was arithmetically correct (enemy 15 ships → captures neutral-7 at step 13 leaving 8; +5/turn → 13 at step 14, so 14 ships flips it) but **geometrically unreachable** — planet 13 sits ~40u from our only base (planet 12) on the opposite corner, so the earliest possible intercept is step 26, twelve turns after the capture. The existing reachability race correctly vetoes it. (2) The true cause of the loss is **macro/expansion failure**: we peaked at 2 planets while `Producer Lite` went 1→19 and won (final reward −1, eliminated ~turn 70). The agent hoarded ~40 idle ships on planet 12 until step 7, then launched slow 29-ship fleets at distant targets — the "frozen capital" + "shiny object" lessons in action. (3) Snipe is **not** a first-class term in `v2_macro/strategy.py`.
  - **Session 6 — Travel-time valuation (Next Action #1) DONE.** Created `v2_1/` (copy of `v2_macro`) as the active dev dir and made it self-contained (the copy's `economy.py`/`reachability.py`/`agent.py` imported the `v2_macro` package, so edits silently ran `v2_macro` — switched to relative imports). Diagnosed that `value()` did *not* "ignore travel time": it already divided by a term, but the term was raw Euclidean distance (not turns), off a stale `initial_planets` position, and speed-blind. **Fix (D-016):** reuse the reachability race's `t_me` (earliest credible-capture turn — size/position-aware, already computed for the hold multiplier) as the time term; return 0 when unreachable. **Validated:** `v2_1` beats the frozen `v2_macro` **57.0%** over 200 games (95% CI 50.1–63.7%, LOS 97.6%, +875 avg ships). Still **0%** vs `Producer Lite` (margin ~−4200) — the remaining gap is ship-hoarding, not valuation.
  - **Session 6 — Arena tooling (D-017).** Wired `arena.py` `_resolve_spec` for `v2_1`, `v2_macro`, and `producer_lite`; fixed a `producer_lite` loader crash (`spec_from_file_location` modules must be registered in `sys.modules` before `exec_module`). M1 Max perf: **kept** BLAS/OMP thread-pinning (`setdefault` to 1; ~6% vs the torch opponent), **rejected** the performance-core worker cap (measured: with threads pinned, throughput rises with workers, 10 > 9 > 8). Default reverted to `cpu_count-1` + an `ARENA_WORKERS` override; `scripts/arena_baseline.py` kept as a pinning-off A/B reference.
  - **Session 7 — Doc-drift reconcile (D-018).** `v1_1/` no longer exists on disk (folded into the `v1_1`→`v2_macro`→`v2_1` lineage), so every doc pointer to it was a dangling path. Repointed `v1_1`→`v2_1`: CLAUDE.md Code layout, all 8 `docs/architecture/` `resource:` paths + the index prose, and the `targeting.md`/`economy.md`/`v2-information-model.md` prose. Documented the D-016 `t_me` valuation in `economy.md`. Refreshed the `README.md` entry-pointer. `AGENTS.md` needed no change (already version-agnostic). Left as-is: append-only history, `PROJECT.md` milestone names (accurate history), and the real `tests/test_v1_1_*.py` filenames. Verified zero stray `v1_1` except the deliberate lineage note + those test filenames. (`check_okf` validates only `type:`, not `resource:`, so the drift had passed conformance silently; not re-run here — host folder unmounted — but `type:` fields were untouched.)
  - **Session 7 — Garrison-release plan drafted** (`docs/design/garrison-release-plan.md`). Traced hoarding to the `available[]` block (`v2_1/strategy.py` 66–105): **M1** `will_lose → available = 0` freezes a holdable planet's whole garrison (biggest hoard); **M2** the 30-turn `min_garrison` trough freezes ships against far threats; **M3** (separate fix) post-D-016 unreachable targets score 0, so released ships have no destination. Plan: *verify which mechanism is binding before turning the knob*, then levers A (shrink lookahead) → B/C (reserve against the first threat only) → D (anti-snipe floor), each arena-gated vs `v2_macro` + `producer_lite`.

---

## §8 — Open Questions & Blockers 🟢 *(overwrite each session)*

- **Blockers:** None.
- **Q1 (Strategy) — partially resolved.** Travel-time valuation is done: scoring ROI per `t_me` made `v2_1` beat the frozen `v2_macro` 57% (D-016). But `v2_1` still loses 0% to `Producer Lite` (margin ~−4200), so the *binding* constraint is now **ship-hoarding**, not target ranking — the agent expands but under-commits idle capital. Next lever: release garrison earlier (Next Action #1) — plan now drafted (`docs/design/garrison-release-plan.md`), which flags the hoard may instead be the reachability target-gate (M3) and so verifies the binding lever before editing `min_garrison`.
- **Q2 (Strategy) — open.** Should "snipe" be a first-class, reachability-gated valuation term in `economy.py`/`strategy.py`? Still absent; deferred behind the garrison fix.
- **Q3 (Engine) — RESOLVED.** Same-owner co-arrivals stack (fleets combine). Confirmed Stage 0 (D-007).
- **Q4 (Hygiene) — RESOLVED (Session 7, D-018).** Doc drift reconciled: `v1_1`→`v2_1` across CLAUDE.md, all `docs/architecture/*` `resource:` paths + index, and design/README prose. `AGENTS.md` was already version-agnostic. Only intentional `v1_1` strings remain (the lineage note + real `tests/test_v1_1_*.py` filenames).

---

## §9 — Next Actions 🟢 *(overwrite each session)

1. **Implement garrison release — per [`docs/design/garrison-release-plan.md`](docs/design/garrison-release-plan.md).** First *verify* which mechanism is binding (instrument `available` vs `sent` vs positive-target count on a `Producer Lite` game), then apply levers in order: A shrink the freeze lookahead → B/C reserve against the first threat only (replace `available = 0` on the holdable branch) → D anti-snipe floor. Arena-gate each vs `v2_macro` (stay ≥ parity) and watch the `Producer Lite` margin (~−4200) shrink + planet count rise.
2. **Add a reachability-gated snipe term.** Value capturing a planet at its post-combat garrison trough, only when the reachability race confirms a fleet can land inside the trough window.
3. *(Supporting)* Use `scripts/visualize.py` on a `Producer Lite` game to confirm `v2_1` expands past 2 planets after the garrison fix.

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
- `D-014 | 2026-06-18 | Reject the decision-tree architecture pivot; keep the utility/scoring core. | Strategy is resource allocation under contention — one ship pool, many competing claims — and a priority-ordered tree cannot arbitrate marginal trade-offs or split a garrison. Model the "reasons to send ships" (capture/defend/deny/evacuate/consolidate/stage/comet/bait/pin) as competing utility terms; add only a thin guard/mode layer (evacuate, defend-or-die). | §3, §7`
- `D-015 | 2026-06-18 | Prioritize three macro scoring fixes as the v2 direction: travel-time-discounted ROI, earlier garrison release, reachability-gated snipe term. | Replay diagnosis showed the Producer Lite loss is a macro/expansion failure (2-planet peak, eliminated ~turn 70), driven by raw-ROI targeting that ignores travel time plus ship hoarding — not a missed-tactics problem. The proposed planet-13 snipe was arithmetically correct but geometrically unreachable. | §7, §9`
- `D-016 | 2026-06-18 | Implement travel-time-discounted valuation via the reachability race's t_me (in v2_1/economy.py). | The old value() time term was raw Euclidean distance off a stale initial_planets position and speed-blind, not turns. Reusing t_me — the earliest credible-capture turn, already computed for the hold multiplier — makes ROI per real turn of travel and returns 0 when unreachable. Validated: v2_1 beat the frozen v2_macro 57.0% over 200 games (95% CI 50.1–63.7%, +875 avg ships). Completes Next Action #1 of D-015. | §7, §9`
- `D-017 | 2026-06-18 | Arena tooling: fix the producer_lite loader, keep BLAS/OMP thread-pinning, reject the worker cap. | (1) spec_from_file_location modules must be registered in sys.modules before exec_module or @dataclass can't resolve __module__ — fixed, producer_lite now runs. (2) Pinning math-lib threads to 1 (setdefault) gave ~6% throughput vs the torch opponent — kept. (3) The M1 Max performance-core worker cap measured slower: with threads pinned, throughput rises with worker count (10 > 9 > 8), so reverted to cpu_count-1 + an ARENA_WORKERS override. | §4`
- `D-018 | 2026-06-18 | Reconcile doc drift: repoint v1_1/ → v2_1/ across CLAUDE.md, docs/architecture (8 resource paths + index), docs/design, and README; document the D-016 t_me valuation in economy.md. | v1_1/ was folded into the v1_1→v2_macro→v2_1 lineage and deleted, leaving every doc resource: path dangling. AGENTS.md was already version-agnostic. Real tests/test_v1_1_*.py filenames preserved (they outlive the dir they pin). check_okf validates only type:, not resource:, so the drift passed conformance silently. | §7, §8, §9`

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
- `S-013 | 2026-06-18 | v2_macro | Diagnosed the Producer Lite loss from an uploaded replay. Verified the engine fleet-speed/combat math; confirmed the proposed planet-13 snipe was arithmetically correct but geometrically unreachable (earliest intercept +12 turns late). Identified the true cause as a macro/expansion failure (2-planet peak, eliminated ~turn 70). Rejected a decision-tree rearchitecture (D-014); queued three macro scoring fixes (D-015). Noted dir drift: v1_1 → v2_macro + new v(teamwork-preview)/.`
- `S-014 | 2026-06-18 | v2_1 | Created v2_1 (active dev) and made it self-contained (relative imports). Implemented travel-time valuation: value() scores ROI per t_me (reachability earliest-capture turn) instead of raw distance — beats frozen v2_macro 57% (200 games, +875 ships); still 0% vs Producer Lite (hoarding remains, → next action). Wired arena _resolve_spec for v2_1/v2_macro/producer_lite; fixed the producer_lite sys.modules loader crash. Optimized arena for M1 Max: kept BLAS/OMP thread-pinning (~6%), rejected the perf-core worker cap (more workers = faster once pinned). Logged D-016, D-017.`
- `S-015 | 2026-06-18 | v2_1 | Reconciled doc drift (D-018): repointed v1_1→v2_1 across CLAUDE.md Code layout, all 8 docs/architecture resource paths + index, targeting/economy/design prose, and README; documented the D-016 t_me valuation in economy.md. AGENTS.md needed no change. Verified zero stray v1_1 (only the lineage note + real test_v1_1_* filenames remain). Drafted the garrison-release plan (docs/design/garrison-release-plan.md): identified M1 (will_lose→available=0), M2 (30-turn trough), M3 (unreachable targets, separate fix) as hoard sources; verify-first, then levers A→B/C→D.`
