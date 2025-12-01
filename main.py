import random
import time
from typing import Dict, TypeVar, Type, List, Callable
import pygame

from callbacks import spawner_callback
from systems.BoundaryCollisionSystem import boundary_collision_system
from systems.DespawnSystem import despawn_system
from systems.PlayerCollisionSystem import player_collision_system
from systems.TimerSystem import timer_system
from components import *
from systems.MovementSystem import movement_system
from systems.TargetSystem import target_system
from systems.PygameRenderSystem import PygameRenderSystem

C = TypeVar("C")
SystemFn = Callable[['World', float], None]
EID = int


class EntityBuilder:
    def __init__(self, world: 'World', eid: EID):
        self.world = world
        self.eid = eid

    def has(self, component: C) -> 'EntityBuilder':
        self.world.add_component(self.eid, component)
        return self


class World:
    def __init__(self, size=(10, 10)):
        self._entities: List[EID] = []
        self._components: Dict[Type[C], Dict[EID, C]] = {}
        self._next_id = 0
        self._systems: List[SystemFn] = []
        self.size = size

    def create_entity(self) -> EID:
        eid = self._next_id
        self._entities.append(eid)
        self._next_id += 1
        return eid

    def build_entity(self) -> EntityBuilder:
        return EntityBuilder(self, self.create_entity())

    def delete_entity(self, eid: EID):
        self._entities.remove(eid)
        # Maybe replace this if I make a "get_components_for_entity" thing?
        [ctype.pop(eid, None) for ctype in self._components.values()]

    def add_component(self, eid: EID, component: C):
        entities = self._components.setdefault(type(component), {})
        entities[eid] = component

    def get_component(self, eid, ctype: Type[C]) -> C:
        try:
            return self._components[ctype][eid]
        except KeyError as e:
            raise KeyError(f"Entity {eid} does not have component {ctype.__name__}") from e

    def add_system(self, system: SystemFn) -> 'World':
        self._systems.append(system)
        return self

    def step(self, dt: float) -> None:
        for system in self._systems:
            system(self, dt)

    def entities_with(self, *ctypes: Type[C]) -> List[EID]:
        if not ctypes:
            return self._entities
        stores = [self._components.get(t, {}) for t in ctypes]
        if not all(stores):
            return []
        common = set(stores[0].keys())
        for s in stores[1:]:
            common &= set(s.keys())
        return list(common)

    def has_component(self, eid: int, ctype: Type[C]) -> bool:
        return eid in self.entities_with(ctype)


def create_waypoint(world: World, x=None, y=None):
    position = Position(x if x is not None else (random.random() * world.size[0]),
                        y if y is not None else (random.random() * world.size[1]))

    return (world.build_entity()
            .has(position)
            .has(Role("target"))
            .has(BoundaryCollision())
            ).eid


def init_systems(world: World):
    world.add_system(timer_system)
    world.add_system(despawn_system)

    world.add_system(target_system)  # Update velocities
    world.add_system(movement_system)  # Update positions

    world.add_system(boundary_collision_system)
    world.add_system(player_collision_system)

    # Render last
    world.add_system(init_pygame(world))


def init_pygame(world: World) -> PygameRenderSystem:
    pygame.init()
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Station Sim")
    return PygameRenderSystem(screen, screen_size, world.size)


if __name__ == '__main__':
    world_x = 20
    world_y = 20
    world = World((world_x, world_y))
    train_1 = create_waypoint(world, world_x / 3, world_y - 1)
    train_2 = create_waypoint(world, 2 * world_x / 3, world_y - 1)
    station_1 = create_waypoint(world, 0.0, world_y / 2)
    station_2 = create_waypoint(world, world_x, world_y / 2)

    init_systems(world)
    clock = pygame.time.Clock()
    running = True

    (world.build_entity().
     has(Timer(0.05, 50, time.time(), callback=spawner_callback,
               callback_args=([station_1, station_2], [train_1, train_2], "commuter"))))

    (world.build_entity().
     has(Timer(0.05, 50, time.time(), callback=spawner_callback,
               callback_args=([train_1, train_2], [station_1, station_2], "leaver"))))

    while running:
        dt = clock.tick(60) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.step(dt)

    pygame.quit()
