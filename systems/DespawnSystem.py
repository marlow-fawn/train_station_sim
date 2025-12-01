from components import Despawn, Target, Position, Velocity
from util import dist


def despawn_system(world: 'World', condition):
    for entity in world.entities_with(Position, Despawn):
        despawn_entity = world.get_component(entity, Despawn)
        target_pos = world.get_component(despawn_entity.target.eid, Position)
        entity_pos = world.get_component(entity, Position)
        if dist(target_pos, entity_pos) < despawn_entity.target.radius:
            world.delete_entity(entity)