import math

from components import Position, Velocity, PlayerCollision


def player_collision_system(world: 'World', dt: float):
    eids = world.entities_with(Position, Velocity, PlayerCollision)
    n = len(eids)

    for i in range(n):
        eid_a = eids[i]
        pos_a = world.get_component(eid_a, Position)
        vel_a = world.get_component(eid_a, Velocity)

        for j in range(i + 1, n):
            eid_b = eids[j]
            pos_b = world.get_component(eid_b, Position)
            vel_b = world.get_component(eid_b, Velocity)

            dx = pos_b.x - pos_a.x
            dy = pos_b.y - pos_a.y
            dist = math.hypot(dx, dy)

            min_dist = 1
            if dist == 0 or dist >= min_dist:
                continue

            # 1) separate the two agents so they no longer overlap
            overlap = min_dist - dist
            nx = dx / dist
            ny = dy / dist

            k = 0.5  # tweak to taste
            force = k * (min_dist - dist) ** 2
            vel_a.vx -= nx * force
            vel_a.vy -= ny * force
            # vel_b.vx -= nx * force
            # vel_b.vy -= ny * force

            pos_a.x -= nx * overlap / 2
            pos_a.y -= ny * overlap / 2
            # pos_b.x += nx * overlap / 2
            # pos_b.y += ny * overlap / 2
