---
type: Design
title: Garrison Release — Working Plan (v2_1)
description: Plan to stop ship-hoarding in v2_1/strategy.py so idle capital expands sooner against Producer Lite. Next Action #1 after the D-016 valuation fix.
tags: [v2_1, strategy, garrison, macro, hoarding, expansion]
timestamp: 2026-06-18
resource: v2_1/strategy.py
---

# Garrison Release — v2_1 Working Plan

## Goal

After D-016 (travel-time valuation) `v2_1` ranks targets correctly but still
loses **0% / ~−4200 avg ships** to `Producer Lite` and peaks at ~2 planets. The
binding constraint is now **ship-hoarding**: idle capital never launches.
This plan releases that capital without giving planets away.

**Success = ** margin vs `Producer Lite` shrinks from ~−4200, planet count rises
past 2 earlier, and `v2_1` stays **≥ parity vs the frozen `v2_macro`** (today: 57%).
Measure, don't assume — one lever at a time.

## Where the capital is frozen

All of it is the `available[src.id]` computation in `decide()`
(`v2_1/strategy.py` lines 66–105). `available` is how many ships a planet may
send this turn. Three mechanisms hold ships back:

```python
# lines 72–77 — freeze lookahead
for T in range(1, min(MAX_PRECOMPUTE, 30) + 1):
    if timeline.owner_at(T) != state.me:
        will_lose = True
        break
    min_garrison = min(min_garrison, timeline.garrison_at(T))
```

```python
# lines 95–101 — release decision
if will_lose:
    if unholdable:
        available[src.id] = src.ships   # evacuate
    else:
        available[src.id] = 0           # hold tight — FREEZES THE WHOLE GARRISON
else:
    available[src.id] = max(0, min_garrison)   # release down to the 30-turn trough
```

- **M1 — `will_lose → available = 0` (lines 95–99).** Any planet forecast to
  flip within 30 turns but judged holdable contributes **zero** offense — its
  entire garrison sits idle "waiting for reinforcements." This is the single
  largest hoard.
- **M2 — 30-turn trough (lines 73, 77, 101).** `min_garrison` is the *minimum*
  forecast garrison over the next 30 turns. A committed enemy fleet 20–30 turns
  out drops the trough and freezes ships **now** — even though the planet's own
  production replenishes during the enemy's travel, and reinforcements can cover
  a far threat later. This is the "frozen capital" lesson, only partly tamed by
  the 30-turn cap.
- **M3 — no destination (cross-ref, not this fix).** Post-D-016, `value()`
  returns 0 when a target is not credibly reachable (`t_me is None`). With one
  early base, many planets score 0, so even *released* ships have nowhere to go.
  That is target-gating, Next Actions #2/#3 — keep it separate so we don't
  conflate two fixes.

## Verify the diagnosis first (cheap, ~30 min)

The tracker assumes the fix is "relax `min_garrison`." Before touching it,
confirm **where** ships stall — the D-016 lesson was exactly *re-read the code
before trusting a symptom-based diagnosis*. Add a one-turn debug line logging:

- `total_owned` ships, `sum(available)`, `sum(sent_this_turn)`
- count of targets with `score_target > 0`, and count zeroed by `t_me is None`

Run one `Producer Lite` game through `scripts/visualize.py`. Two outcomes:

- **`available` is small** (ships frozen at source) → M1/M2 are binding → do the
  levers below.
- **`available` is large but `sent` is small / few positive targets** → the wall
  is M3 (reachability gating), *not* `min_garrison` → this plan is the wrong
  lever; pivot to Next Action #2/#3 and say so in the tracker.

This keeps us honest and stops us "fixing" a knob that isn't the constraint.

## Levers (ponytail order — smallest knob first)

**A — shrink the freeze lookahead.** `min(MAX_PRECOMPUTE, 30)` → a smaller
horizon (try 10–12), or tie it to `t_enemy` so only *imminent* committed threats
freeze capital. One number, instantly A/B-able. Why it works: production over a
long horizon already covers far threats; freezing now wastes the enemy's travel
buffer.

**B — partial release on the holdable branch (targets M1, the biggest hoard).**
Replace `available = 0` with a defensive *reserve*, not the whole garrison:

```python
else:
    reserve = required_to_hold(src, t_enemy, f_enemy)   # survive the FIRST threat only
    available[src.id] = max(0, src.ships - reserve)
```

`reserve` = ships needed to survive the earliest committed enemy arrival, from
the values `value()` already caches (`t_enemy`, `f_enemy` in `reachable_cache`)
plus `physics.arrival_garrison` / `required_to_capture` (reuse the oracle — do
**not** re-derive combat math). Releases surplus while keeping the planet
defensible.

**C — redefine `min_garrison` as "survive the next threat event," not the
30-turn trough.** A cleaner restatement of A+B: reserve against the *first*
arrival event, release everything above it. Pick C *or* A+B, not both.

**D — anti-snipe floor (guardrail).** Keep a small floor on the home/core base
so over-release doesn't get it sniped (the replay's opposite failure mode). A
flat floor or `production * k` is enough; gate by the reachability race already
in hand.

Recommended: **verify → A → measure → B/C if margin still bad → D as guardrail.**

## Validation

Arena hooks for `v2_1` / `v2_macro` / `producer_lite` already exist (D-017).

```bash
# parity guard (must not regress vs the frozen prior baseline)
PYTHONPATH=. python scripts/arena.py --a v2_1/agent.py --b v2_macro/agent.py --games 40 --steps 150
# the boss (no --steps; ladder length is 500)
PYTHONPATH=. python scripts/arena.py --a v2_1/agent.py --b producer_lite --games 200
```

Watch: **win-rate + mean score margin** (baseline 0% / ~−4200) and **planet
count over time** (`scripts/visualize.py` — confirm v2_1 holds >2 planets
earlier). Change one lever, re-measure, keep or revert. Stay ≥ parity vs
`v2_macro` throughout.

## Risks & guardrails

- **Over-release → piecemeal capture or home snipe.** Mitigate with lever D's
  floor and by keeping the reachability gate; never send below the first-threat
  reserve (B/C).
- **Regression vs `v2_macro`.** The 40-game smoke is the gate; if parity drops,
  the lever is wrong — revert.
- **Conflating M1/M2 with M3.** If the verify step says M3, stop and re-route.

## Hard constraints (docs/conventions.md)

- **Oracle protection.** Don't edit `physics.py` or the math in `targeting.py`;
  the reserve calc reuses `physics.arrival_garrison` / `required_to_capture`.
- **Determinism.** No new `random` / `np.random`.
- **Performance.** Reuse `reachable_cache`; add no O(T) scan per planet.
- **Knowledge before code.** A change to the release contract updates
  `docs/architecture/strategy.md` (and `economy.md` if `value`'s use shifts) in
  the same change, then `PYTHONPATH=. python scripts/check_okf.py docs`.
- **Append-only memory.** Log the landed fix as the next decision (D-019) plus a
  changelog entry; update §7–§9 live state.
