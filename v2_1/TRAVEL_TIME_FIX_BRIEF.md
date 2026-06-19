---
type: Brief
title: Travel-Time-Discounted Valuation — Working Brief (v2_1)
description: Everything needed to fix value() so target ROI is scored per turn, not per raw distance.
tags: [v2_1, economy, value, ROI, macro, travel-time]
timestamp: 2026-06-18
---

# Travel-Time-Discounted Valuation — v2_1 Working Brief

Goal of this fix (Next Action #1, decision D-015): make `value()` score ROI
*per turn of travel*, so near/cheap neutrals outrank far/expensive ones and the
agent stops peaking at 2 planets vs `Producer Lite`.

## TL;DR

- The fix lives in **`v2_1/economy.py` → `value()` (lines 31–86)**, specifically
  the travel-time block at **lines 49–60**.
- **Surprise / correction to the tracker:** `value()` does **not** "ignore
  travel time." It already divides by a distance term. The real defect is that
  the term `T` is **raw Euclidean distance, not turns** — plus a coordinate
  mismatch and speed-blindness. So this is a *fix the broken term*, not *add a
  missing term*.
- **Two blockers must be cleared first or your edits won't execute** (the v2_1
  files import from the `v2_macro` package, and `arena.py` has no v2_1 hook).
  See §6.

---

## 1. What the code does now

The relevant slice of `v2_1/economy.py` (`value()`):

```python
target_p = state.initial_planets[P_id]                 # L47  (t=0 position)

min_T = float('inf')                                   # L51
for src in my_planets:                                 #   my_planets = current planets
    if src.id == P_id: continue
    dist = math.hypot(src.x - target_p.x, src.y - target_p.y)   # L54  current src vs INITIAL target
    min_T = min(min_T, dist)

T = max(1.0, min_T)                                     # L57  <-- a DISTANCE, used as time
R = 500 - state.step                                   # L58  remaining turns

profit = timeline.production * max(0, R - T) - cost     # L60
roi = profit / T                                        # L61
if roi <= 0: return 0.0
# ... then hold_multiplier ∈ {0.5, 1.0, 1.5} from the reachability race (L65–85)
return float(roi * hold_multiplier)                     # L86
```

Conceptually the **shape is already correct**: `roi = (lifetime profit) / (time
to first return)`, where lifetime profit discounts the holding window by travel
time `(R − T)`. That *is* "ROI per turn." The bug is purely what `T` measures.

## 2. Why it underperforms — four concrete defects

1. **`T` is distance, not turns (dimensional bug).** Fleets move at
   `fleet_speed(ships)` ∈ [1.0, 6.0] units/turn (`physics.py` L19–23). Real
   travel time = distance ÷ speed (and `physics.travel_time` also subtracts the
   target radius and `ceil`s). Using raw distance overstates time by up to 6×
   and, worse, makes `R − T` subtract *units* from *turns*.
2. **Coordinate mismatch.** Target position comes from
   `state.initial_planets[P_id]` (turn-0), but sources use current `src.x/src.y`.
   Inner planets rotate (`planet_position`, L111–120), so for them this distance
   is stale.
3. **Speed-blind.** `value()` doesn't know how many ships it will send, so it
   can't pick a speed. The reachability oracle already solves this: `reachable()`
   returns the size-aware *earliest arrival turn*.
4. **Window term is nearly inert.** With `R = 500 − step` ≈ 500 and `T` a board
   distance (≤ ~110), `max(0, R − T)` barely moves, so ranking collapses to
   roughly `production / distance × hold_multiplier`. Directionally OK, but
   speed-blind and coordinate-stale.

**Worked example** (step 0, hold_multiplier folded out):

| Target | production | dist `T` | cost | profit = prod·(R−T) − cost | roi = profit/T |
|--------|-----------:|---------:|-----:|---------------------------:|---------------:|
| near cheap | 2 | 10 | 20 | 2·490 − 20 = 960 | **96.0** |
| far rich   | 10 | 60 | 105 | 10·440 − 105 = 4295 | 71.6 |

Near already wins — but only by raw distance. A *big* fleet would reach the far
target ~6× faster than this assumes, and a rotating inner target's distance is
wrong. Real turns sharpen and correct the ranking.

## 3. Tools you already have (reuse — don't rebuild)

- **`physics.transit_turns(distance, ships)`** and
  **`physics.travel_time(sx, sy, tx, ty, target_radius, garrison)`** → integer
  turns, size-aware, radius-aware. `physics.py` is the **frozen oracle** — call
  it, never edit it.
- **`reachability.reachable(P_id, side, state, timelines, trajectory_cache)`**
  → `(earliest_turn, force)`. `value()` **already calls this** and caches it as
  `t_me` / `t_enemy` (L67–76) — but only uses it for `hold_multiplier`.
  **`t_me` is exactly the size-aware travel time you want, already computed.**
- **`trajectory_cache[P_id][delta_t-1]`** → the target's future `(x, y)` at
  relative turn `delta_t`. Use this for a *consistent* position instead of
  `initial_planets`.

## 4. Fix options (pick one; recommended order)

**Option A — Ponytail-minimal: reuse `t_me` as the time term.** It is already
computed, size-aware, uses future positions, and costs nothing extra. Move the
reachability block above the ROI math and set `T = t_me`:

```python
# after computing t_me from reachable_cache:
if t_me is None:           # we can't credibly reach it yet
    return 0.0             # (or a large T to heavily discount, if you'd rather keep it)
T = float(t_me)
R = 500 - state.step
profit = timeline.production * max(0, R - T) - cost
roi = profit / T
```

This collapses defects 1–3 in one move. Measure before doing anything fancier.

