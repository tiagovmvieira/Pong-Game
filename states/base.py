import pygame
import os
import extra_files.game_constants as game_constants

from abc import ABC, abstractmethod

class BaseState(ABC):
    assets_dir = os.path.join(os.getcwd(), 'assets')

    def __init__(self)-> None:
        """__init__ constructor"""
        if self.__class__ == BaseState:
            raise TypeError("Instantiating the Abstract Class")

        self.window_width = game_constants.WINDOW_WIDTH
        self.window_height = game_constants.WINDOW_HEIGHT

        self.done: bool = False
        self.resume: bool = False
        self.quit: bool = False
        self.next_state: str = ''
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist: dict = {}

    def startup(self, persistent):
        """This method sets the persistent data between states, thus allowing data diffusion through the game states"""
        self.persist = persistent
        self.resume = False

    @abstractmethod
    def get_event(self, event: pygame.event.Event, keys: pygame.key.ScancodeWrapper):
        """This method handles how to react to specific events and keys pressed"""
        pass

    @abstractmethod
    def update(self, dt: int)-> None:
        """This method handles the update of the state"""
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the specified components on the surface"""
        pass