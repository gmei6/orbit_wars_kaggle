import pytest
from v2_macro.state import Planet, State
from v2_macro.timeline import PlanetTimeline, Event
from v2_macro.economy import production_integral, capture_cost, value

def test_production_integral():
    # Planet 0: mine, prod 2
    # Planet 1: enemy, prod 3, but flips to me at turn 5
    tl0 = PlanetTimeline(0, 1, 10, 2) # I am player 1
    tl1 = PlanetTimeline(1, 2, 5, 3)  # Enemy is player 2
    
    # Event: I capture planet 1 at turn 5 (garrison is 5 + 5*3 = 20, so 30 wins)
    tl1.events.append(Event(turn=5, fleets=[(1, 30)]))
    
    timelines = {0: tl0, 1: tl1}
    
    # Test production integral for 10 turns
    # Planet 0 produces 2 per turn * 10 = 20
    # Planet 1 produces 3 per turn * 6 (from turn 5 to 10) = 18
    # Total for me = 38
    total = production_integral(1, timelines, max_turns=10, current_turn=0)
    assert total == 38

def test_capture_cost():
    tl0 = PlanetTimeline(0, 2, 10, 2)
    # Neutral/Enemy planet 0. Garrison starts at 10, produces 2 per turn.
    # We check max garrison over next 10 turns. Should be 10 + 10*2 = 30
    timelines = {0: tl0}
    cost = capture_cost(0, 1, timelines)
    assert cost == 30

def test_value():
    p_target = Planet(id=0, owner=2, x=70, y=50, radius=5.0, ships=5, production=10)
    p_me = Planet(id=1, owner=1, x=90, y=50, radius=5.0, ships=100, production=1)
    
    state = State(step=0, me=1, planets=[p_target, p_me], 
                  initial_planets={0: p_target, 1: p_me}, 
                  comets_data=[], fleets=[], angular_velocity=0.0)
                  
    timelines = {
        0: PlanetTimeline(0, 2, 5, 10),
        1: PlanetTimeline(1, 1, 100, 1)
    }
    
    trajectory_cache = {
        0: [(70, 50) for _ in range(150)],
        1: [(90, 50) for _ in range(150)]
    }
    
    reachable_cache = {}
    
    # Target production = 10. Cost = 5 + 10*10 = 105.
    # ROI = 10 / 105 ~ 0.095
    # We can reach it (t_me > 0). Enemy is already there, but can they "reach" it with a credible force?
    # Enemy has no other planets. Opponent total ships = 100 (my ships). Target garrison = 5 + 10*T.
    # Let's just verify value returns a float and uses the cache.
    v = value(0, 1, state, timelines, trajectory_cache, reachable_cache)
    assert isinstance(v, float)
    assert len(reachable_cache) > 0
    assert (0, 1) in reachable_cache
    assert (0, 2) in reachable_cache
