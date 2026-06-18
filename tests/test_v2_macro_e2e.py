import pytest
import math
import os
import sys

# Setup root path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from v2_macro.agent import act
except ImportError:
    from v1_1.agent import act

try:
    from v2_macro.state import parse
except ImportError:
    from v1_1.state import parse

try:
    from v2_macro.physics import fleet_speed
except ImportError:
    from v1_1.physics import fleet_speed

from scripts.sim import run

def make_obs(planets, my_id=1, step=0, fleets=None, comets=None, angular_velocity=0.0):
    if fleets is None:
        fleets = []
    if comets is None:
        comets = []
    return {
        "step": step,
        "player": my_id,
        "planets": planets,
        "initial_planets": planets,
        "fleets": fleets,
        "comets": comets,
        "angular_velocity": angular_velocity
    }

def make_incoming_fleet(fleet_id, owner, target_x, target_y, ships, arrival_turn):
    v = fleet_speed(ships)
    fx = target_x
    fy = target_y - v * arrival_turn
    fangle = math.pi / 2
    return [fleet_id, owner, fx, fy, fangle, -1, ships]

# ==========================================
# TIER 1: Feature Coverage (25 tests)
# ==========================================

# --- Capital Unfreezing (5 tests) ---

def test_tier1_capital_unfreezing_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][0] == 0
    assert cmds[0][2] == 11

def test_tier1_capital_unfreezing_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 25, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 25, 5)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier1_capital_unfreezing_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    fleets = [
        make_incoming_fleet(0, 2, 15.0, 15.0, 25, 5),
        make_incoming_fleet(1, 1, 15.0, 15.0, 20, 4)
    ]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][0] == 0

def test_tier1_capital_unfreezing_c4():
    planets_high = [
        [0, 1, 15.0, 15.0, 1.0, 30, 10],
        [2, -1, 15.0, 45.0, 1.0, 24, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 15, 5)]
    obs_high = make_obs(planets_high, fleets=fleets)
    cmds_high = act(obs_high)
    assert len(cmds_high) > 0

    planets_low = [
        [0, 1, 15.0, 15.0, 1.0, 30, 1],
        [2, -1, 15.0, 45.0, 1.0, 24, 2]
    ]
    obs_low = make_obs(planets_low, fleets=fleets)
    cmds_low = act(obs_low)
    assert len(cmds_low) == 0

def test_tier1_capital_unfreezing_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 20.0, 1.0, 30, 3],
        [2, -1, 15.0, 85.0, 1.0, 5, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 40, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    launched_from_0 = [c for c in cmds if c[0] == 0]
    assert len(launched_from_0) == 0

# --- Reachability Race (5 tests) ---

def test_tier1_reachability_race_c1():
    planets = [
        [0, 1, 30.0, 20.0, 1.0, 30, 3],
        [1, 2, 80.0, 20.0, 1.0, 30, 3],
        [2, -1, 50.0, 20.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][0] == 0


def test_tier1_reachability_race_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 85.0, 85.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier1_reachability_race_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 2, 85.0, 85.0, 1.0, 30, 3],
        [2, -1, 15.0, 35.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0

def test_tier1_reachability_race_c5():
    v10 = fleet_speed(10)
    v100 = fleet_speed(100)
    assert v100 > v10

# --- ROI Valuation (5 tests) ---

def test_tier1_roi_valuation_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 10],
        [3, -1, 45.0, 15.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert abs(cmds[0][1] - math.pi/2) < 0.1

def test_tier1_roi_valuation_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 5, 5],
        [3, -1, 45.0, 15.0, 1.0, 20, 5]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert abs(cmds[0][1] - math.pi/2) < 0.1

def test_tier1_roi_valuation_c3():
    planets = [
        [0, 1, 30.0, 50.0, 1.0, 30, 3],
        [1, 2, 70.0, 50.0, 1.0, 30, 3],
        [2, -1, 40.0, 50.0, 1.0, 10, 5],
        [3, -1, 60.0, 50.0, 1.0, 10, 7]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert abs(cmds[0][1]) < 0.1

def test_tier1_roi_valuation_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 45.0, 1.0, 10, 3]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier1_roi_valuation_c5():
    planets = [[0, 1, 15.0, 15.0, 1.0, 30, 3]]
    obs = make_obs(planets, step=490)
    s = parse(obs)
    assert s.step == 490

# --- Synchronized Arrivals (5 tests) ---

def test_tier1_synchronized_arrivals_c1():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 1
    assert cmds[0][0] == 1
    assert abs(cmds[0][1]) < 0.1

def test_tier1_synchronized_arrivals_c2():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 1
    assert cmds[0][2] == 6

def test_tier1_synchronized_arrivals_c3():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 25, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier1_synchronized_arrivals_c4():
    planets = [
        [0, 1, 50.0, 65.0, 1.0, 10, 1],
        [1, 1, 40.0, 40.0, 1.0, 10, 1],
        [2, -1, 60.0, 60.0, 1.0, 15, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier1_synchronized_arrivals_c5():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, 1, 20.0, 20.0, 1.0, 10, 1],
        [3, -1, 50.0, 20.0, 1.0, 25, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0

# --- Evacuating Unholdable Planets (5 tests) ---

def test_tier1_evacuating_unholdable_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3],
        [2, -1, 15.0, 30.0, 1.0, 10, 1]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    launched_from_0 = [c for c in cmds if c[0] == 0]
    assert len(launched_from_0) > 0

def test_tier1_evacuating_unholdable_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3],
        [2, -1, 80.0, 80.0, 1.0, 100, 1]
    ]
    fleets = [
        make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2),
        make_incoming_fleet(1, 1, 15.0, 15.0, 100, 1)
    ]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    launched_from_0 = [c for c in cmds if c[0] == 0]
    assert len(launched_from_0) == 0

