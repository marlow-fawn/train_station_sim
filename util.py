import math
from random import random

from components import Position, Role
from world import World


def dist(a: Position, b: Position):
    dx = b.x - a.x
    dy = b.y - a.y
    return math.hypot(dx, dy)


def create_waypoint(world: World, x=None, y=None):
    position = Position(x if x is not None else (random() * world.size[0]),
                        y if y is not None else (random() * world.size[1]))

    return (world.build_entity()
            .has(position)
            .has(Role("target"))
            ).eid
