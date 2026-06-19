"""Macroeconomic forecasting and target valuation (Stage 4)."""
from __future__ import annotations

from .state import State
from .timeline import PlanetTimeline
from .reachability import reachable

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

    Time term is t_me: the earliest turn at which `side` can land a credible
    capturing force (from the reachability race) -- i.e. real turns-to-capture,
    size- and position-aware -- replacing the old raw-distance proxy.
        profit = production * (remaining_turns - t_me) - capture_cost
        roi    = profit / t_me        # ROI per turn of travel
    """
    timeline = timelines[P_id]

    cost = capture_cost(P_id, side, timelines)
    if cost == 0:
        cost = 1  # Avoid division by zero

    my_planets = [p for p in state.planets if p.owner == side]
    if not my_planets:
        return 0.0

    enemy_side = 1 if side == 2 else 2

    # Reachability race: t_me / t_enemy = earliest turn each side can land a
    # credible capturing force. t_me is our real turns-to-capture and is reused
    # below as the travel-time term (it is size- and position-aware).
    me_key = (P_id, side)
    if me_key not in reachable_cache:
        reachable_cache[me_key] = reachable(P_id, side, state, timelines, trajectory_cache)
    t_me, f_me = reachable_cache[me_key]

    enemy_key = (P_id, enemy_side)
    if enemy_key not in reachable_cache:
        reachable_cache[enemy_key] = reachable(P_id, enemy_side, state, timelines, trajectory_cache)
    t_enemy, f_enemy = reachable_cache[enemy_key]

    # Can't muster a credible force within the reachability horizon -> no value.
    if not t_me:
        return 0.0

    T = float(t_me)  # real turns-to-capture (size- and position-aware)
    R = 500 - state.step

    profit = timeline.production * max(0, R - T) - cost
    roi = profit / T
    if roi <= 0:
        return 0.0

    hold_multiplier = 1.0
    if t_enemy and (not t_me or t_enemy < t_me):
        # Enemy can reach it faster. Risky, but ceding guarantees a macro loss.
        hold_multiplier = 0.5
    elif t_me and (not t_enemy or t_me <= t_enemy):
        # We reach it faster or at the same time -> easy to hold.
        hold_multiplier = 1.5

    return float(roi * hold_multiplier)