def test_tier1_evacuating_unholdable_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    # P0 is unholdable, but P1 is safe. P0 should evacuate to P1.
    assert len(cmds) == 1
    assert cmds[0][0] == 0

def test_tier1_evacuating_unholdable_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3],
        [2, -1, 15.0, 45.0, 1.0, 5, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][0] == 0

def test_tier1_evacuating_unholdable_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3],
        [2, -1, 15.0, 45.0, 1.0, 29, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][2] == 30


# ==========================================
# TIER 2: Boundary & Corner Cases (25 tests)
# ==========================================

# --- Capital Unfreezing (5 tests) ---

def test_tier2_capital_unfreezing_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 0, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier2_capital_unfreezing_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 150)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_capital_unfreezing_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    fleets = [
        make_incoming_fleet(0, 1, 15.0, 15.0, 10, 2),
        make_incoming_fleet(1, 1, 15.0, 15.0, 20, 3)
    ]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_capital_unfreezing_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    fleets = [
        make_incoming_fleet(0, 2, 15.0, 15.0, 20, 3),
        make_incoming_fleet(1, 1, 15.0, 15.0, 20, 3)
    ]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_capital_unfreezing_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 1, 3],
        [2, -1, 15.0, 45.0, 1.0, 0, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][2] == 1

# --- Reachability Race (5 tests) ---

def test_tier2_reachability_race_c1():
    planets = [
        [0, 1, 30.0, 20.0, 1.0, 30, 3],
        [1, 2, 70.0, 20.0, 1.0, 30, 3],
        [2, -1, 50.0, 20.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_reachability_race_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 95.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_reachability_race_c3():
    planets = [
        [0, 1, 0.0, 0.0, 1.0, 1, 3],
        [2, -1, 100.0, 100.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_reachability_race_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 60.0, 45.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_reachability_race_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2]
    ]
    comets = [{"planet_ids": [2], "paths": [[[15.0, 45.0]]], "path_index": 0}]
    obs = make_obs(planets, comets=comets)
    cmds = act(obs)
    assert isinstance(cmds, list)

# --- ROI Valuation (5 tests) ---

def test_tier2_roi_valuation_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 0]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_roi_valuation_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10000, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) == 0

def test_tier2_roi_valuation_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 95.0, 95.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets, step=498)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_roi_valuation_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 0, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0

