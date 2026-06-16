"""Pick targets and size fleets. Greedy, distance- and production-aware."""
from __future__ import annotations
import math
from .physics import (
    transit_turns, required_to_capture, hits_sun, 
    comet_position, planet_position, intercept_time,
    predict_fleet_target
)
from .state import State, Planet


def angle_to(src: Planet, dst: Planet) -> float:
    return math.atan2(dst.y - src.y, dst.x - src.x)


def plan(state: State):
    """Return [[source_id, angle, ships], ...]. For each owned planet with a
    surplus, attack the best reachable target it can afford; skip any whose
    straight path crosses the sun.
    ponytail: transit estimated at full-garrison speed (sending more = faster =
    fewer defenders), so the estimate is conservative. Refine if it matters."""
    cmds = []
    comet_ids = {pid for group in state.comets_data for pid in group.get("planet_ids", [])}

    MAX_PRECOMPUTE = 150
    trajectory_cache = {}
    for p in state.planets:
        trajectory_cache[p.id] = []
        if p.id in comet_ids:
            for t in range(1, MAX_PRECOMPUTE + 1):
                trajectory_cache[p.id].append(comet_position(p.id, state.comets_data, t))
        else:
            initial = state.initial_planets.get(p.id)
            if initial:
                for t in range(1, MAX_PRECOMPUTE + 1):
                    trajectory_cache[p.id].append(planet_position(initial.x, initial.y, p.radius, state.angular_velocity, state.step + t))
            else:
                trajectory_cache[p.id] = [None] * MAX_PRECOMPUTE

    def get_pos(tid, t):
        if t < 1 or t > MAX_PRECOMPUTE:
            return None
        return trajectory_cache[tid][t - 1]

    # 1. Build target functions for our planets for defense prediction
    my_targets = {p.id: (lambda t, tid=p.id: get_pos(tid, t), p.radius) for p in state.mine()}

    # 2. Compute incoming enemy attacks
    incoming_attacks = {p.id: 0 for p in state.mine()}
    for f in state.fleets:
        if f.owner != state.me:
            pred = predict_fleet_target(f.x, f.y, f.ships, f.angle, my_targets, max_turns=MAX_PRECOMPUTE)
            if pred is not None:
                tid, turns = pred
                incoming_attacks[tid] += f.ships

    # 3. Available garrisons (deducting defense reserve)
    available = {}
    for src in state.mine():
        reserve = incoming_attacks[src.id]
        available[src.id] = max(0, src.ships - reserve)

    # 4. Multi-planet greedy attacks
    enemy_targets = {p.id: lambda t, tid=p.id: get_pos(tid, t) for p in state.targets()}

    target_list = sorted(state.targets(), key=lambda p: p.production, reverse=True)

    for dst in target_list:
        tfunc = enemy_targets[dst.id]
        
        my_planets = sorted([p for p in state.mine() if available[p.id] > 0], 
                            key=lambda p: math.hypot(p.x - dst.x, p.y - dst.y))
        
        accumulated = 0
        contributors = []
        max_turns = 0
        
        for src in my_planets:
            garrison = available[src.id]
            speed = 1.0 + (6.0 - 1.0) * (math.log(max(1, garrison)) / math.log(1000.0)) ** 1.5 if garrison > 0 else 1.0
            speed = min(6.0, speed)
            turns = intercept_time(src.x, src.y, tfunc, speed, max_turns=MAX_PRECOMPUTE)
            if turns is None:
                continue
            
            tx, ty = tfunc(turns)
            if hits_sun(src.x, src.y, tx, ty):
                continue
                
            max_turns = max(max_turns, turns)
            accumulated += garrison
            contributors.append((src, turns, tx, ty))
            
            need = required_to_capture(dst.ships, dst.production, max_turns)
            if accumulated >= need:
                remaining_need = need
                for c_src, c_turns, c_tx, c_ty in contributors:
                    send = min(available[c_src.id], remaining_need)
                    if send > 0:
                        cmds.append([c_src.id, math.atan2(c_ty - c_src.y, c_tx - c_src.x), send])
                        available[c_src.id] -= send
                        remaining_need -= send
                break

    return cmds


if __name__ == "__main__":
    from .state import parse
    s = parse({"turn": 1, "my_id": 0,
               "planets": [[0, 0, 10, 10, 1.0, 50, 3],
                           [1, -1, 20, 20, 1.0, 5, 4]],
               "initial_planets": [[0, 0, 10, 10, 1.0, 50, 3],
                                   [1, -1, 20, 20, 1.0, 5, 4]]})
    cmds = plan(s)
    assert cmds and cmds[0][0] == 0
    print("targeting self-check passed")
