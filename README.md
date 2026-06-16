# Orbit Wars Kaggle Agent

Agent implementation for the Orbit Wars Kaggle competition. Uses greedy targeting (`v0`), strict oracle/physics separation, and Open Knowledge Format (OKF) documentation.

## Architecture

- **`src/`**: Kaggle entry point, simulation engine, and game logic.
  - `agent.py`: Entry point; wires parsing to policy.
  - `physics.py`: The oracle. Frozen game math (speed, sun collision, capture logic). No strategy.
  - `targeting.py` & `strategy.py`: `v0` greedy target selection and fleet sizing against arrival garrisons.
  - `state.py`: Raw observation parser.
  - `sim.py`: Local seeded self-play engine.
- **`docs/`**: OKF v0.1 knowledge bundle. Read `docs/architecture/index.md` for the module map.
- **`tests/` & `addons/quant/`**: Tests and frozen baselines (`baselines.json`) to prevent physics/oracle drift.

## Environment & Skills

This repo uses two behavior skills imported via `AGENTS.md` / `GEMINI.md`:
- **[ponytail](https://github.com/DietrichGebert/ponytail)** — lazy, stdlib-first, minimum code that works.
- **[caveman](https://github.com/JuliusBrussee/caveman)** — terse, token-compressed prose.

## Testing

Run tests to ensure physics matches Kaggle baselines:
```bash
python -m unittest tests/test_physics.py
```

Run local self-play:
```bash
python src/sim.py
```

## Next Steps (`v1`)

- Comet interception for production boosts.
- Defense / garrison retention against incoming fleets.
- Multi-planet cooperative attacks.
