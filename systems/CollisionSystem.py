import math

from world import World
from components import Position, Velocity

AGENT_RADIUS = 0.3  # tweak to taste
# FIXME: No generic collision component any more
def collision_system(world: World, dt: float):
    width, height = world.size

    # --- 1. wall collisions ---
    for eid in world.entities_with(Position, Velocity):
        pos = world.get_component(eid, Position)
        vel = world.get_component(eid, Velocity)

        # Left/right walls
        if pos.x < AGENT_RADIUS:
            pos.x = AGENT_RADIUS
            vel.vx = abs(vel.vx)  # bounce right
        elif pos.x > width - AGENT_RADIUS:
            pos.x = width - AGENT_RADIUS
            vel.vx = -abs(vel.vx)  # bounce left

        # Bottom/top walls
        if pos.y < AGENT_RADIUS:
            pos.y = AGENT_RADIUS
            vel.vy = abs(vel.vy)  # bounce up
        elif pos.y > height - AGENT_RADIUS:
            pos.y = height - AGENT_RADIUS
            vel.vy = -abs(vel.vy)  # bounce down

    # --- 2. agent–agent collisions (naive O(N^2)) ---
    eids = world.entities_with(Position, Velocity)
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