import math

from components import Position, Velocity, PlayerCollision

AGENT_RADIUS = 0.3  # tweak to taste

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

            min_dist = 2 * AGENT_RADIUS
            if dist == 0 or dist >= min_dist:
                continue

            # 1) separate the two agents so they no longer overlap
            overlap = min_dist - dist
            nx = dx / dist
            ny = dy / dist

            # push each agent half the overlap distance along the normal
            pos_a.x -= nx * overlap / 2
            pos_a.y -= ny * overlap / 2
            pos_b.x += nx * overlap / 2
            pos_b.y += ny * overlap / 2

            # 2) simple velocity response: push velocities apart along normal
            # (this is not "physically correct", just keeps them from clumping)
            rel_vx = vel_b.vx - vel_a.vx
            rel_vy = vel_b.vy - vel_a.vy
            rel_speed = rel_vx * nx + rel_vy * ny

            if rel_speed < 0:  # only if moving toward each other
                impulse = -rel_speed
                vel_a.vx -= nx * impulse / 2
                vel_a.vy -= ny * impulse / 2
                vel_b.vx += nx * impulse / 2
                vel_b.vy += ny * impulse / 2