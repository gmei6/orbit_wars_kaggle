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
    cmds = []
    for src in state.mine():
        garrison = src.ships
        best = None
        for dst in state.targets():
            if hits_sun(src.x, src.y, dst.x, dst.y):
                continue
            dist = math.hypot(dst.x - src.x, dst.y - src.y)
            need = required_to_capture(dst.ships, dst.production,
                                       transit_turns(dist, max(1, garrison)))
            if need <= garrison:
                score = dst.production / (dist + 1e-9)
                if best is None or score > best[0]:
                    best = (score, dst, need)
        if best:
            _, dst, need = best
            cmds.append([src.id, angle_to(src, dst), need])
    return cmds


if __name__ == "__main__":
    from .state import parse
    s = parse({"turn": 1, "my_id": 0,
               "planets": [[0, 0, 10, 10, 1.0, 50, 3],
                           [1, -1, 20, 20, 1.0, 5, 4]]})
    cmds = plan(s)
    assert cmds and cmds[0][0] == 0
    print("targeting self-check passed")
