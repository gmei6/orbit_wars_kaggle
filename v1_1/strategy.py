"""Strategic decision making: what to attack, how to defend, when to launch."""
from __future__ import annotations
import math
from .state import State
from .targeting import (
    get_trajectory_cache, 
    calculate_defense_needs, 
    calculate_attack_options,
    get_travel_time,
    is_path_clear,
    MAX_PRECOMPUTE
)

def decide(state: State):
    cmds = []
    
    # 1. Get math oracles
    trajectory_cache = get_trajectory_cache(state)
    incoming_enemies = calculate_defense_needs(state, trajectory_cache)
    
    comet_ids = {pid for group in state.comets_data for pid in group.get("planet_ids", [])}
        
    # 2. Available garrisons (deducting defense reserve)
    available = {}
    for src in state.mine():
        reserve = incoming_enemies.get(src.id, 0)
        available[src.id] = max(0, src.ships - reserve)

    # 3. Target Scoring
    def score_target(dst):
        prod = dst.production
        if dst.id in comet_ids:
            prod *= 2.5  # Heavy comet priority
        if state.step < 100 and dst.owner == -1:
            prod *= 1.5  # Early rush
        return prod

    target_list = sorted(state.targets(), key=score_target, reverse=True)

    # 4. Multi-planet greedy synchronized attacks
    for dst in target_list:
        for delta_t in range(1, MAX_PRECOMPUTE + 1):
            need, pos = calculate_attack_options(state, dst, delta_t, trajectory_cache)
            if need is None or pos is None:
                break
            tx, ty = pos
            
            contributors = []
            accumulated = 0
            
            # Sort owned planets by distance to the future target position
            my_planets = sorted([p for p in state.mine() if available[p.id] > 0], 
                                key=lambda p: math.hypot(p.x - tx, p.y - ty))
                                
            for src in my_planets:
                garrison = available[src.id]
                tt = get_travel_time(src, tx, ty, dst.radius, garrison)
                
                if tt <= delta_t:
                    if is_path_clear(src, tx, ty):
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
