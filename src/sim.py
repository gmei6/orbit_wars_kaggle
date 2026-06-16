"""Minimal local Orbit Wars simulator: iterate the rules fast and reproducibly.
Not the official engine — enough to self-play and regression-test a policy.
Seeded via addons.quant.seeding when importable.
ponytail: orbiting planets and comets omitted in v0 (static map); add when a
policy depends on them."""
from __future__ import annotations
import math, os, sys
from .physics import fleet_speed, hits_sun, seg_within, resolve_combat

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "addons", "quant"))
    from seeding import get_rng
except Exception:  # ponytail: stdlib fallback, still deterministic per seed
    import random
    def get_rng(seed=0): return random.Random(seed)


def _start(rng):
    """Two mirrored home planets + two neutrals, all clear of the sun."""
    planets = [[0, 0, 15.0, 15.0, 1.0, 30, 3],
               [1, 1, 85.0, 85.0, 1.0, 30, 3],
               [2, -1, 15.0, 85.0, 1.0, 10, 2],
               [3, -1, 85.0, 15.0, 1.0, 10, 2]]
    return {"turn": 0, "comets": [], "fleets": [],
            "planets": [list(p) for p in planets],
            "initial_planets": [list(p) for p in planets]}



def _obs(world, me):
    o = dict(world); o["my_id"] = me; return o


def step(world, cmds_by_player):
    P, F = world["planets"], world["fleets"]
    byid = {p[0]: p for p in P}
    nid = max([f[0] for f in F], default=-1) + 1
    for owner, cmds in cmds_by_player.items():           # launches
        for src_id, ang, n in cmds:
            p = byid.get(src_id); n = int(n)
            if not p or p[1] != owner or n <= 0 or n > p[5]:
                continue
            p[5] -= n
            r = p[4] + 1e-6
            F.append([nid, owner, p[2] + r * math.cos(ang), p[3] + r * math.sin(ang),
                      ang, src_id, n]); nid += 1
    for p in P:                                          # production
        if p[1] != -1:
            p[5] += int(p[6])
    arrivals, survivors = {}, []                         # move + sun + arrivals
    for f in F:
        spd = fleet_speed(f[6])
        x0, y0 = f[2], f[3]
        x1, y1 = x0 + spd * math.cos(f[4]), y0 + spd * math.sin(f[4])
        if hits_sun(x0, y0, x1, y1):
            continue
        hit = next((p for p in P if seg_within(x0, y0, x1, y1, p[2], p[3], p[4])), None)
        if hit is None:
            f[2], f[3] = x1, y1
            if 0 <= x1 <= 100 and 0 <= y1 <= 100:
                survivors.append(f)
        else:
            arrivals.setdefault(hit[0], []).append((f[1], f[6]))
    world["fleets"] = survivors
    for pid, arr in arrivals.items():                    # resolve combat
        p = byid[pid]
        for owner, n in arr:
            if owner == p[1]:
                p[5] += n
        enemy = {}
        for owner, n in arr:
            if owner != p[1]:
                enemy[owner] = enemy.get(owner, 0) + n
        if not enemy:
            continue
        ranked = sorted(enemy.items(), key=lambda kv: kv[1], reverse=True)
        top_owner, top = ranked[0]
        second = ranked[1][1] if len(ranked) > 1 else 0
        cap, left = resolve_combat([top, second] if second else [top], p[5])
        p[1], p[5] = (top_owner, left) if cap else (p[1], left)
    world["turn"] += 1
    return world


def run(policy_a, policy_b, turns=200, seed=0):
    world = _start(get_rng(seed))
    pol = {0: policy_a, 1: policy_b}
    for _ in range(turns):
        step(world, {pid: (pol[pid](_obs(world, pid)) or []) for pid in (0, 1)})
    counts = {0: 0, 1: 0}
    for p in world["planets"]:
        if p[1] in counts: counts[p[1]] += p[5]
    for f in world["fleets"]:
        if f[1] in counts: counts[f[1]] += f[6]
    winner = -1 if counts[0] == counts[1] else max(counts, key=counts.get)
    return {"counts": counts, "winner": winner, "turns": turns}


if __name__ == "__main__":
    from .agent import act
    idle = lambda obs: []
    r1 = run(act, idle, turns=120, seed=7)
    r2 = run(act, idle, turns=120, seed=7)
    assert r1 == r2, "sim must be reproducible for a fixed seed"
    assert r1["counts"][0] >= 30, "active policy should not bleed ships to an idle foe"
    print("sim self-check passed:", r1)
