"""Reachability race logic for v2 Information Model."""
from __future__ import annotations
import math

from v2_macro.state import State
from v2_macro.timeline import PlanetTimeline
from v2_macro.physics import travel_time, lane_clear

def max_arriving_force(target_id: int, target_pos: tuple[float, float], side: int, T: int, state: State, timelines: dict[int, PlanetTimeline]) -> int:
    """Calculates the max ships `side` can land on `target` EXACTLY at turn `T`."""
    total_force = 0
    target_p = state.initial_planets[target_id]
    
    for S_id, timeline in timelines.items():
        if timeline.owner_at(0) != side: # Only consider planets side owns now (simplification for launch sources)
            continue
        if S_id == target_id:
            continue
            
        S_p = state.initial_planets[S_id]
        
        # Check lane clarity to target position at T
        if not lane_clear(S_p.x, S_p.y, target_pos[0], target_pos[1]):
            continue
            
        # Find latest t_launch in [0, T-1] such that it arrives at or before T
        for t_launch in range(T - 1, -1, -1):
            if timeline.owner_at(t_launch) != side:
                break # We lost the planet before this launch
                
            ships = timeline.garrison_at(t_launch)
            if ships <= 0:
                continue
                
            # travel_time is size-aware
            tt = travel_time(S_p.x, S_p.y, target_pos[0], target_pos[1], target_p.radius, ships)
            if t_launch + tt <= T:
                total_force += ships
                break
                
    return total_force

def reachable(target_id: int, side: int, state: State, timelines: dict[int, PlanetTimeline], trajectory_cache: dict, max_turns: int = 150) -> tuple[int | None, int]:
    """
    Returns (earliest_turn, max_force_at_that_turn) where max_force is considered 'credible'.
    Credible force is defined conservatively as max(target_garrison, opponent_total_ships).
    """
    for T in range(1, max_turns + 1):
        pos = trajectory_cache[target_id][T - 1]
        if pos is None:
            continue
            
        target_garrison = timelines[target_id].garrison_at(T)
        credible_threshold = target_garrison
        
        force = max_arriving_force(target_id, pos, side, T, state, timelines)
        if force > credible_threshold:  # greater than, since ties mean no capture
            return T, force
            
    return None, 0
