"""Strategic decision making: what to attack, how to defend, when to launch."""
from __future__ import annotations
import math
from .state import State
from .targeting import get_trajectory_cache, MAX_PRECOMPUTE
from .physics import travel_time, lane_clear
from .timeline import build_timeline
from .reachability import reachable
from .economy import value

def decide(state: State):
    cmds = []
    
    # 1. Initialize Information Model
    trajectory_cache = get_trajectory_cache(state)
    timelines = build_timeline(state, trajectory_cache, max_turns=MAX_PRECOMPUTE)
    reachable_cache = {}
    
    # 2. Available garrisons (Freeing Frozen Capital)
    available = {}
    for src in state.mine():
        timeline = timelines[src.id]
        min_garrison = src.ships
        will_lose = False
        
        for T in range(1, MAX_PRECOMPUTE + 1):
            if timeline.owner_at(T) != state.me:
                will_lose = True
                break
            min_garrison = min(min_garrison, timeline.garrison_at(T))
            
        me_key = (src.id, state.me)
        enemy_side = 1 if state.me == 2 else 2
        enemy_key = (src.id, enemy_side)
        
        reachable_cache[me_key] = reachable(src.id, state.me, state, timelines, trajectory_cache)
        reachable_cache[enemy_key] = reachable(src.id, enemy_side, state, timelines, trajectory_cache)
        
        t_me, f_me = reachable_cache[me_key]
        t_enemy, f_enemy = reachable_cache[enemy_key]
        
        unholdable = t_enemy and (not t_me or t_enemy < t_me)
        
        if will_lose:
            if unholdable:
                available[src.id] = src.ships # Evacuate!
            else:
                available[src.id] = 0 # Hold tight, wait for reinforcements
        else:
            available[src.id] = max(0, min_garrison)

    # 3. Target Valuation & Ranking
    def score_target(dst):
        # Skip healthy owned planets
        if dst.owner == state.me and available.get(dst.id, 0) > 0:
            return -1.0 
        return value(dst.id, state.me, state, timelines, trajectory_cache, reachable_cache)

    target_list = sorted(state.planets, key=score_target, reverse=True)

    # 4. Synchronized Attacks
    for dst in target_list:
        if score_target(dst) <= 0:
            continue
            
        for delta_t in range(1, MAX_PRECOMPUTE + 1):
            pos = trajectory_cache[dst.id][delta_t - 1]
            if pos is None:
                break
            tx, ty = pos
            
            # Need to strictly beat the garrison at delta_t
            need = timelines[dst.id].garrison_at(delta_t) + 1
            
            contributors = []
            accumulated = 0
            
            # Sort owned planets by distance to future target position
            my_planets = sorted([p for p in state.mine() if available.get(p.id, 0) > 0 and p.id != dst.id], 
                                key=lambda p: math.hypot(p.x - tx, p.y - ty))
                                
            for src in my_planets:
                garrison = available[src.id]
                tt = travel_time(src.x, src.y, tx, ty, dst.radius, garrison)
                
                if tt <= delta_t:
                    if lane_clear(src.x, src.y, tx, ty):
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
