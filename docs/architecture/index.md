# Architecture

One concept document per module. Each binds to a code path via its `resource:`
field, so an agent can route from a question to the right doc, then to the
right code.

* [Module template](_module-template.md) - copy this to start a new module doc

# Modules

* [Physics](physics.md) — frozen rules/oracle: speed, radius, sun, combat (`src/physics.py`)
* [State](state.md) — parse the observation into typed entities (`src/state.py`)
* [Targeting](targeting.md) — pick targets, size fleets vs the arrival garrison (`src/targeting.py`)
* [Strategy](strategy.md) — per-turn policy / command generation (`src/strategy.py`)
* [Agent](agent.md) — Kaggle entry point (`src/agent.py`)

Local engine `src/sim.py` is test tooling (seeded self-play), not a module doc.

Keep this list in sync — or generate it (see the upgrade path in
[/workflow.md](/workflow.md)).
