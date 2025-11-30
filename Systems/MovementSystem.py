from components import Position, Velocity


def movement_system(world: 'World', dt: float) -> None:
    for eid in world.entities_with(Position, Velocity):
        pos = world.get_component(eid, Position)
        vel = world.get_component(eid, Velocity)
        pos.x += vel.vx * dt
        pos.y += vel.vy * dt

        # Todo: Cap speed
        # Todo: Add goals, increase vel to goal to cap
