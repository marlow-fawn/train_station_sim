from components import Velocity, Color
from world import World
from river import cluster

clustering = cluster.KMeans(n_clusters=2, halflife=0.01, sigma=1)
subclusters = {
    0: cluster.KMeans(n_clusters=2, halflife=0.01, sigma=1),
    1: cluster.KMeans(n_clusters=2, halflife=0.01, sigma=1)
}

colors = [(255, 255, 0), (0, 255, 255)]


def clustering_system(world: World, dt) -> None:
    for entity in world.entities_with(Velocity, Color):
        vel = world.get_component(entity, Velocity)
        features = {0: vel.vx, 1: vel.vy}
        cluster_number = clustering.learn_predict_one(features)
        sub_cluster_number = subclusters[cluster_number].learn_predict_one(features)
        color = colors[cluster_number]
        if sub_cluster_number == 1:
            color = tuple([int(0.5 * c) for c in color])
        world.get_component(entity, Color).color = color
