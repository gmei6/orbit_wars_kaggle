---
type: Readme
---

# Orbit Wars Kaggle Agent

Agent for the Orbit Wars Kaggle competition. Strict oracle/physics separation,
synchronized-arrival fleet targeting, and an Open Knowledge Format (OKF v0.1)
documentation bundle.

Project state, roadmap, and decisions live in
**[`PROJECT_TRACKER.md`](PROJECT_TRACKER.md)** (read it first); recurring
pitfalls in **[`LESSONS_LEARNED.md`](LESSONS_LEARNED.md)**.

## Layout

The agent ships as a Python package, kept in parallel copies — a frozen baseline per milestone plus the active dev copy:

- **[`v1/`](v1/)** — frozen baseline. `targeting.py` holds the decision logic;
  `strategy.py` is a thin pass-through. The arena measures candidates against it.
- **[`v2_1/`](v2_1/)** — active development. Implements the v2 Information Model with timeline forecasting, reachability race logic, and economy-driven ROI valuation (travel-time-discounted, D-016). Lineage `v1_1` → `v2_macro` → `v2_1`; beats the frozen `v2_macro` 57% and wins outright vs the `v1` baseline.
- **[`v2_macro/`](v2_macro/)** — frozen prior baseline; the v2 arena yardstick. The old `v1_1/` dir was folded into this lineage and no longer exists.

Both packages share the same modules:

| Module | Role |
|--------|------|
| `agent.py` | Kaggle entry point. `act(obs)` → `parse` → `decide`; one line of wiring. |
| `state.py` | Parse the raw observation into typed `Planet` / `Comet` / `Fleet` / `State`. |
| `physics.py` | The oracle: frozen constants and game math (speed, sun collision, capture, combat). No strategy. |
| `targeting.py` | v1: greedy targeting + fleet sizing. v2_1: pure-math helpers (trajectory cache, defense/attack calc). |
| `strategy.py` | v1: pass-through to targeting. v2_1: the brain — scoring, defense reserves, synchronized launches. |

Supporting trees:

- **[`scripts/`](scripts/)** — `arena.py` (self-play eval: antithetic seat-swap + Wilson CI), `sim.py` (minimal local engine), `check_okf.py` (docs conformance).
- **[`tests/`](tests/)** — `test_physics.py` pins `physics.py` to the frozen baselines.
- **[`addons/quant/`](addons/quant/)** — `seeding.py`, `oracle_baseline.py`, and `baselines.json` (frozen truth) for reproducibility and drift protection.
- **[`docs/`](docs/)** — OKF v0.1 knowledge bundle. Start at [`docs/index.md`](docs/index.md); module map in [`docs/architecture/index.md`](docs/architecture/index.md).
- **[`vendor/`](vendor/kaggle_environments/envs/orbit_wars)** — the Kaggle `orbit_wars` environment, vendored for offline self-play.

## Agent contract & skills

Behaviour and knowledge rules live in **[`AGENTS.md`](AGENTS.md)**, loaded per
tool via [`CLAUDE.md`](CLAUDE.md) (Claude Code / Cowork) and
[`GEMINI.md`](GEMINI.md) (Antigravity / Gemini CLI). Two always-on skills,
vendored under [`github-steals/`](github-steals/):

- **[ponytail](https://github.com/DietrichGebert/ponytail)** — lazy, stdlib-first, minimum code that works.
- **[caveman](https://github.com/JuliusBrussee/caveman)** — terse, token-compressed prose.

## Running

Run from the repo root (the agents are importable packages):

```bash
python -m tests.test_physics       # pin physics to the frozen baselines
python -m scripts.sim              # local self-play self-check (v1)
python scripts/check_okf.py docs   # OKF conformance of the docs bundle
```

Self-play arena (needs the vendored env on the import path):

```bash
PYTHONPATH=vendor python -m scripts.arena --a v2_1/agent.py --b v2_macro/agent.py --games 200
```

`--a` / `--b` take an agent path (`v1/agent.py`, `v2_1/agent.py`, `v2_macro/agent.py`) or a built-in
(`starter`, `random`); the default opponent is `starter`.

## Roadmap

Tracked in [`PROJECT_TRACKER.md`](PROJECT_TRACKER.md) §5. Current focus: beat the
`Producer Lite` opponent via macro/expansion fixes — travel-time-discounted ROI
(done, D-016) and earlier garrison release in `v2_1/strategy.py`.
