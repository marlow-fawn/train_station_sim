import math

from components import Position, Velocity, Goal
from world import World

MAX_SPEED = 1.0      # units per second
MAX_ACCEL = 3.0      # how fast velocity can change toward goal per second

def goal_system(world: World, dt: float):
    for eid in world.entities_with(Position, Velocity, Goal):
        pos = world.get_component(eid, Position)
        vel = world.get_component(eid, Velocity)
        goal = world.get_component(eid, Goal)

        dx = goal.x - pos.x
        dy = goal.y - pos.y
        dist = math.hypot(dx, dy)

        # Already at goal → stop moving
        if dist < goal.radius or dist == 0:
            vel.vx = 0.0
            vel.vy = 0.0
            continue

        # Normalize direction toward goal
        dir_x = dx / dist
        dir_y = dy / dist

        # Desired velocity (pointing at goal, capped by MAX_SPEED)
        desired_vx = dir_x * MAX_SPEED
        desired_vy = dir_y * MAX_SPEED

        # Steer current velocity toward desired velocity, limited by MAX_ACCEL
        steer_x = desired_vx - vel.vx
        steer_y = desired_vy - vel.vy
        steer_mag = math.hypot(steer_x, steer_y)

        if steer_mag > 0:
            max_delta = MAX_ACCEL * dt
            if steer_mag > max_delta:
                scale = max_delta / steer_mag
                steer_x *= scale
                steer_y *= scale

            vel.vx += steer_x
            vel.vy += steer_y
