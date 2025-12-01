import math

from components import Position, Velocity, BoundaryCollision

AGENT_RADIUS = 0.3  # tweak to taste


def boundary_collision_system(world: 'World', dt: float):
    width, height = world.size

    # --- 1. wall collisions ---
    for eid in world.entities_with(Position, Velocity, BoundaryCollision):
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
