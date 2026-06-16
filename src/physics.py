"""Orbit Wars physics — the oracle. Constants and formulas are frozen here and
pinned to addons/quant/baselines.json. Bot code must not drift from these.
"""
from __future__ import annotations
import math

# Frozen game constants.
SUN = (50.0, 50.0)
SUN_RADIUS = 10.0
BOARD = 100.0
MAX_SPEED = 6.0
SPEED_REF_SHIPS = 1000.0   # ships at which max speed is reached
SPEED_EXP = 1.5
TOTAL_TURNS = 500
COMET_SPAWN_TURNS = (50, 150, 250, 350, 450)


def fleet_speed(ships: int) -> float:
    """Units/turn. 1 ship -> 1.0, ~1000 ships -> MAX_SPEED. Monotone in ships."""
    s = max(1, int(ships))
    frac = (math.log(s) / math.log(SPEED_REF_SHIPS)) ** SPEED_EXP
    return min(MAX_SPEED, 1.0 + (MAX_SPEED - 1.0) * frac)


def planet_radius(production: float) -> float:
    """radius = 1 + ln(production), production >= 1."""
    return 1.0 + math.log(max(1.0, production))


def transit_turns(distance: float, ships: int) -> float:
    """Turns for `ships` to cover `distance` in a straight line."""
    return distance / fleet_speed(ships)


def arrival_garrison(garrison: int, production: int, turns: float) -> float:
    """Defenders present on arrival — garrison grows during transit."""
    return garrison + production * turns


def seg_within(x0, y0, x1, y1, cx, cy, r) -> bool:
    """True if segment (x0,y0)->(x1,y1) comes within `r` of (cx,cy).
    Continuous (point-to-segment distance), per the collision rule."""
    dx, dy = x1 - x0, y1 - y0
    seg2 = dx * dx + dy * dy
    t = 0.0 if seg2 == 0.0 else max(0.0, min(1.0, ((cx - x0) * dx + (cy - y0) * dy) / seg2))
    return math.hypot(x0 + t * dx - cx, y0 + t * dy - cy) < r


def hits_sun(x0, y0, x1, y1, *, r: float = SUN_RADIUS) -> bool:
    return seg_within(x0, y0, x1, y1, SUN[0], SUN[1], r)


def required_to_capture(garrison: int, production: int, turns: float) -> int:
    """Ships needed to flip on arrival. Tie = mutual destruction (no flip), so
    strictly greater than the arrival garrison."""
    return int(math.floor(arrival_garrison(garrison, production, turns))) + 1


def resolve_combat(attackers: list[int], garrison: int) -> tuple[bool, int]:
    """Resolve simultaneous arrivals at one planet.
    Largest attacker fights second-largest, the difference survives; survivors
    fight the garrison; attackers>garrison flips ownership, tie = no flip.
    Returns (captured, ships_left).
    ponytail: models the documented top-two reduction; >2 multi-owner stacks
    collapse to (max - second). Refine if the real engine proves finer order.
    """
    a = sorted(attackers, reverse=True)
    force = a[0] - a[1] if len(a) >= 2 else (a[0] if a else 0)
    if force > garrison:
        return True, force - garrison
    return False, garrison - force


def planet_position(cx: float, cy: float, radius: float, start_angle: float, angular_velocity: float, turn: int) -> tuple[float, float]:
    """Dynamically compute orbital (x, y). Flat angular velocity assumed until Kaggle formula is known."""
    current_angle = start_angle + angular_velocity * turn
    return (cx + radius * math.cos(current_angle), cy + radius * math.sin(current_angle))


def comet_position(start_x: float, start_y: float, vx: float, vy: float, turn: int, spawn_turn: int) -> tuple[float, float]:
    """Parametric comet position. Placeholder until Kaggle orbital formula is provided."""
    dt = max(0, turn - spawn_turn)
    return (start_x + vx * dt, start_y + vy * dt)


def intercept_time(src_x: float, src_y: float, target_pos_func, fleet_speed: float, max_turns: int = TOTAL_TURNS) -> int | None:
    """Find earliest turn t where a fleet can reach the target's position at t.
    target_pos_func(t) returns (x, y) of the target at relative turn t.
    ponytail: Iterative solver is O(T) max 500 steps. Faster and more robust than 
    analytic root-finding for arbitrary curves."""
    for t in range(1, max_turns + 1):
        tx, ty = target_pos_func(t)
        dist = math.hypot(tx - src_x, ty - src_y)
        if dist <= fleet_speed * t:
            return t
    return None


def intercept_angle(src_x: float, src_y: float, tx: float, ty: float) -> float:
    """Launch angle to intercept point."""
    return math.atan2(ty - src_y, tx - src_x)


if __name__ == "__main__":
    assert fleet_speed(1) == 1.0
    assert abs(fleet_speed(1000) - MAX_SPEED) < 1e-12
    assert fleet_speed(10) < fleet_speed(100) < fleet_speed(1000)
    assert planet_radius(1) == 1.0
    assert hits_sun(0, 50, 100, 50)        # straight through the sun
    assert not hits_sun(0, 0, 0, 100)      # left edge, clear
    assert required_to_capture(10, 3, 5) == 26   # arrival 25 -> need 26
    cap, left = resolve_combat([30, 10], 15)     # 20 vs 15 -> capture, 5 left
    assert cap and left == 5
    print("physics self-check passed")
