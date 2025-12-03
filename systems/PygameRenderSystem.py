import pygame
from pygame import Rect

from components import Position, Role, Color
from world import World

colors = {"target": (255, 0, 0),
          "robot": (0, 255, 255),
          "commuter": (0, 200, 200),
          "leaver": (200, 0, 200),
          "train": (255, 255, 150)
          }


def _pos_to_pixels(pos_x, pos_y, scale_x, scale_y) -> tuple[int, int]:
    px = int(pos_x * scale_x)
    py = int(pos_y * scale_y)
    return px, py


class PygameRenderSystem:
    def __init__(self, screen: pygame.Surface, screen_size, world_size):
        print("video driver:", pygame.display.get_driver())
        self.screen = screen
        self.screen_width, self.screen_height = screen_size
        self.world_width, self.world_height = world_size

        # choose a scale so your world fits on screen
        self.scale_x = self.screen_width / self.world_width
        self.scale_y = self.screen_height / self.world_height

    def __call__(self, world: World, dt: float) -> None:
        # background
        self.screen.fill((20, 20, 20))

        # (optional) draw a faint grid
        grid_color = (180, 180, 180)
        for i in range(self.world_width + 1):
            x = int(i * self.scale_x)
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.screen_height))
        for j in range(self.world_height + 1):
            y = int(j * self.scale_y)
            pygame.draw.line(self.screen, grid_color, (0, y), (self.screen_width, y))

        for eid in world.entities_with(Role, Position):
            pos = world.get_component(eid, Position)
            px, py = _pos_to_pixels(pos.x, pos.y, self.scale_x, self.scale_y)
            role = world.get_component(eid, Role)
            if role.name == "train":
                color = colors.get(role.name, (0, 255, 0))
                train_sprite = Rect(0, 0, 10 * self.scale_x, 5 * self.scale_y)
                train_sprite.center = (px, py)
                pygame.draw.rect(self.screen, color, train_sprite)

        # draw entities
        for eid in world.entities_with(Position, Color):

            pos = world.get_component(eid, Position)
            px, py = _pos_to_pixels(pos.x, pos.y, self.scale_x, self.scale_y)

            # Flip y
            color = world.get_component(eid, Color).color
            radius = 8
            pygame.draw.circle(self.screen, color, (px, py), radius)

        pygame.display.flip()
