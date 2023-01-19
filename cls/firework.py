import pygame
import random
import math

import extra_files.game_constants as game_constants

from .projectile import Projectile
from typing import Final

class Firework:
    _radius : Final[int] = game_constants.FIREWORK_RADIUS
    _projectile_vel: Final[int] = game_constants.PROJECTILE_VEL
    _max_projectiles: Final[int] = game_constants.FIREWORK_MAX_PROJECTILES
    _min_projectiles: Final[int] = game_constants.FIREWORK_MIN_PROJECTILES

    def __init__(self, x: int, y: int, y_vel: int, explode_height: int, color: tuple)-> None:
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
        number_of_projectiles = random.randrange(
            self._min_projectiles,
            self._max_projectiles
        )

        self.create_circular_projectiles(number_of_projectiles)

    def create_circular_projectiles(self, number_of_projectiles: int):
        """This method creates a circular pattern to launch the projectiles"""
        angle_difference = math.pi * 2 / number_of_projectiles
        current_angle = 0
        velocity = random.randrange(self._projectile_vel - 1,
                                    self._projectile_vel + 1)
        for i in range(number_of_projectiles):
            x_vel = math.sin(current_angle) * velocity
            y_vel = math.cos(current_angle) * velocity
            color = "#354B5E"
            self.projectiles.append(Projectile(self.x, self.y, x_vel, y_vel, color))
            current_angle += angle_difference

    def move(self, max_width: int, max_height: int)-> None:
        """This method handles the movement of the firework object"""
        if not self.exploded:
            self.y -= self.y_vel # y position of the firework will be decreasing or increasing until it reaches the explode height
            if self.y <= self.explode_height:
                self.explode()

        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()

            if projectile.x >= max_width or projectile.x < 0:
                projectiles_to_remove.append(projectile)
            elif projectile.y >= max_height or projectile.y < 0:
                projectiles_to_remove.append(projectile)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)
    
    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the firework on the pygame.surface"""
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (self.x, self.y), self._radius)