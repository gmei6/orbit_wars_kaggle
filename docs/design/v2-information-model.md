---
type: Design
title: v2 Information Model & Strategy
description: How the agent stores game state (the forecastable baseline) and the doctrine and build plan for v2 macro play.
resource: v1_1/
tags: [design, strategy, information-model, economy, v2]
timestamp: 2026-06-17
---

# Core model: determinism + observability

The game is deterministic *except for new launches*. Orbits are periodic
(precompute all 500 turns once), comet paths are fixed, and any fleet already
in flight is a committed straight-line projectile — it cannot change heading
or speed. The only non-deterministic input is each player's *next* launch.

Two ways to know the future, used together:

- **Observe.** Every turn Kaggle returns the true observation — planet owners,
  ship counts, fleets. This is ground truth; we never hand-track enemy
  garrisons.
- **Forecast.** Between turns, project the committed baseline forward to plan.
  The forecast is exact for in-flight fleets and degrades only where it must
  guess the enemy's *future* launches. Each turn, overwrite the forecast with
  the new observation.

Design rule: store the baseline; treat any launch — ours or a hypothetical we
are evaluating — as a cheap perturbation of it, not a recompute.

# Garrison as a function of time

A garrison is not a scalar to mutate. It is a function of time:

```text
garrison(t) = base + production * (t - t_last_event)     # resets at each arrival/flip
```

`owner(t)` is derived the same way, by folding arrival events in time order.

# Structures

## 1. Per-planet event timeline (the spine)

Per planet, store:

```text
owner_now, garrison_now, production, position[t]   # position from the orbital precompute
arrivals: sorted [(turn, owner, ships), ...]        # every fleet projected to hit this planet
```

`garrison_at(T)` / `owner_at(T)` fold the arrivals in turn order: accrue
production between events, apply combat at each event, flip the owner on
capture (which changes accrual afterward). This single structure answers
defense need, capture cost, snipe surplus, and hold window. A hypothetical
launch is just "insert one event, re-fold the tail after it."

A dense per-turn vector is the wrong shape: it breaks the moment a planet flips
mid-window (every later cell is conditioned on the new owner). Materialize a
dense array from the events only as a read-cache if needed; the events stay the
source of truth.

This replaces the naive `calculate_defense_needs` in
[targeting](/architecture/targeting.md), which sums incoming enemy ships
ignoring arrival order, ownership flips, and survival.

> **Resolved (Stage 0, decision D-007).** Same-owner co-arrivals **stack**
> (additive force); multi-owner contention reduces by top-two. The fold calls
> `physics.resolve_combat(planet_owner, garrison, [(owner, ships), ...])`, now
> updated in `v1_1/physics.py` and pinned by `tests/test_v1_1_physics.py`. This
> also confirms v1's synchronized arrivals are engine-valid, not self-defeating.

## 2. Travel / intercept layer (size-aware)

No pathfinding exists in this game: a fleet flies one fixed angle in a straight
line. So "shortest path" collapses to **straight-line distance if the lane is
sun-clear, else blocked** (give up, or multi-hop via an intermediate planet —
deferred). Travel *time* is size-aware, because bigger fleets move faster:

```text
travel_time(src, dst_pos, ships) = ceil(max(0, dist - target_radius) / fleet_speed(ships))
```

