import time

from components import Timer
from world import World


def timer_system(world: World, dt):
    for entity in world.entities_with(Timer):
        timer = world.get_component(entity, Timer)

        current_time = time.time()
        if (current_time - timer.last) > timer.interval:
            [callback(world) for callback in timer.callbacks]
            timer.last = current_time
            timer.n -= 1

        if timer.n < 0:
            continue

        if timer.n == 0:
            world.delete_entity(entity)
