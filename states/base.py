import pygame
import os
import extra_files.game_constants as game_constants

from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self)-> None:
        if self.__class__ == BaseState:
            raise TypeError("Instantiating the Abstract Class")

        self.window_width = game_constants.WINDOW_WIDTH
        self.window_height = game_constants.WINDOW_HEIGHT

        self.done: bool = False
        self.quit: bool = False
        self.next_state: None = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist: dict = {}

        self._root_dir = os.getcwd()
        self.assets_dir = os.path.join(self._root_dir, 'assets')

    @abstractmethod
    def startup(self, persistent):
        """This method sets the persistent data between states, thus allowing data diffusion through the states"""
        pass

    @abstractmethod
    def get_event(self, event: pygame.event.Event):
        """This method handles how to react to specific events"""
        pass

    @abstractmethod
    def update(self, dt: int)-> None:
        """This method handles the update of the state"""
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the specified components on the surface"""
        pass