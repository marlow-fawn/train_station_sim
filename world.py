from typing import TypeVar, Callable, List, Dict, Type

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
        self.width = size[0]
        self.height = size[1]
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
