"""Targeting mathematics: trajectory caching, defense calculation, attack window calculation. Pure math, no strategy."""
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
MAX_PRECOMPUTE = 150

def get_trajectory_cache(state: State) -> dict:
    global _GLOBAL_TRAJECTORY_CACHE, _LAST_GAME_ID
    
    comet_ids = {pid for group in state.comets_data for pid in group.get("planet_ids", [])}
    game_id = hash(tuple(sorted((p.id, p.x, p.y) for p in state.initial_planets.values())))
    
    if game_id != _LAST_GAME_ID:
        _GLOBAL_TRAJECTORY_CACHE.clear()
        _LAST_GAME_ID = game_id
        for pid, p in state.initial_planets.items():
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
    
    return trajectory_cache



def calculate_attack_options(state: State, target: Planet, delta_t: int, trajectory_cache: dict) -> tuple[int | None, tuple[float, float] | None]:
    """
    Given a target planet and a specific future turn (delta_t),
    returns the required ships to capture it, and its expected position.
    """
    if delta_t < 1 or delta_t > MAX_PRECOMPUTE:
        return None, None
        
    pos = trajectory_cache[target.id][delta_t - 1]
    if pos is None:
        return None, None
        
    tx, ty = pos
    need = required_to_capture(target.ships, target.production, delta_t)
    return need, (tx, ty)

