"""Per-turn policy. Thin over targeting for v0.
ponytail: strategy == targeting until policies actually diverge; split then."""
from __future__ import annotations
from .state import State
from .targeting import plan


def decide(state: State):
    """Return launch commands [[source_id, angle, ships], ...]."""
    return plan(state)
