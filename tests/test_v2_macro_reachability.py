import pytest
from v2_macro.state import Planet, State
from v2_macro.timeline import PlanetTimeline
from v2_macro.reachability import max_arriving_force, reachable

def test_max_arriving_force():
    p_target = Planet(id=0, owner=2, x=70, y=50, radius=5.0, ships=5, production=2)
    p_src1 = Planet(id=1, owner=1, x=90, y=50, radius=5.0, ships=10, production=1)
    
    state = State(step=0, me=1, planets=[p_target, p_src1], 
                  initial_planets={0: p_target, 1: p_src1}, 
                  comets_data=[], fleets=[], angular_velocity=0.0)
                  
    timelines = {
        0: PlanetTimeline(0, 2, 5, 2),
        1: PlanetTimeline(1, 1, 10, 1)
    }
    
    # Target is at (70, 50). S1 is at (90, 50).
    # S1 ships at t=0 is 10.
    force = max_arriving_force(0, (70, 50), 1, 10, state, timelines)
    # We expect some force to arrive
    assert force > 10

def test_reachable():
    p_target = Planet(id=0, owner=2, x=70, y=50, radius=5.0, ships=5, production=2)
    p_src1 = Planet(id=1, owner=1, x=90, y=50, radius=5.0, ships=100, production=1)
    
    state = State(step=0, me=1, planets=[p_target, p_src1], 
                  initial_planets={0: p_target, 1: p_src1}, 
                  comets_data=[], fleets=[], angular_velocity=0.0)
                  
    timelines = {
        0: PlanetTimeline(0, 2, 5, 2),
        1: PlanetTimeline(1, 1, 100, 1)
    }
    
    trajectory_cache = {
        0: [(70, 50) for _ in range(150)],
        1: [(90, 50) for _ in range(150)]
    }
    
    earliest_t, max_f = reachable(0, 1, state, timelines, trajectory_cache, max_turns=20)
    assert earliest_t is not None
    assert earliest_t > 0
    assert max_f >= 100
