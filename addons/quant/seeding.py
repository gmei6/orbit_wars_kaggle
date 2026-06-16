"""Single source of randomness.

Import `seed_everything` (global state) or `get_rng` (explicit generator,
preferred). Never scatter `random.seed()` / `np.random.seed()` across the
codebase — that is what makes runs non-reproducible.
"""
from __future__ import annotations

import os
import random

DEFAULT_SEED = int(os.environ.get("PROJECT_SEED", "0"))


def seed_everything(seed: int = DEFAULT_SEED) -> int:
    """Seed every RNG we know about. Returns the seed used."""
    random.seed(seed)
    try:
        import numpy as np  # ponytail: numpy optional, no hard dep
        np.random.seed(seed)
    except ModuleNotFoundError:
        pass
    return seed


def get_rng(seed: int = DEFAULT_SEED):
    """Prefer an explicit generator over global state.

    Returns a numpy Generator when numpy is installed, else a stdlib
    random.Random. Both expose `.random()`.
    """
    try:
        import numpy as np
        return np.random.default_rng(seed)
    except ModuleNotFoundError:
        return random.Random(seed)  # ponytail: stdlib fallback


if __name__ == "__main__":
    # ponytail: one runnable check — same seed reproduces, different seed diverges.
    draw = lambda s: [get_rng(s).random() for _ in range(3)]
    assert draw(123) == draw(123), "same seed must reproduce"
    assert draw(123) != draw(124), "different seed must diverge"
    print("seeding self-check passed")
