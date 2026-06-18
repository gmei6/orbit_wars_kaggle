"""Strategic decision making: what to attack, how to defend, when to launch."""
from __future__ import annotations
import math
from .state import State
from .targeting import get_trajectory_cache, MAX_PRECOMPUTE
from .physics import travel_time, lane_clear
from .timeline import build_timeline
from .reachability import reachable
from .economy import value

RESERVATIONS = {}

def decide(state: State):
    global RESERVATIONS
    if state.step == 0:
        RESERVATIONS.clear()
        
    cmds = []
    
    # 1. Initialize Information Model
    trajectory_cache = get_trajectory_cache(state)
    timelines = build_timeline(state, trajectory_cache)
    
    from .timeline import Event
    for src_id, tasks in RESERVATIONS.items():
        for task in tasks:
            if len(task) == 5:
                abs_arrival = task[4]
                dst_id = task[3]
                ships = task[2]
                rel_arrival = abs_arrival - state.step
                if rel_arrival > 0 and dst_id in timelines:
                    tl = timelines[dst_id]
                    found = False
                    for e in tl.events:
                        if e.turn == rel_arrival:
                            e.fleets.append((state.me, ships))
                            found = True
                            break
                    if not found:
                        tl.events.append(Event(turn=rel_arrival, fleets=[(state.me, ships)]))
                        tl.events.sort(key=lambda x: x.turn)
                        
    reachable_cache = {}
    unholdable_set = set()
    will_lose_cache = {}
    
    # 2. Process Reservations and Available Garrisons
    for src_id, tasks in list(RESERVATIONS.items()):
        remaining_tasks = []
        for task in tasks:
            turn_to_launch, angle, ships = task[0], task[1], task[2]
            if state.step >= turn_to_launch:
                p = state.initial_planets.get(src_id)
                if p and p.owner == state.me:
                    actual_ships = min(ships, p.ships)
                    if actual_ships > 0:
                        cmds.append([src_id, angle, actual_ships])
            else:
                remaining_tasks.append(task)
        if remaining_tasks:
            RESERVATIONS[src_id] = remaining_tasks
        else:
            del RESERVATIONS[src_id]

    available = {}
    for src in state.mine():
        timeline = timelines[src.id]
        min_garrison = src.ships
        will_lose = False
        
        # Fix: Limit freeze lookahead to prevent paralyzing early economy
        for T in range(1, min(MAX_PRECOMPUTE, 30) + 1):
            if timeline.owner_at(T) != state.me:
                will_lose = True
                break
            min_garrison = min(min_garrison, timeline.garrison_at(T))
            
        will_lose_cache[src.id] = will_lose
            
        me_key = (src.id, state.me)
        enemy_side = 1 if state.me == 2 else 2
        enemy_key = (src.id, enemy_side)
        
        reachable_cache[me_key] = reachable(src.id, state.me, state, timelines, trajectory_cache)
        reachable_cache[enemy_key] = reachable(src.id, enemy_side, state, timelines, trajectory_cache)
        
        t_me, f_me = reachable_cache[me_key]
        t_enemy, f_enemy = reachable_cache[enemy_key]
        
        unholdable = t_enemy and (not t_me or t_enemy < t_me)
        if unholdable:
            unholdable_set.add(src.id)
            
        if will_lose:
            if unholdable:
                available[src.id] = src.ships # Evacuate!
            else:
                available[src.id] = 0 # Hold tight, wait for reinforcements
        else:
            available[src.id] = max(0, min_garrison)
            
        # Deduct reserved ships from available
        reserved_ships = sum(task[2] for task in RESERVATIONS.get(src.id, []))
        available[src.id] = max(0, available[src.id] - reserved_ships)

    # 3. Target Valuation & Ranking
    def score_target(dst):
        # Skip planets we already own or are guaranteed to own
        if timelines[dst.id].owner_at(MAX_PRECOMPUTE) == state.me:
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
                                
            remaining_need = need
            for src in my_planets:
                send_potential = min(available[src.id], remaining_need)
                if send_potential <= 0:
                    continue
                    
                tt = travel_time(src.x, src.y, tx, ty, dst.radius, send_potential)
                
                if tt <= delta_t:
                    if lane_clear(src.x, src.y, tx, ty):
                        delay = delta_t - tt
                        contributors.append((src, delay, tx, ty, send_potential))
                        accumulated += send_potential
                        remaining_need -= send_potential
                        if accumulated >= need:
                            break
                            
            if accumulated >= need:
                for c_src, delay, c_tx, c_ty, send in contributors:
                    if send > 0:
                        angle = math.atan2(c_ty - c_src.y, c_tx - c_src.x)
                        with open("/tmp/v2_macro_debug.log", "a") as f:
                            f.write(f"Turn {state.step}: Planet {c_src.id} -> Target {dst.id} (send {send}, delay {delay}, need {need})\n")
                        if delay == 0:
                            cmds.append([c_src.id, angle, send])
                        else:
                            if c_src.id not in RESERVATIONS:
                                RESERVATIONS[c_src.id] = []
                            RESERVATIONS[c_src.id].append((state.step + delay, angle, send, dst.id, state.step + delta_t))
                        available[c_src.id] -= send
                break

    # 5. Evacuate unholdable planets
    for src in state.mine():
        if will_lose_cache.get(src.id, False) and src.id in unholdable_set:
            if available.get(src.id, 0) > 0:
                safe_planets = [p for p in state.mine() if not will_lose_cache.get(p.id, False)]
                if safe_planets:
                    dst = min(safe_planets, key=lambda p: math.hypot(p.x - src.x, p.y - src.y))
                else:
                    other_planets = [p for p in state.planets if p.id != src.id]
                    if other_planets:
                        dst = max(other_planets, key=lambda p: math.hypot(p.x - src.x, p.y - src.y))
                    else:
                        continue
                tt = travel_time(src.x, src.y, dst.x, dst.y, dst.radius, available[src.id])
                pos = trajectory_cache[dst.id][min(tt, MAX_PRECOMPUTE) - 1]
                if pos:
                    tx, ty = pos
                else:
                    tx, ty = dst.x, dst.y
                cmds.append([src.id, math.atan2(ty - src.y, tx - src.x), available[src.id]])
                available[src.id] = 0

    return cmds
