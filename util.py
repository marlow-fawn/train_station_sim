import math

from components import Position


def dist(a: Position, b: Position):
    dx = b.x - a.x
    dy = b.y - a.y
    return math.hypot(dx, dy)
