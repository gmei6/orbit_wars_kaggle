---
type: Readme
---

# Orbit Wars Agent — v2_macro

> **Active development copy.** Macro changes happen here. The frozen baseline is
> [`../v1/`](../v1/); the two diverge here via the v2 Information Model.

This directory is the Kaggle agent. It runs as a single Python entry point
(`agent.py:act`), parses the environment observation, and computes launch
commands, leaning on a precomputed physics oracle to stay inside real-time turn
limits.

## Architecture (v2 Information Model)

v2_macro implements the v2 Information Model. Instead of a monolithic `targeting.py`, it separates forecasting (`timeline.py`), strategic valuation (`economy.py`), and reachability races (`reachability.py`).

```mermaid
graph TD
    Env["Kaggle Environment"] --> Agent["agent.py: act"]
    Agent --> Parse["state.py: parse"]
    Parse --> Timeline["timeline.py: forecast"]
    Timeline --> Strategy["strategy.py: decide (the brain)"]

    subgraph Brain["Decision making — strategy.py"]
        TS["Target scoring (ROI valuation)"]
        DR["Defense unfreezing"]
        SFA["Synchronized fleet arrivals"]
        CmdGen["Command generation"]
    end
    Strategy --> TS
    Strategy --> DR
    Strategy --> SFA
    SFA --> CmdGen

    subgraph Economy & Reachability
        ECO["economy.py: value(P), production_integral"]
        RCH["reachability.py: reachable(P)"]
    end
    TS --> ECO
    DR --> RCH

    subgraph Physics["Physics — physics.py"]
        PP["planet_position"]
        TT["get_travel_time"]
        LC["lane_clear"]
    end
    Timeline --> PP
    RCH --> TT
    SFA --> LC

    subgraph Math Oracle
        GTC["targeting.py: get_trajectory_cache"]
    end
    Timeline --> GTC
    GTC --> PP

    CmdGen --> EnvOut["Kaggle Environment"]
```

## Synchronized Fleet Arrivals

To stop enemy reserves from picking off attackers one-by-one, `strategy.decide`
targets a planet at a chosen future turn (`delta_t`) and staggers launches across
owned planets so every fleet lands on the same turn. The travel-time and
attack-window math come from `reachability.py` and `physics.py`.

```mermaid
sequenceDiagram
    participant Far as Far Planet
    participant Close as Close Planet
    participant Target as Target Planet

    Note over Far, Target: strategy selects a target for Turn T + 10

    Far->>Target: Travel Time: 10 turns (Delay: 0)
    Note over Far: Launches IMMEDIATELY

    Close->>Target: Travel Time: 7 turns (Delay: 3)
    Note over Close: Waits 3 turns before launching

    Note over Target: Both fleets hit the garrison simultaneously at T + 10
```

## Module Responsibilities

- **`agent.py`**: The Kaggle interface. Wires the parser to the strategy
  (`act → parse → decide`). One line of logic.
- **`state.py`**: Typed data structures (`State`, `Planet`, `Fleet`, `Comet`)
  and observation parsing. `parse` is the only integration seam with the env.
- **`timeline.py`**: Forecasts future state by folding arriving fleets chronologically. Provides `garrison_at(T)` and `owner_at(T)`.
- **`economy.py`**: Calculates target ROI (`value(P)`) and tracks the production-integral metric.
- **`reachability.py`**: Calculates the fastest credible arrival times (`reachable(P)`) to define defense thresholds and strike windows.
- **`strategy.py`**: The brain. Owns target scoring, defense-reserve allocation,
  synchronized launch delays, and command generation.
- **`targeting.py`**: Legacy pure-math oracle. Primarily provides `get_trajectory_cache`.
- **`physics.py`**: Exact extraction of the Kaggle environment's continuous math
  — orbital positions, fleet-target prediction, sun line-of-sight, and travel times.
