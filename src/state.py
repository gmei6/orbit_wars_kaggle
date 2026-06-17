"""Parse the Orbit Wars observation into typed objects.
ponytail: light dataclasses, no validation framework. `parse` is the only
integration seam — adjust it to the real Kaggle obs shape."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Planet:
    id: int; owner: int; x: float; y: float
    radius: float; ships: int; production: int
    incoming_enemy_ships: int = 0

    @property
    def is_in_danger(self) -> bool:
        return self.incoming_enemy_ships > 0


@dataclass
class Comet:
    id: int; owner: int; x: float; y: float; ships: int; production: int = 1


@dataclass
class Fleet:
    id: int; owner: int; x: float; y: float
    angle: float; source: int; ships: int


@dataclass
class State:
    step: int
    me: int
    planets: list
    initial_planets: dict
    comets_data: list
    fleets: list
    angular_velocity: float
    def mine(self): return [p for p in self.planets if p.owner == self.me]
    def targets(self): return [p for p in self.planets if p.owner != self.me]


def parse(obs: dict) -> State:
    """obs keys: step, player/my_id, planets, initial_planets, comets, fleets."""
    P = [Planet(*row[:7]) for row in obs.get("planets", [])]
    IP = {int(row[0]): Planet(*row[:7]) for row in obs.get("initial_planets", [])}
    F = [Fleet(*row[:7]) for row in obs.get("fleets", [])]
    return State(
        step=int(obs.get("step", 0)),
        me=int(obs.get("player", obs.get("my_id", 0))),
        planets=P,
        initial_planets=IP,
        comets_data=obs.get("comets", []),
        fleets=F,
        angular_velocity=float(obs.get("angular_velocity", 0.0))
    )


if __name__ == "__main__":
    s = parse({"turn": 1, "my_id": 0,
               "planets": [[0, 0, 10, 10, 1.0, 20, 3], [1, -1, 90, 90, 1.0, 5, 2]]})
    assert s.mine()[0].id == 0 and s.targets()[0].id == 1
    print("state self-check passed")
