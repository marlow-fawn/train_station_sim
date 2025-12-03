from dataclasses import dataclass
from typing import Callable, Tuple, Any


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
    radius: float = 1.0


@dataclass
class BoundaryCollision:
    pass


@dataclass
class PlayerCollision:
    pass


@dataclass
class Despawn:
    target: Target


@dataclass
class Color:
    color: Tuple[int, int, int] = (255, 255, 255)


@dataclass
class Action:
    func: Callable[['World', ...], None]
    args: tuple[Any, ...]
    kwargs: dict = None

    def __call__(self, world: 'World') -> None:
        self.kwargs = self.kwargs or {}
        self.func(world, *self.args, **self.kwargs)

    def __init__(self, func: Callable[..., None], *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


@dataclass
class Condition:
    func: Callable[['World', ...], bool]
    args: tuple[Any, ...]
    kwargs: dict = None

    def __call__(self, world: 'World') -> bool:
        self.kwargs = self.kwargs or {}
        return self.func(world, *self.args, **self.kwargs)

    def __init__(self, func: Callable[..., bool], *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


@dataclass
class Timer:
    interval: float  # How long to wait between spawns
    n: int  # How many entities to spawn
    last: float
    callbacks: list[Action]


@dataclass
class Trigger:
    conditions: list[Condition]
    callbacks: list[Action]
