"""Pin src.physics to the frozen baselines. Run: python -m tests.test_physics"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "addons", "quant"))
from src import physics as ph
import oracle_baseline as ob


def main():
    ob.check("fleet_speed_1", ph.fleet_speed(1))
    ob.check("fleet_speed_500", ph.fleet_speed(500))
    ob.check("fleet_speed_1000", ph.fleet_speed(1000))
    ob.check("planet_radius_1", ph.planet_radius(1))
    ob.check("planet_radius_5", ph.planet_radius(5))
    ob.check("arrival_garrison_g10_p3_t5", ph.arrival_garrison(10, 3, 5))
    assert ph.hits_sun(0, 50, 100, 50)
    assert not ph.hits_sun(0, 0, 0, 100)
    import math
    px, py = ph.planet_position(0.0, 0.0, 10.0, 0.0, math.pi/2, 1)
    assert math.isclose(px, 0.0, abs_tol=1e-9)
    assert math.isclose(py, 10.0, abs_tol=1e-9)
    assert ph.intercept_time(0.0, 0.0, lambda t: (100.0, 0.0), 5.0) == 20
    assert ph.intercept_time(0.0, 0.0, lambda t: (10.0 + t, 0.0), 2.0) == 10

    print("test_physics passed (physics matches frozen baselines)")


if __name__ == "__main__":
    main()
