import dataclasses
from random import random, choice

from components import Position, Velocity, BoundaryCollision, Role, Target, PlayerCollision, Despawn


def spawner_callback(world: 'World', *args) -> None:

    start_position = choice(args[0])
    target_eid = choice(args[1])
    print(target_eid)
    (world.build_entity()
     .has(dataclasses.replace(world.get_component(start_position, Position)))
     .has(Velocity(10 * (random() - 0.5),
                   10 * (random() - 0.5)))
     .has(BoundaryCollision())
     .has(PlayerCollision())
     .has(Role(args[2]))
     .has(Target(target_eid))
     .has(Despawn(Target(target_eid)))
     )

    # Todo: Requires that components have default args.
    # Fine for now but need to enforce/log somehow
    # eid = world.create_entity()
    # for ctype in spawner.components:
    #     world.add_component(eid, ctype())
