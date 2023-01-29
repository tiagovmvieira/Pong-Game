import pygame
import math

import extra_files.game_constants as game_constants

from .projectile import Projectile
from typing import Final, Union, List
from random import randint, choice


class Firework:
    radius : Final[int] = game_constants.FIREWORK_RADIUS
    _projectile_vel: Final[int] = game_constants.PROJECTILE_VEL
    _max_projectiles: Final[int] = game_constants.FIREWORK_MAX_PROJECTILES
    _min_projectiles: Final[int] = game_constants.FIREWORK_MIN_PROJECTILES
    min_speed: Final[int] = game_constants.FIREWORK_SPEED_MIN
    max_speed: Final[int] = game_constants.FIREWORK_SPEED_MAX
    gravity_force: pygame.math.Vector2 = pygame.math.Vector2(0, 0.3)

    def __init__(self, x: int, y: int, explode_height: int):    
        """__init__ constructor"""
        self.pos = pygame.math.Vector2(x, y)
        self.explode_height = explode_height

        self.color = tuple(randint(0, 255) for i in range(3))
        self.colors = tuple(tuple(randint(0, 255) for i in range(3)) for j in range(3))

        self.firework: Projectile = Projectile(self.pos.x, self.pos.y, True, self.color)

        self.projectiles: Union[None, List[Projectile]] = None
        self.exploded: bool = False

    def __repr__(self)-> str:
        """__repr__ constructor"""
        return f"Firework(exploded: {self.exploded}, projectiles: {self.projectiles}, explode_height: {self.explode_height})"

    def __str__(self)-> None:
        """__str__ constructor"""
        return self.__repr__()

    def update(self, surface: pygame.Surface, max_width: int, max_height: int)-> None:
        """This method xxxx"""
        if not self.exploded:
            self.firework.apply_force(self.gravity_force)
            self.firework.move(explode_height=self.explode_height)
            self.draw(surface)
            if self.firework.vel.y >= 0:
                self.explode()
        else:
            for projectile in self.projectiles:
                projectile.update()
                projectile.draw(surface)

    def explode(self)-> None:
        """This method sets the instance variable exploded to True and populates the 
            projectiles list based on the projectiles amount computed"""
        self.exploded = True
        number_of_projectiles = randint(
            self._min_projectiles,
            self._max_projectiles
        )

        self.projectiles = [Projectile(self.firework.pos.x, self.firework.pos.y,
                                    False, choice(self.colors)) for _ in range(number_of_projectiles)]

    def remove(self)-> bool:
        if not self.exploded:
            return False

        for projectile in self.projectiles:
            if projectile.remove:
                self.projectiles.remove(projectile)

        # remove the firework object if all projectiles were removed
        return len(self.projectiles) == 0

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the firework on the pygame.surface"""
        x_pos = int(self.firework.pos.x) # grab the x_pos from the 2D vector
        y_pos = int(self.firework.pos.y) # grab the y_pos from the 2D vector

        pygame.draw.circle(surface, self.color, (x_pos, y_pos), self.firework.radius)