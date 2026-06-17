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


_GLOBAL_TRAJECTORY_CACHE = {}
_LAST_GAME_ID = None

def plan(state: State):
    """Return [[source_id, angle, ships], ...]. For each owned planet with a
    surplus, attack the best reachable target it can afford; skip any whose
    straight path crosses the sun.
    ponytail: transit estimated at full-garrison speed (sending more = faster =
    fewer defenders), so the estimate is conservative. Refine if it matters."""
    global _GLOBAL_TRAJECTORY_CACHE, _LAST_GAME_ID
    
    cmds = []
    comet_ids = {pid for group in state.comets_data for pid in group.get("planet_ids", [])}

    MAX_PRECOMPUTE = 150
    
    # Precompute regular planets globally per game
    # initial_planets dict values are Planet objects; we hash their id and positions
    game_id = hash(tuple(sorted((p.id, p.x, p.y) for p in state.initial_planets.values())))
    if game_id != _LAST_GAME_ID:
        _GLOBAL_TRAJECTORY_CACHE.clear()
        _LAST_GAME_ID = game_id
        for pid, p in state.initial_planets.items():
            # Precompute enough absolute turns (500 max turns + 150 lookahead)
            _GLOBAL_TRAJECTORY_CACHE[pid] = [
                planet_position(p.x, p.y, p.radius, state.angular_velocity, t)
                for t in range(650)
            ]

    trajectory_cache = {}
    for p in state.planets:
        if p.id in comet_ids:
            trajectory_cache[p.id] = [
                comet_position(p.id, state.comets_data, t)
                for t in range(1, MAX_PRECOMPUTE + 1)
            ]
        else:
            if p.id in _GLOBAL_TRAJECTORY_CACHE:
                trajectory_cache[p.id] = _GLOBAL_TRAJECTORY_CACHE[p.id][state.step + 1 : state.step + 1 + MAX_PRECOMPUTE]
            else:
                trajectory_cache[p.id] = [None] * MAX_PRECOMPUTE

    def get_pos(tid, t):
        if t < 1 or t > MAX_PRECOMPUTE:
            return None
        return trajectory_cache[tid][t - 1]

    # 1. Build target functions for our planets for defense prediction
    my_targets = {p.id: (lambda t, tid=p.id: get_pos(tid, t), p.radius) for p in state.mine()}

    # 2. Compute incoming enemy attacks and annotate planet state
    planet_by_id = {p.id: p for p in state.planets}
    for f in state.fleets:
        if f.owner != state.me:
            pred = predict_fleet_target(f.x, f.y, f.ships, f.angle, my_targets, max_turns=MAX_PRECOMPUTE)
            if pred is not None:
                tid, turns = pred
                if tid in planet_by_id:
                    planet_by_id[tid].incoming_enemy_ships += f.ships

    # 3. Available garrisons (deducting defense reserve)
    available = {}
    for src in state.mine():
        reserve = src.incoming_enemy_ships
        available[src.id] = max(0, src.ships - reserve)

    # 4. Multi-planet greedy attacks
    enemy_targets = {p.id: lambda t, tid=p.id: get_pos(tid, t) for p in state.targets()}

    def score_target(dst):
        prod = dst.production
        if dst.id in comet_ids:
            prod *= 2.5  # Heavy comet priority
        if state.step < 100 and dst.owner == -1:
            prod *= 1.5  # Early rush
        return prod

    target_list = sorted(state.targets(), key=score_target, reverse=True)

    for dst in target_list:
        tfunc = enemy_targets[dst.id]
        
        for delta_t in range(1, MAX_PRECOMPUTE + 1):
            pos = tfunc(delta_t)
            if pos is None:
                break
            tx, ty = pos
            
            need = required_to_capture(dst.ships, dst.production, delta_t)
            
            contributors = []
            accumulated = 0
            
            my_planets = sorted([p for p in state.mine() if available[p.id] > 0], 
                                key=lambda p: math.hypot(p.x - tx, p.y - ty))
                                
            for src in my_planets:
                garrison = available[src.id]
                speed = 1.0 + (6.0 - 1.0) * (math.log(max(1, garrison)) / math.log(1000.0)) ** 1.5 if garrison > 0 else 1.0
                speed = min(6.0, speed)
                
                dist = math.hypot(tx - src.x, ty - src.y)
                travel_dist = max(0.0, dist - dst.radius)
                tt = math.ceil(travel_dist / speed)
                
                if tt <= delta_t:
                    if not hits_sun(src.x, src.y, tx, ty):
                        delay = delta_t - tt
                        contributors.append((src, delay, tx, ty))
                        accumulated += garrison
                        if accumulated >= need:
                            break
                            
            if accumulated >= need:
                remaining_need = need
                for c_src, delay, c_tx, c_ty in contributors:
                    send = min(available[c_src.id], remaining_need)
                    if send > 0:
                        if delay == 0:
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
