import pygame
import time
import random

import extra_files.game_constants as game_constants

from .firework import Firework
from typing import Final, Union

class Launcher:
    _width: Final[int] = game_constants.LAUNCHER_WIDTH
    _height: Final[int] = game_constants.LAUNCHER_HEIGHT
    _start_time: Union[None, float] = None

    def __init__(self, x: int, y: int, launch_frequency: float)-> None:
        """__init__ constructor"""
        self.x = x
        self.y = y
        self.launch_frequency = launch_frequency # ms

        self.fireworks = []

    @classmethod
    def set_start_time(cls)-> None:
        """This method sets the _start_time cls variable according to the instant time"""
        cls._start_time = time.time()

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the launcher on the pygame.surface"""
        
        launcher = pygame.Rect((self.x , self.y), (self._width, self._height))
        pygame.draw.rect(surface, "#354B5E", launcher)

        print(self.fireworks)

        for firework in self.fireworks:
            firework.draw(surface)

    def launch(self)-> None:
        """This method launches"""
        # color = random.choice(colors) # don't have colors
        color = "#354B5E"
        explode_height = random.randrange(50, 400) # pass into constants

        firework = Firework(self.x + (self._width / 2), self.y, -5, explode_height, color)
        self.fireworks.append(firework)

    def loop(self, max_width: int, max_height: int)-> None:
        """This method loops"""

        current_time: float = time.time()
        time_elapsed: float = current_time - self._start_time

        if time_elapsed * 1000 >= float(self.launch_frequency):
            self.launch()
            self._start_time = current_time

        # move all of the fireworks
        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move(max_width, max_height)
            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)