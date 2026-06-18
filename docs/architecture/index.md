# Architecture

One concept document per module. Each binds to a code path via its `resource:`
field, so an agent can route from a question to the right doc, then to the
right code.

* [Module template](_module-template.md) - copy this to start a new module doc

# Modules

* [Physics](physics.md) — frozen rules/oracle: constants, speed, sun, capture, combat (`v1_1/physics.py`)
* [State](state.md) — parse the observation into typed entities (`v1_1/state.py`)
* [Timeline](timeline.md) — event forecasting and chronological arrival folding (`v1_1/timeline.py`)
* [Reachability](reachability.md) — fast-arrival tracking and time-margin races (`v1_1/reachability.py`)
* [Economy](economy.md) — ROI valuation and production integrals (`v1_1/economy.py`)
* [Targeting](targeting.md) — legacy pure-math oracle: trajectory caching (`v1_1/targeting.py`)
* [Strategy](strategy.md) — the decision brain: target selection, defense reserves, synchronized arrivals (`v1_1/strategy.py`)
* [Agent](agent.md) — Kaggle entry point; wires parse → decide (`v1_1/agent.py`)

These docs track `v1_1/` (active development), which uses the v2 Information Model. The frozen `v1/` baseline mirrors
them, except its decision logic lives in `targeting.py` rather than `strategy.py`, and it lacks timeline/economy modules.

Local engine `scripts/sim.py` is test tooling (seeded self-play), not a module doc.

Keep this list in sync — or generate it (see the upgrade path in
[/workflow.md](/workflow.md)).
