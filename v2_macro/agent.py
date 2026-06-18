"""Kaggle entry point — the env calls this each turn.
ponytail: adapt the signature/obs access to the real environment; the parse
seam lives in state.parse."""
from __future__ import annotations
from v2_macro.state import parse
from v2_macro.strategy import decide


def act(obs, config=None):
    return decide(parse(obs))
