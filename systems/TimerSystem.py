import dataclasses
import time
from random import random

from components import Spawner, Position, Velocity, BoundaryCollision, Role, Timer
from datetime import datetime


def timer_system(world: 'World', dt):
    for entity in world.entities_with(Timer):
        timer = world.get_component(entity, Timer)

        current_time = time.time()
        if (current_time - timer.last) > timer.interval:
            timer.callback(world)
            timer.last = current_time
            timer.n -= 1

        if timer.n == 0:
            print("Timer done")
            world.delete_entity(entity)
