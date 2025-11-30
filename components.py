from dataclasses import dataclass

@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0


@dataclass
class Velocity:
    vx: float = 0.0
    vy: float = 0.0

    @property
    def speed(self) -> float:
        return (self.vx ** 2 + self.vy ** 2) ** 0.5


@dataclass
class Role:
    name: str = "na"
from dataclasses import dataclass

@dataclass
class Goal:
    x: float
    y: float
    radius: float = 0.3  # how close counts as "arrived"

@dataclass
class Target:
    eid: 'EID'
    radius: float = 0.3

@dataclass
class BoundaryCollision:
    pass

@dataclass
class PlayerCollision:
    pass
