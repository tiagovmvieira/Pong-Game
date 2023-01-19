import pygame
import extra_files.game_constants as game_constants

from typing import Final

class Projectile:
    _width: Final[int] = game_constants.PROJECTILE_WIDTH
    _height: Final[int] = game_constants.PROJECTILE_HEIGHT
    _alpha_decrement: Final[int] = game_constants.PROJECTILE_ALPHA_DECREMENT

    def __init__(self, x: int, y: int, x_vel: int, y_vel: int, color: tuple)-> None:
        """__init__ constructor"""
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color

        self.alpha = 255

    def move(self)-> None:
        """This method handles the movement of the projectile"""
        self.x += self.x_vel
        self.y += self.y_vel
        self.alpha = max(0, self.alpha - self._alpha_decrement)

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the projectile on the pygame.surface"""
        self.draw_rect_alpha(surface, self.color + (self.alpha,), self.x, self.y, self._width, self._height)

    @staticmethod
    def draw_rect_alpha(surface: pygame.Surface, color: tuple, rect)-> None:
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)
