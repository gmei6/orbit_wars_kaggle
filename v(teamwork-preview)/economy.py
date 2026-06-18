"""Macroeconomic forecasting and target valuation (Stage 4)."""
from __future__ import annotations

from v1_1.state import State
from v1_1.timeline import PlanetTimeline
from v1_1.reachability import reachable

def production_integral(side: int, timelines: dict[int, PlanetTimeline], max_turns: int = 500, current_turn: int = 0) -> int:
    """
    Computes the total ships 'side' will produce over the remaining game turns,
    assuming no new launches (baseline projection).
    """
    total_ships = 0
    # Remaining turns to evaluate
    for T in range(1, max_turns - current_turn + 1):
        for timeline in timelines.values():
            if timeline.owner_at(T) == side:
                total_ships += timeline.production
    return total_ships

def capture_cost(P_id: int, side: int, timelines: dict[int, PlanetTimeline]) -> int:
    """
    Estimates the absolute minimum cost to take the planet. 
    Looks ahead 10 turns to find the peak garrison size to overcome.
    """
    # If we already own it, cost is 0
    if timelines[P_id].owner_at(0) == side:
        return 0
    return max(timelines[P_id].garrison_at(T) for T in range(1, 11))

def value(P_id: int, side: int, state: State, timelines: dict[int, PlanetTimeline], trajectory_cache: dict, reachable_cache: dict) -> float:
    """
    Evaluates the Return on Investment (ROI) for capturing planet P.
    Base formula: value(P) ~= production(P) * hold_probability(P) - capture_cost(P)
    We use ROI (production / cost) as recommended.
    """
    timeline = timelines[P_id]
    
    cost = capture_cost(P_id, side, timelines)
    if cost == 0:
        cost = 1 # Avoid division by zero
        
    roi = timeline.production / float(cost)
    
    enemy_side = 1 if side == 2 else 2
    
    # Check reachable_cache for (P_id, player)
    me_key = (P_id, side)
    if me_key not in reachable_cache:
        reachable_cache[me_key] = reachable(P_id, side, state, timelines, trajectory_cache)
    t_me, f_me = reachable_cache[me_key]
    
    enemy_key = (P_id, enemy_side)
    if enemy_key not in reachable_cache:
        reachable_cache[enemy_key] = reachable(P_id, enemy_side, state, timelines, trajectory_cache)
    t_enemy, f_enemy = reachable_cache[enemy_key]
    
    hold_multiplier = 1.0
    if t_enemy and (not t_me or t_enemy < t_me):
        # Enemy can reach it faster -> hard to hold
        hold_multiplier = 0.1
    elif t_me and (not t_enemy or t_me <= t_enemy):
        # We reach it faster or at same time -> easy to hold
        hold_multiplier = 1.5
        
    return roi * hold_multiplier
