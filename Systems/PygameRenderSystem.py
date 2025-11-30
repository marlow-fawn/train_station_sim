import pygame

from components import Position, Role

colors = {"target": (255, 0, 0),
          "robot": (0, 255, 255)}


class PygameRenderSystem:
    def __init__(self, screen: pygame.Surface, screen_size, world_size):
        self.screen = screen
        self.screen_width, self.screen_height = screen_size
        self.world_width, self.world_height = world_size

        # choose a scale so your world fits on screen
        self.scale_x = self.screen_width / self.world_width
        self.scale_y = self.screen_height / self.world_height

    def __call__(self, world: 'World', dt: float) -> None:
        # background
        self.screen.fill((20, 20, 20))

        # (optional) draw a faint grid
        grid_color = (40, 40, 40)
        for i in range(self.world_width + 1):
            x = int(i * self.scale_x)
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen_height))
        for j in range(self.world_height + 1):
            y = int(j * self.scale_y)
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen_width, y))

        # draw entities as discs
        for eid in world.entities_with(Position, Role):
            pos = world.get_component(eid, Position)

            # convert world coords (0..world_width) to pixels
            px = int(pos.x * self.scale_x)
            py = int(pos.y * self.scale_y)

            # flip y so bigger y is "up" in world
            py = self.screen_height - py

            # pick a color; e.g. based on Role if present
            role = world.get_component(eid, Role)
            color = colors.get(role.name, (0, 255, 0))
            # you could inspect Role here and change color

            radius = 8
            pygame.draw.circle(self.screen, color, (px, py), radius)

        pygame.display.flip()
