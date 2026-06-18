import pytest
from v2_macro.state import Planet, State, Fleet
from v2_macro.timeline import PlanetTimeline, Event, build_timeline

def test_planet_timeline_folding():
    # Planet: owner 1, garrison 10, production 2
    timeline = PlanetTimeline(planet_id=0, owner_now=1, garrison_now=10, production=2)
    
    # Event 1: Enemy (owner 2) arrives at turn 5 with 15 ships
    timeline.events.append(Event(turn=5, fleets=[(2, 15)]))
    
    # Event 2: My ally (owner 1) arrives at turn 10 with 5 ships
    timeline.events.append(Event(turn=10, fleets=[(1, 5)]))
    
    # Assert garrison at turn 4: 10 + 4*2 = 18
    assert timeline.garrison_at(4) == 18
    assert timeline.owner_at(4) == 1
    
    # Assert at turn 5: garrison is 10 + 5*2 = 20. Then -15 enemy = 5. Owner is still 1.
    assert timeline.garrison_at(5) == 5
    assert timeline.owner_at(5) == 1
    
    # Assert at turn 9: garrison from turn 5 is 5. 4 turns passed. 5 + 4*2 = 13.
    assert timeline.garrison_at(9) == 13
    assert timeline.owner_at(9) == 1
    
    # Assert at turn 10: 5 turns passed since turn 5. 5 + 5*2 = 15. Then +5 ally = 20.
    assert timeline.garrison_at(10) == 20
    assert timeline.owner_at(10) == 1
    
def test_planet_timeline_flip():
    # Neutral planet (owner -1), garrison 10, production 3
    # Note: neutral planets do not produce. 
    timeline = PlanetTimeline(planet_id=1, owner_now=-1, garrison_now=10, production=3)
    
    # Event at turn 5: Player 1 attacks with 15 ships
    timeline.events.append(Event(turn=5, fleets=[(1, 15)]))
    
    # At turn 4: neutral doesn't produce, so garrison remains 10
    assert timeline.garrison_at(4) == 10
    assert timeline.owner_at(4) == -1
    
    # At turn 5: garrison 10. 15 attack. 15 > 10. 15 - 10 = 5. Owner flips to 1.
    assert timeline.garrison_at(5) == 5
    assert timeline.owner_at(5) == 1
    
    # At turn 8: owner 1 produces for 3 turns (turns 5 to 8). 5 + 3*3 = 14.
    assert timeline.garrison_at(8) == 14
    assert timeline.owner_at(8) == 1

def test_build_timeline():
    # Mock state and trajectory cache to verify build logic
    p1 = Planet(id=0, owner=1, x=50, y=50, radius=5.0, ships=10, production=2)
    f1 = Fleet(id=0, owner=2, x=60, y=50, angle=3.14159, source=1, ships=20)
    
    state = State(step=0, me=1, planets=[p1], initial_planets={}, comets_data=[], fleets=[f1], angular_velocity=0.0)
    
    # Mock trajectory cache for p1 (stationary at 50,50)
    trajectory_cache = {0: [(50, 50) for _ in range(150)]}
    
    timelines = build_timeline(state, trajectory_cache)
    
    assert 0 in timelines
    tl = timelines[0]
    
    # distance = 10, target_radius = 5, dist to cover = 5
    # speed of 20 ships = fleet_speed(20). Let's see if there is an event.
    assert len(tl.events) == 1
    event = tl.events[0]
    assert event.fleets[0] == (2, 20)
