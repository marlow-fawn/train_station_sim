from components import Velocity
from world import World


def recognition_system(world: World, dt) -> None:
    for entity in world.entities_with(Velocity):
        # Step 1: get its velocity. Add it to the histogram? How should I deal with multivar? Diff histograms for each?
        pass