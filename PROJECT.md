# Project: Orbit Wars v2 Macro Strategy

## Architecture
Our agent is structured into two main tracks:
1. **Implementation Track (`v2_macro/`)**: Adapts the timeline-based forecasting and reachability models of `v1_1` to build a macro strategy that out-scales `Producer Lite`.
2. **E2E Testing Track**: Build requirement-driven tests to verify correctness, boundary behavior, and ensure zero-regression on baseline capabilities.

### Code Layout
```
/Users/garymei/Downloads/oribt-wars/
├── v2_macro/
│   ├── agent.py       # Kaggle entry point
│   ├── state.py       # Observation parses
│   ├── physics.py     # Trajectory and combat mechanics
│   ├── targeting.py   # Pure math & caching helpers
│   ├── timeline.py    # Eventtimeline forecasting
│   ├── reachability.py# Reachability logic (threat & support races)
│   ├── economy.py     # Target ROI valuation & production-integral curves
│   └── strategy.py    # Decider brain (launches, garrison allocation)
├── tests/             # Unit and integration tests
├── scripts/           # Benchmarking & verification tools
└── .agents/           # Agent coordination metadata
```

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Diagnose v1_1 Deficits | Spawn Explorer to run benchmarks, inspect v1_1 logs, and identify why capital unfreezing fails | None | PLANNED |
| 2 | Setup v2_macro & Test Track | Duplicate v1_1 baseline into v2_macro; initialize E2E test infra and write E2E/unit tests | M1 | PLANNED |
| 3 | Optimize Macro Strategy | Implement optimized reachability thresholds, capital unfreezing adjustments, and expansion logic in v2_macro | M2 | PLANNED |
| 4 | Benchmarking & Forensic Audit | Validate v2_macro against v1_1 and Producer Lite; run Challengers/Reviewers/Auditor | M3 | PLANNED |

## Interface Contracts
### `strategy` ↔ `state` / `targeting` / `timeline`
- `decide(state)`: returns list of commands `[[source_planet_id, angle, ships], ...]`.
- `build_timeline(state, trajectory_cache, max_turns)`: returns map of planet timelines.
- `reachable(planet_id, side, state, timelines, trajectory_cache)`: returns `(earliest_turn, max_force)`.
- `value(planet_id, side, state, timelines, trajectory_cache, reachable_cache)`: returns ROI score.
