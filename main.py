import random
from typing import Dict, TypeVar, Type, List, Callable
import pygame

from Systems.BoundaryCollisionSystem import boundary_collision_system
from Systems.PlayerCollisionSystem import player_collision_system
from components import *
from Systems.MovementSystem import movement_system
from Systems.TargetSystem import target_system
from Systems.CollisionSystem import collision_system
from Systems.PygameRenderSystem import PygameRenderSystem

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


if __name__ == '__main__':
    world = World()

    # Initialize pygame stuff
    pygame.init()
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("ECS little guys")
    render_system = PygameRenderSystem(screen, screen_size, world.size)

    # Create moving target
    target = (world.build_entity()
              .has(Position(random.random() * world.size[0],
                            random.random() * world.size[1]))
              .has(Velocity(10 * (random.random() - 0.5),
                            10 * (random.random() - 0.5)))
              .has(Role("target"))
              .has(BoundaryCollision())
              ).eid

    agents = 100

    # Create commuters
    for _ in range(agents):
        (world.build_entity()
         .has(Position(random.random() * world.size[0],
                       random.random() * world.size[1]))
         .has(Velocity(10 * (random.random() - 0.5),
                       10 * (random.random() - 0.5)))
         .has(Role())
         .has(BoundaryCollision())
         .has(PlayerCollision())
         .has(Target(target))
         )

    (world.build_entity()
     .has(Position(random.random() * world.size[0],
                   random.random() * world.size[1]))
     .has(Velocity(10 * (random.random() - 0.5),
                   10 * (random.random() - 0.5)))
     )

    # Declare systems
    world.add_system(target_system)
    world.add_system(movement_system)
    world.add_system(boundary_collision_system)
    world.add_system(player_collision_system)
    world.add_system(render_system)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.step(dt)

    pygame.quit()
