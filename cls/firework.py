import pygame
import extra_files.game_constants as game_constants

from typing import Final

class Firework:
    _radius : Final[int] = game_constants.FIREWORK_RADIUS

    def __init__(self, x: int, y: int, y_vel: int, explode_height: int, color)-> None:
        """__init__ constructor"""
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.explode_height = explode_height
        self.color = color

        self.projectiles: list = []
        self.exploded: bool = False

    def explode(self)-> None:
        """This method sets the instance variable exploded to True"""
        self.exploded = True

    def move(self, max_width: int, max_height: int)-> None:
        """This method handles the movement of the firework object"""
        if not self.exploded:
            self.y -= self.y_vel # y position of the firework will be decreasing until it reaches the explode height
            if self.y > self.explode_height:
                self.explode()
    
    def draw(self, surface: pygame.Surface)-> None:
        print("estou aqui")
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self._radius)