import dataclasses
import time
from random import random, choice

from components import Position, Velocity, BoundaryCollision, Role, Target, PlayerCollision, Despawn, Color, Timer, \
    Action, Trigger, Condition
from util import create_waypoint, dist
from world import World


def send_train_callback(world: World, role: str) -> None:
    target_eid = create_waypoint(world, world.width / 2, 0.0)
    train_eid = (world.build_entity()
                 .has(Position(-world.width, 0.0))
                 .has(Velocity(0.0, 0.0))
                 .has(Role(role))
                 .has(Target(target_eid))
                 ).eid

    # Wait at station until
    (world.build_entity()
     .has(Trigger([Condition(train_arrive_condition, train_eid=train_eid, target_eid=target_eid)],
                  [Action(wait_at_station_callback, target_eid=target_eid)])))

    # Spawn people leaving the train
    train_1 = create_waypoint(world, world.width / 3, 3)
    train_2 = create_waypoint(world, 2 * world.width / 3, 3)
    station_1 = create_waypoint(world, 1.0, world.height - 1)
    station_2 = create_waypoint(world, world.width - 1.0, world.height - 1)

    (world.build_entity()
     .has(Timer(0.1, -1, time.time(), [Action(spawner_callback,
                                              start=[train_1, train_2],
                                              end=[station_1, station_2],
                                              role="leaver")])))

    # Todo: Refactor timers/triggers/despawning all into one system.
    # Todo cont'd: Create an object that deletes itself after a condition. Time is a condition.
    # Todo cont'd: We could also make a despawn tag that takes a condition. Any entity will now delete itself on condition.


def train_arrive_condition(world: World, train_eid: int, target_eid: int) -> bool:
    entity_pos = world.get_component(train_eid, Position)
    target_pos = world.get_component(target_eid, Position)
    return dist(target_pos, entity_pos) < 1.0


def wait_at_station_callback(world: World, target_eid: int) -> None:
    (world.build_entity()
     .has(Timer(5, 1, time.time(), [Action(depart_train_callback, target_eid=target_eid)])))


def depart_train_callback(world: World, target_eid: int) -> None:
    world.get_component(target_eid, Position).x = world.width * 2
    # world.delete_entity(train_eid)
    # world.delete_entity(target_eid)


def spawner_callback(world: World, start: list[int], end: list[int], role: Role) -> None:
    start_eid = choice(start)
    target_eid = choice(end)
    (world.build_entity()
     .has(dataclasses.replace(world.get_component(start_eid, Position)))
     .has(Velocity(10 * (random() - 0.5),
                   10 * (random() - 0.5)))
     .has(BoundaryCollision())
     .has(PlayerCollision())
     .has(Target(target_eid))
     .has(Color())
     .has(Despawn(Target(target_eid)))
     )
