"""Pick targets and size fleets. Greedy, distance- and production-aware."""
from __future__ import annotations
import math
from .physics import transit_turns, required_to_capture, hits_sun
from .state import State, Planet


def angle_to(src: Planet, dst: Planet) -> float:
    return math.atan2(dst.y - src.y, dst.x - src.x)


def plan(state: State):
    """Return [[source_id, angle, ships], ...]. For each owned planet with a
    surplus, attack the best reachable target it can afford; skip any whose
    straight path crosses the sun.
    ponytail: transit estimated at full-garrison speed (sending more = faster =
    fewer defenders), so the estimate is conservative. Refine if it matters."""
    comet_ids = {pid for group in state.comets_data for pid in group.get("planet_ids", [])}

    for src in state.mine():
        garrison = src.ships
        speed = 1.0 + (6.0 - 1.0) * (math.log(max(1, garrison)) / math.log(1000.0)) ** 1.5 if garrison > 0 else 1.0
        speed = min(6.0, speed)
        best = None
        for dst in state.targets():
            if dst.id in comet_ids:
                def target_func(t):
                    return comet_position(dst.id, state.comets_data, t)
            else:
                initial = state.initial_planets[dst.id]
                def target_func(t):
                    return planet_position(initial.x, initial.y, dst.radius, state.angular_velocity, state.step + t)

            turns = intercept_time(src.x, src.y, target_func, speed)
            if turns is None:
                continue
            
            tx, ty = target_func(turns)
            if hits_sun(src.x, src.y, tx, ty):
                continue
            
            dist = math.hypot(tx - src.x, ty - src.y)
            need = required_to_capture(dst.ships, dst.production, turns)
            if need <= garrison:
                score = dst.production / (dist + 1e-9)
                if best is None or score > best[0]:
                    best = (score, dst, need, tx, ty)
        if best:
            _, dst, need, tx, ty = best
            cmds.append([src.id, math.atan2(ty - src.y, tx - src.x), need])
    return cmds


if __name__ == "__main__":
    from .state import parse
    s = parse({"turn": 1, "my_id": 0,
               "planets": [[0, 0, 10, 10, 1.0, 50, 3],
                           [1, -1, 20, 20, 1.0, 5, 4]]})
    cmds = plan(s)
    assert cmds and cmds[0][0] == 0
    print("targeting self-check passed")
