# Orbit Wars Agent

This directory contains the Kaggle agent source code. The agent runs as a single Python entry point (`agent.py:act`), parses the environment observation, and computes optimal launch commands.

## Architecture Overview

The core loop relies on separating state parsing from decision logic, while heavily utilizing a precomputed physics engine to stay within real-time turn limits.




```mermaid
graph TD
    Env["Kaggle Environment"] --> ObsDict["Observation Dictionary"]
    ObsDict --> Agent["agent.py: act"]
    Agent --> ObsNode["obs"]

    subgraph Data Parsing
        StateParse["state.py: parse"]
    end
    ObsNode --> StateParse
    StateParse --> StateNode1["state"]

    subgraph Decision Making
        Strategy["strategy.py: decide"]
        StateNode2["state"]
        Target["targeting.py: plan"]
        Strategy --> StateNode2 --> Target
    end
    StateNode1 --> Strategy

    subgraph Targeting Logic
        GTC["Global Trajectory Caching"]
        DRP["Defense Reserve Prediction"]
        TS["Target Scoring"]
        SFA["Synchronized Fleet Arrivals"]
    end

    Target --> GTC
    Target --> DRP
    Target --> TS
    Target --> SFA

    CmdGen["Command Generation"]
    Target --> CmdGen

    Phys1["planet_position"]
    Phys2["predict_fleet_target"]
    Phys3["hits_sun"]

    GTC --> Phys1
    DRP --> Phys2
    SFA --> Phys3

    CmdGen --> EnvOut["Kaggle Environment"]
```

## Synchronized Fleet Arrivals (v1 Logic)

To prevent enemy defensive reserves from picking off our attacking fleets one-by-one, the targeting logic utilizes a synchronized arrival strategy. It targets a planet at a specific future time (`delta_t`) and coordinates launches across multiple owned planets so they land exactly on the same turn.

```mermaid
sequenceDiagram
    participant Far as Far Planet
    participant Close as Close Planet
    participant Target as Target Planet
    
    Note over Far, Target: Agent selects a target for Turn T + 10
    
    Far->>Target: Travel Time: 10 turns (Delay: 0)
    Note over Far: Launches IMMEDIATELY
    
    Close->>Target: Travel Time: 7 turns (Delay: 3)
    Note over Close: Waits 3 turns before launching
    
    Note over Target: Both fleets hit the garrison simultaneously at T + 10
```

## Module Responsibilities

- **`agent.py`**: The interface for the Kaggle environment. Wires the parser to the strategy.
- **`state.py`**: Typed data structures (`State`, `Planet`, `Fleet`, `Comet`) and observation parsing.
- **`strategy.py`**: Per-turn policy interface. Currently acts as a pass-through to `targeting.py`.
- **`targeting.py`**: The core AI logic (ROI targeting, defensive reserves, and synchronized launch delays).
- **`physics.py`**: Exact extraction of the Kaggle environment's continuous math, used for predictive raycasting, line-of-sight checks, and trajectory generation.