**Option B — Explicit physics call.** If you want `value()` independent of the
reachability threshold, compute the time yourself with a *consistent future
position* and a nominal fleet size (e.g. the capture `cost`, since speed scales
with fleet size):

```python
pos = trajectory_cache[P_id][0]            # or [min_T_guess] for a fixed-point pass
tx, ty = pos if pos else (target_p.x, target_p.y)
nominal = max(1, cost)
T = min(travel_time(src.x, src.y, tx, ty, target_p.radius, nominal)
        for src in my_planets if src.id != P_id)
```

**Option C — Borrow the opponent's proven shape.** `Producer Lite` multiplies
each candidate's score by `1.0 / (1.0 + dist / 15.0)`
(`opponents/producer_lite/opp_producer.py` L651) plus a strategic-alignment
cosine term. If A/B underperform, a distance multiplier of that form is a
known-good fallback — but it's less principled than turns-based ROI.

**Recommendation:** A first (cheapest, consistent, zero added cost) → unit-test
→ arena. Escalate to B/C only if the signal says so.

## 5. Hard constraints (from docs/conventions.md + CLAUDE.md)

- **Oracle protection.** Do not edit `physics.py` (pinned to
  `addons/quant/baselines.json`) or the pure math in `targeting.py`. Reuse them.
- **Knowledge before code.** Changing `value()`'s contract means updating
  `docs/architecture/economy.md` *in the same change*, then run
  `PYTHONPATH=. python scripts/check_okf.py`.
- **Determinism.** No new `random`/`np.random`; one seed source if you ever add
  sampling.
- **Performance.** Keep the shared `reachable_cache`. Don't add an O(T) scan per
  `value()` call — `score_target` runs it ~twice per planet per turn.

## 6. Blockers to clear FIRST (or edits to v2_1 silently run v2_macro)

**(a) Import footgun — v2_1 is not self-contained.** These files import the
`v2_macro` *package*, so editing v2_1 has no effect through `agent.py`:

- `v2_1/economy.py` L4–6 → `from v2_macro.state/timeline/reachability import …`
- `v2_1/reachability.py` L5–7 → `from v2_macro.state/timeline/physics import …`
- `v2_1/agent.py` L5–6 → `from v2_macro.state import parse`, `from v2_macro.strategy import decide`
- `v2_1/__init__.py` L1 docstring says "v2_macro package"; `v2_1/strategy.py`
  L158 logs to `/tmp/v2_macro_debug.log`.

`strategy.py`, `targeting.py`, `timeline.py` already use **relative** imports and
are fine. **Fix:** make the three offenders relative (`from .state import …`),
or `sed -i 's/v2_macro/v2_1/g' v2_1/*.py`. Then `v2_1/agent.py` actually runs
v2_1's brain. (Aside: that debug-log line writes on every launch — drop it.)

**(b) Arena has no v2_1 hook.** `scripts/arena.py` `_resolve_spec` (L82–93)
knows `v1`, `v1_1` (stale — that dir is gone), and `main.py`. Add:

```python
if spec == "v2_1/agent.py":
    import importlib
    return getattr(importlib.import_module("v2_1.agent"), "act")
```

`Producer Lite`'s entrypoint is **`agent`** (not `act`), needs `torch`, and
self-inserts its vendored `orbit_lite` dir. Add a branch returning
`opp_producer.agent`, or pass its path as `--b`.

**(c) `sim.py` is the wrong harness.** It's hardwired to `v1` on a static
4-planet map with no orbits/comets (`scripts/sim.py` L8, L18–27). It cannot
exercise v2_1 macro vs Producer Lite. Use `arena.py` (real Kaggle env).

**(d) Tests point at v2_macro.** Copy `tests/test_v2_macro_economy.py` →
`tests/test_v2_1_economy.py` (swap imports to `v2_1`). The current `test_value`
only asserts the result is a float — strengthen it to assert a near-cheap planet
outranks a far-rich one (your actual regression guard for this fix).

## 7. How to validate

- **Unit:** `PYTHONPATH=. pytest tests/test_v2_1_economy.py -v`
- **Smoke self-play:**
  `PYTHONPATH=. python scripts/arena.py --a v2_1/agent.py --b v2_macro/agent.py --games 40 --steps 150`
  (should be ≈ parity or better — proves v2_1 runs and the change isn't a
  regression).
- **Real eval vs the boss:**
  `PYTHONPATH=. python scripts/arena.py --a v2_1/agent.py --b <producer_lite_path> --games 200`
  (no `--steps`; ladder length is 500).
- **Watch:** win-rate + **mean score margin** (baseline today: 0% / **−4163**
  avg ships). Macro tell: **planet count over time** — render a game with
  `scripts/visualize.py` and confirm v2_1 expands past 2 planets earlier.

## 8. Suggested loop

1. Clear blockers (a), (b), (d). Confirm v2_1 plays in arena at ~parity with
   v2_macro.
2. Implement Option A in `value()`. Make the near>far unit test pass.
3. Arena smoke vs v2_macro, then 200 games vs Producer Lite. Watch margin shrink
   and planet count rise.
4. If margin improves but you're still losing, that's the handoff to Next
   Action #2 (release garrison earlier) — hoarding, not valuation, becomes the
   binding constraint. Keep them separate so each is measured on its own.
5. Update `docs/architecture/economy.md`; run `check_okf.py`; log a decision
   (D-016) + changelog entry per the tracker's append-only rule.

## Open question to resolve while coding (tracker Q2)

Should a **reachability-gated snipe** term live in `value()` too? It's Next
Action #3, not this fix — but if you touch the reachability block for Option A,
note where a snipe term would slot in so you don't have to re-thread it later.
