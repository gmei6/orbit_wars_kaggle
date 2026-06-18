"""Timeline forecast layer for Stage 1. 
Replaces naive defense calculation with a fold over chronologically ordered arrival events.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .state import State
from .physics import arrival_garrison, resolve_combat, predict_fleet_target

@dataclass
class Event:
    turn: int
    fleets: list[tuple[int, int]] = field(default_factory=list) # list of (owner, ships)

class PlanetTimeline:
    """A deterministic projection of a planet's garrison and owner over time."""
    def __init__(self, planet_id: int, owner_now: int, garrison_now: int, production: int):
        self.planet_id = planet_id
        self.owner_now = owner_now
        self.garrison_now = garrison_now
        self.production = production
        self.events: list[Event] = []

    def owner_at(self, t: int) -> int:
        """Forecast the owner of the planet at relative turn t."""
        owner, _ = self._fold_until(t)
        return owner

    def garrison_at(self, t: int) -> int:
        """Forecast the garrison of the planet at relative turn t."""
        _, garrison = self._fold_until(t)
        return garrison

    def _fold_until(self, t: int) -> tuple[int, int]:
        """Folds events chronologically up to turn t."""
        owner = self.owner_now
        garrison = self.garrison_now
        last_turn = 0
        
        for event in self.events:
            if event.turn > t:
                break
            # Accrue production up to this event's turn. Neutral (owner < 0) does not produce.
            turns_elapsed = event.turn - last_turn
            current_production = self.production if owner >= 0 else 0
            garrison = int(arrival_garrison(garrison, current_production, turns_elapsed))
            
            # Resolve combat
            owner, garrison = resolve_combat(owner, garrison, event.fleets)
            last_turn = event.turn
            
        # Accrue any remaining production up to turn t
        if t > last_turn:
            turns_elapsed = t - last_turn
            current_production = self.production if owner >= 0 else 0
            garrison = int(arrival_garrison(garrison, current_production, turns_elapsed))
            
        return owner, garrison

def build_timeline(state: State, trajectory_cache: dict, max_turns: int = 150) -> dict[int, PlanetTimeline]:
    """Builds per-planet timelines from state.fleets using the intercept layer."""
    timelines = {}
    for p in state.planets:
        timelines[p.id] = PlanetTimeline(p.id, p.owner, p.ships, p.production)
        
    def get_pos(tid, t):
        if t < 1 or t > max_turns:
            return None
        return trajectory_cache[tid][t - 1]

    # Predict target and arrival turn for all fleets
    target_funcs = {p.id: (lambda t, tid=p.id: get_pos(tid, t), p.radius) for p in state.planets}
    events_by_planet = {p.id: {} for p in state.planets}
    
    for f in state.fleets:
        pred = predict_fleet_target(f.x, f.y, f.ships, f.angle, target_funcs, max_turns=max_turns)
        if pred is not None:
            tid, turn = pred
            if tid in events_by_planet:
                if turn not in events_by_planet[tid]:
                    events_by_planet[tid][turn] = []
                events_by_planet[tid][turn].append((f.owner, f.ships))
                
    # Sort events by turn and append to timelines
    for tid, t_dict in events_by_planet.items():
        for turn in sorted(t_dict.keys()):
            timelines[tid].events.append(Event(turn=turn, fleets=t_dict[turn]))
            
    return timelines
