"""Single in-process game vs producer_lite — macro-diagnosis harness.

Runs ONE v2_1-vs-producer_lite game in-process (no arena process pool) so a
per-turn debug probe inside v2_1/strategy.decide() prints cleanly. Used in
Session 8 to show garrison release is NOT the binding constraint
(see LESSONS_LEARNED.md). Kept as the harness for the launch-gate pivot.

    PYTHONPATH=. python scripts/verify_garrison.py --seed 12345 --steps 120

The probe itself was reverted with lever A. To re-instrument, drop a block like
this at the end of decide(), gated so arena/visualize parity stays untouched:

    import os
    _DEBUG = os.environ.get("GARRISON_DEBUG")          # near module top
    ...
    if _DEBUG and (state.step < 25 or state.step % 10 == 0):
        owned = state.mine()
        print(f"[MACRO] step={state.step} planets={len(owned)} "
              f"owned={sum(p.ships for p in owned)} sent={sum(c[2] for c in cmds)} "
              f"leftover={sum(available.values())}", flush=True)

ponytail: throwaway harness; delete if the launch-gate work moves elsewhere.
"""
from __future__ import annotations
import argparse
import contextlib
import importlib
import importlib.util
import os
import sys


@contextlib.contextmanager
def _silence():
    """Mute the kaggle_environments import banner so probe lines stay clean."""
    devnull = open(os.devnull, "w")
    saved = (sys.stdout, sys.stderr)
    sys.stdout = sys.stderr = devnull
    try:
        yield
    finally:
        sys.stdout, sys.stderr = saved
        devnull.close()


def _load_producer():
    """Same path-load arena uses (register in sys.modules before exec_module)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "opponents", "producer_lite", "opp_producer.py")
    spec = importlib.util.spec_from_file_location("opp_producer", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.agent


def main():
    ap = argparse.ArgumentParser(description="One in-process game vs producer_lite.")
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--steps", type=int, default=120)
    args = ap.parse_args()

    os.environ.setdefault("GARRISON_DEBUG", "1")  # triggers the probe if one is present
    for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
               "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ.setdefault(_v, "1")

    v2_1 = importlib.import_module("v2_1.agent").act
    with _silence():
        from kaggle_environments import make
    producer = _load_producer()

    env = make("orbit_wars",
               configuration={"seed": args.seed, "episodeSteps": args.steps},
               debug=True)
    print(f"# v2_1 (seat 0) vs producer_lite (seat 1)  seed={args.seed} steps={args.steps}\n",
          flush=True)
    env.run([v2_1, producer])
    print("# done", flush=True)


if __name__ == "__main__":
    main()
