import pygame
import time
import random
import threading

import extra_files.game_constants as game_constants

from .firework import Firework
from typing import Final, Union
   
class Launcher:
    _width: Final[int] = game_constants.LAUNCHER_WIDTH
    _height: Final[int] = game_constants.LAUNCHER_HEIGHT

    def __init__(self, x: int, y: int, launch_frequency: float)-> None:
        """__init__ constructor"""
        self.x = x
        self.y = y
        self.launch_frequency = launch_frequency # ms

        self._start_time: Union[None, float] = None
        self.fireworks = []

    def __repr__(self)-> str:
        """__repr__ constructor"""
        return f"Launcher(x: {self.x}, y: {self.y}, launch_frequency: {self.launch_frequency}, start_time: {self._start_time})"
        
    def __str__(self)-> None:
        """__str__ constructor"""
        return self.__repr__()

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

        for firework in self.fireworks:
            firework.draw(surface)

    def launch(self)-> None:
        """This method "launches" a firework by creating one and storing it on a list"""
        # color = random.choice(colors) # don't have colors
        color = "#354B5E"
        explode_height = random.randrange(50, 400) # pass into constants

        firework = Firework(self.x + (self._width / 2), self.y, 5, explode_height, color)
        self.fireworks.append(firework)

    def loop(self, max_width: int, max_height: int)-> None:
        """This method creates a loop that is responsible for launching the firework and moving the firework"""
        current_time: float = time.time()
        time_elapsed: float = current_time - self._start_time

        if time_elapsed * 1000 >= float(self.launch_frequency):
            self.reset_start_time(current_time=current_time)
            self.launch()

        # move all of the fireworks
        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move(max_width, max_height)
            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)