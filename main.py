import time
import pygame

from callbacks import spawner_callback, send_train_callback
from recognition.ClusteringSystem import clustering_system
from recognition.RecognitionSystem import recognition_system
from systems.BoundaryCollisionSystem import boundary_collision_system
from systems.DespawnSystem import despawn_system
from systems.PlayerCollisionSystem import player_collision_system
from systems.TimerSystem import timer_system
from components import *
from systems.MovementSystem import movement_system
from systems.TargetSystem import target_system
from systems.PygameRenderSystem import PygameRenderSystem
from systems.TriggerSystem import trigger_system
from util import create_waypoint
from world import World


def init_systems(world: World):
    world.add_system(timer_system)
    world.add_system(trigger_system)
    world.add_system(despawn_system)

    world.add_system(target_system)  # Update velocities
    world.add_system(movement_system)  # Update positions

    world.add_system(boundary_collision_system)
    world.add_system(player_collision_system)

    world.add_system(clustering_system)
    # Render last
    world.add_system(init_pygame(world))


def init_pygame(world: World) -> PygameRenderSystem:
    pygame.init()
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Station Sim")
    return PygameRenderSystem(screen, screen_size, world.size)


if __name__ == '__main__':
    world = World((20, 20))
    init_systems(world)
    clock = pygame.time.Clock()
    running = True

    # (world.build_entity()
    #  .has(Timer(0.1, -1, time.time(), [Action(spawner_callback,
    #                                           start=[station_1, station_2],
    #                                           end=[train_1, train_2],
    #                                           role="commuter")])))
    #
    (world.build_entity()
     .has(Timer(1, 1, time.time(), [Action(send_train_callback, role="train")])))

    while running:
        dt = clock.tick(60) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.step(dt)

    pygame.quit()