Split the distance work by motion (Gary's refinement):

- **Stationary ↔ stationary:** distance constant → precompute a small table once.
- **Inner ↔ inner:** also constant (planets co-rotate rigidly about the sun at
  the shared angular velocity) → precomputable.
- **Anything ↔ exactly one mover (inner ↔ outer):** distance varies with `t`.
  Compute on demand, and as an **intercept** — aim at the planet's *future*
  position, not its current one. The oracle already does this
  (`physics.intercept_time` / `predict_fleet_target`).

`lane_clear(src, dst_pos) = not hits_sun(...)`; time-varying whenever an
endpoint moves. Reuses [physics](/architecture/physics.md); consolidate the
duplicated speed formula (see Stage 2).

## 3. Reachability race (threat & support)

A threat to planet P is real only if the enemy can win the race to it:

```text
t_enemy = earliest credible enemy arrival at P
t_me    = fastest I can land support / retake P
F_enemy = max enemy ships that can converge by t_enemy   # concurrency matters (synchronized arrivals)
```

Hold P iff `t_me <= t_enemy` and I can muster more than `F_enemy`. Otherwise
give the planet up — do not pour ships into a loss — and consider a later
snipe. "Credible" is force-weighted: an enemy rotating into range with 5 ships
is no threat to a 200-ship planet, so geometric reachability over-counts.

## 4. Planet valuation

```text
value(P) ~= production(P) * hold_probability(P) - capture_cost(P)
```

- **Inner (moving):** offensive asset — its orbit sweeps it into strike range —
  but harder to hold (it also sweeps into *enemy* range). Offensive value is
  **windowed**: store the turn intervals where inner P wins the reachability
  race against a target, e.g. "P can take Q during turns 80–95."
- **Outer (static):** predictable threat geometry → easier to reinforce/hold;
  weaker offense. Edge position can mean isolation (fewer supporters).

Do not hardcode an inner/outer preference. Derive the offense/defense lean from
the reachability race and the economy state below.

## 5. Economy scoreboard (the referee)

Track both players' production income over time and the projected curve if
pending captures resolve. The objective is to **maximize our own
production-integral over the remaining turns** — total ships generated — not to
win individual fights. This is the metric that says whether the current
aggressive/defensive lean is working, and it directly targets the macro deficit
behind the `Producer Lite` loss (tracker §7).

# Doctrine (playstyle)

- **Cautious expansion by default.** Grab economically efficient, *holdable*
  planets; garrison only as much as the reachability race demands — freeing the
  "frozen capital" the lessons-learned flags.
- **Awareness.** Classify every enemy launch via `owner_at(arrival_turn)`: is it
  projected to take a planet I will own at that turn?
- **Phases are per-front, not global.** A poke on one flank triggers local
  defense only; keep expanding elsewhere. "No attack yet" is not "expansion is
  going well" — an economy bot may never strike first.
- **Opportunistic knockout.** Hold for a first strike that puts the opponent at
  a *decisive*, not marginal, disadvantage (a coordinated snipe that flips a key
  producer or punishes an overcommitted fleet). Otherwise default to defend +
  expand.
- **Give up unholdable planets**; plan the retake or snipe instead.

# Open questions

- **Q2 — RESOLVED (Stage 0).** Same-owner co-arrivals stack (additive), so v1
  synchronized arrivals are engine-valid. See `v1_1/physics.py:resolve_combat`.
- **Thresholds:** what time-margin and force-ratio count as "wins the
  reachability race" and as a "decisive" knockout.
- **Multi-hop routing** around the sun: real capability or YAGNI?

# Modular build plan

Staged so each rung is independently testable via
[`scripts/arena.py`](/../scripts/arena.py) (self-play, Wilson intervals) and
[`scripts/sim.py`](/../scripts/sim.py). All work lands in `v1_1/`. Each stage is
arena-gated: no regression vs. `v1`, measured vs. `Producer Lite`.

- **Stage 0 — Resolve Q2 (DONE, 2026-06-17, D-007).** Confirmed against the
  engine: same-owner fleets **stack**. `v1_1/physics.py:resolve_combat` updated
  and pinned by `tests/test_v1_1_physics.py`.
- **Stage 1 — Event timeline.** New `v1_1/timeline.py`: build per-planet
  `arrivals` from `state.fleets` via the intercept layer; implement
  `garrison_at` / `owner_at`. Retire the naive `calculate_defense_needs`. Test:
  forecast vs. a vendored-engine rollout with no new launches must match
  exactly.
- **Stage 2 — Travel/intercept cleanup.** Consolidate `get_travel_time` +
  `fleet_speed` (kill the inline speed duplicate in `targeting.py` —
  oracle protection); add the stationary-pair distance table and `lane_clear`.
  Test: parity vs. the physics oracle.
- **Stage 3 — Reachability race.** `reachable(P, side) -> (earliest_turn,
  max_force)` over the timeline + travel layer. Test on seeded boards.
- **Stage 4 — Valuation + economy scoreboard.** `value(P)` and the
  production-integral projection. Test: scoreboard tracks a known sim.
- **Stage 5 — Strategy rewrite (`v1_1/strategy.py`).** Cautious-expand sized by
  `value` + reachability; per-front defense off the timeline; snipe detection
  via `owner_at` + surplus; knockout trigger gated on a decisive-advantage
  check. Benchmark vs. `Producer Lite` after each sub-step.
- **Stage 6 — Tune thresholds.** Strike-range and knockout-decisiveness, via
  arena Wilson intervals.

Dependencies: `1 ← 0`, `2` independent, `3 ← {1,2}`, `4 ← 1`, `5 ← {1,2,3,4}`,
`6 ← 5`.
