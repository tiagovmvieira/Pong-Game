import pygame
import time
import random

import extra_files.game_constants as game_constants

from .firework import Firework
from typing import Final, Union, List

class Launcher:
    _width: Final[int] = game_constants.LAUNCHER_WIDTH
    _height: Final[int] = game_constants.LAUNCHER_HEIGHT

    def __init__(self, x: int, y: int, launch_frequency: float)-> None:
        """__init__ constructor"""
        self.x = x
        self.y = y
        self.launch_frequency = launch_frequency # ms

        self._start_time: Union[None, float] = None
        self.fireworks: List[Firework] = []

    def __repr__(self)-> str:
        """__repr__ constructor"""
        return f"Launcher(x: {self.x}, y: {self.y}, launch_frequency: {self.launch_frequency}, start_time: {self._start_time})"
        
    def __str__(self)-> None:
        """__str__ constructor"""
        return self.__repr__()

    def update(self, surface: pygame.Surface)-> None:
        """This method handles the fireworks' dynamic since its called every frame"""
        for firework in self.fireworks:
            firework.update(surface)
            if firework.remove():
                self.fireworks.remove(firework)

        pygame.display.update()

    def reset_start_time(self, current_time: Union[float, None] = None)-> None:
        """This method resets the _start_time instance variable according to a time value"""
        if current_time:
            self._start_time = current_time
        else:
            self._start_time = time.time()

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the launcher on the pygame.surface"""
        
        launcher = pygame.Rect((self.x , self.y), (self._width, self._height))
        pygame.draw.rect(surface, "#354B5E", launcher)

    def launch(self)-> None:
        """This method "launches" a firework by creating one and storing it on a list"""
        firework = Firework(self.x + (self._width / 2), self.y, random.randrange(50, 400))
        self.fireworks.append(firework)

    def loop(self, surface: pygame.Surface)-> None:
        """This method creates a loop that is responsible for launching the firework and calling the update method"""
        current_time: float = time.time()
        time_elapsed: float = current_time - self._start_time

        if time_elapsed * 1000 >= float(self.launch_frequency):
            self.reset_start_time(current_time=current_time)
            self.launch()

        self.update(surface)