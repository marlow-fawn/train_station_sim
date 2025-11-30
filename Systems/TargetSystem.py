import math

from components import Position, Velocity, Goal, Target

MAX_SPEED = 20.0      # units per second
MAX_ACCEL = 5.0      # how fast velocity can change toward goal per second

def target_system(world: 'World', dt: float):
    for eid in world.entities_with(Position, Velocity, Target):
        pos = world.get_component(eid, Position)
        vel = world.get_component(eid, Velocity)
        target = world.get_component(eid, Target)

        target_pos = world.get_component(target.eid, Position)
        dx = target_pos.x - pos.x
        dy = target_pos.y - pos.y
        dist = math.hypot(dx, dy)

        # Already at goal → stop moving
        if dist < target.radius or dist == 0:
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
