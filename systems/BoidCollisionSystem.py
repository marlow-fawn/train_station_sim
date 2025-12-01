import math

from components import Position, Velocity, PlayerCollision



def boid_collision_system(world: 'World', dt: float):
    eids = world.entities_with(Position, Velocity, PlayerCollision)
    n = len(eids)
    avoidradius=1.5
    avoidfactor = 0.1
    # todo: make buckets

    for i in range(n):
        eid_a = eids[i]
        pos_a = world.get_component(eid_a, Position)
        vel_a = world.get_component(eid_a, Velocity)
        close_dx = 0.0
        close_dy = 0.0

        for j in range(i + 1, n):
            eid_b = eids[j]
            pos_b = world.get_component(eid_b, Position)

            dx = pos_b.x - pos_a.x
            dy = pos_b.y - pos_a.y
            dist = math.hypot(dx, dy)

            if dist == 0 or dist >= avoidradius:
                continue

            close_dx += pos_a.x - pos_b.x
            close_dy += pos_a.y - pos_b.y

        vel_a.vx += close_dx * avoidfactor
        vel_a.vy += close_dy * avoidfactor
