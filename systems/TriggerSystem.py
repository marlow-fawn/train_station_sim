from components import Timer, Trigger, Action
from world import World


def trigger_system(world: World, dt):
    for entity in world.entities_with(Trigger):
        trigger = world.get_component(entity, Trigger)
        if all(condition(world) for condition in trigger.conditions):
            [callback(world) for callback in trigger.callbacks]
            world.delete_entity(entity)