def test_tier2_roi_valuation_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2],
        [3, -1, 45.0, 15.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

# --- Synchronized Arrivals (5 tests) ---

def test_tier2_synchronized_arrivals_c1():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 5, 1],
        [2, -1, 50.0, 20.0, 1.0, 14, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_synchronized_arrivals_c2():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 9, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_synchronized_arrivals_c3():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 35.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_synchronized_arrivals_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, -1, 15.0, 45.0, 1.0, 10, 2],
        [2, -1, 45.0, 15.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_synchronized_arrivals_c5():
    planets = [
        [0, 1, 10.0, 10.0, 1.0, 30, 3],
        [1, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 90.0, 90.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

# --- Evacuating Unholdable Planets (5 tests) ---

def test_tier2_evacuating_unholdable_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 1)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_evacuating_unholdable_c2():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 150)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_evacuating_unholdable_c3():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 0, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_evacuating_unholdable_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 85.0, 85.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier2_evacuating_unholdable_c5():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [
        make_incoming_fleet(0, 2, 15.0, 15.0, 50, 2),
        make_incoming_fleet(1, 2, 15.0, 15.0, 60, 3)
    ]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)


# ==========================================
# TIER 3: Pairwise Combinations (10 tests)
# ==========================================

def test_tier3_pairwise_c1():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert cmds[0][2] == 30

def test_tier3_pairwise_c2():
    planets = [
        [0, 1, 30.0, 50.0, 1.0, 30, 3],
        [1, 2, 70.0, 50.0, 1.0, 30, 3],
        [2, -1, 40.0, 50.0, 1.0, 10, 2],
        [3, -1, 60.0, 50.0, 1.0, 10, 10]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert abs(cmds[0][1]) < 0.1

def test_tier3_pairwise_c3():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 2]
    ]
    fleets = [make_incoming_fleet(0, 2, 40.0, 20.0, 5, 5)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0

def test_tier3_pairwise_c4():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [2, 1, 55.0, 15.0, 1.0, 30, 10],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert len(cmds) > 0
    # Can evacuate to P1 (+y, ~1.57) or P2 (+x, 0.0)
    angle = cmds[0][1]
    assert abs(angle - 0.0) < 0.1 or abs(angle - 1.5707) < 0.1

def test_tier3_pairwise_c5():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 2],
        [3, 2, 80.0, 20.0, 1.0, 30, 3]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier3_pairwise_c6():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 10],
        [3, -1, 45.0, 15.0, 1.0, 10, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0
    assert abs(cmds[0][1] - math.pi/2) < 0.1

def test_tier3_pairwise_c7():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3],
        [2, -1, 80.0, 80.0, 1.0, 10, 1]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier3_pairwise_c8():
    planets = [
        [0, 1, 40.0, 20.0, 1.0, 10, 1],
        [1, 1, 30.0, 20.0, 1.0, 10, 1],
        [2, -1, 50.0, 20.0, 1.0, 15, 10],
        [3, -1, 30.0, 30.0, 1.0, 15, 2]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert len(cmds) > 0

def test_tier3_pairwise_c9():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [2, -1, 15.0, 45.0, 1.0, 10, 2],
        [3, 2, 80.0, 80.0, 1.0, 30, 3]
    ]
    obs = make_obs(planets)
    cmds = act(obs)
    assert isinstance(cmds, list)

def test_tier3_pairwise_c10():
    planets = [
        [0, 1, 15.0, 15.0, 1.0, 30, 3],
        [1, 1, 15.0, 55.0, 1.0, 30, 3],
        [3, 2, 15.0, 25.0, 1.0, 200, 3]
    ]
    fleets = [make_incoming_fleet(0, 2, 15.0, 15.0, 100, 2)]
    obs = make_obs(planets, fleets=fleets)
    cmds = act(obs)
    assert isinstance(cmds, list)


# ==========================================
# TIER 4: Realistic Scenarios (5 tests)
# ==========================================

def test_tier4_simulator_play_c1():
    idle = lambda obs: []
    r = run(act, idle, turns=30, seed=1)
    assert isinstance(r, dict)
    assert "winner" in r
    assert "counts" in r

def test_tier4_simulator_play_c2():
    idle = lambda obs: []
    r = run(act, idle, turns=30, seed=2)
    assert isinstance(r, dict)

def test_tier4_simulator_play_c3():
    idle = lambda obs: []
    r = run(act, idle, turns=30, seed=3)
    assert isinstance(r, dict)

def test_tier4_simulator_play_c4():
    idle = lambda obs: []
    r = run(act, idle, turns=30, seed=4)
    assert isinstance(r, dict)

def test_tier4_simulator_play_c5():
    idle = lambda obs: []
    r = run(act, idle, turns=30, seed=5)
    assert isinstance(r, dict)
