"""Parse the Orbit Wars observation into typed objects.
ponytail: light dataclasses, no validation framework. `parse` is the only
integration seam — adjust it to the real Kaggle obs shape."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Planet:
    id: int; owner: int; x: float; y: float
    radius: float; ships: int; production: int


@dataclass
class Comet:
    id: int; owner: int; x: float; y: float; ships: int; production: int = 1


@dataclass
class Fleet:
    id: int; owner: int; x: float; y: float
    angle: float; source: int; ships: int


@dataclass
class State:
    turn: int
    me: int
    planets: list
    comets: list
    fleets: list
    def mine(self): return [p for p in self.planets if p.owner == self.me]
    def targets(self): return [p for p in self.planets if p.owner != self.me]


def parse(obs: dict) -> State:
    """obs keys: turn, my_id, planets[], comets[], fleets[] (raw arrays).
    Planet row [id,owner,x,y,radius,ships,production];
    Fleet row [id,owner,x,y,angle,source_planet_id,ships]."""
    P = [Planet(*row[:7]) for row in obs.get("planets", [])]
    C = [Comet(int(r[0]), int(r[1]), r[2], r[3], int(r[-1])) for r in obs.get("comets", [])]
    F = [Fleet(*row[:7]) for row in obs.get("fleets", [])]
    return State(int(obs.get("turn", 0)), int(obs.get("my_id", 0)), P, C, F)


if __name__ == "__main__":
    s = parse({"turn": 1, "my_id": 0,
               "planets": [[0, 0, 10, 10, 1.0, 20, 3], [1, -1, 90, 90, 1.0, 5, 2]]})
    assert s.mine()[0].id == 0 and s.targets()[0].id == 1
    print("state self-check passed")
