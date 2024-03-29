import pygame
import os

from .base import BaseState
from cls.button import Button
import extra_files.game_constants as game_constants

from typing import List

class Menu(BaseState):
    pygame.init()
    start_game_button: None = None
    quit_game_button: None = None
    state_font: pygame.font = pygame.font.Font(os.path.join(BaseState.assets_dir, os.listdir(BaseState.assets_dir)[0]), 20)
    
    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()

        self.next_state: str = "GAMEPLAY"

    @classmethod
    def get_state_font(cls)-> pygame.font:
        """This class method returns the state_font class variable"""
        return cls.state_font

    @classmethod
    def set_state_elements(cls, buttons: List[Button])-> None:
        """This class method allocates on the cls variables the corresponding objects"""
        cls.start_game_button = buttons[0]
        cls.quit_game_button = buttons[1]

    def _render_text(self, index: int)-> pygame.Surface:
        """This method renders the text grabbed through the index on the options attribute and returns the Pygame Surface"""
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.menu_font.render(self.options[index], True, color)

    def _get_text_position(self, text: pygame.Surface, index: int)-> tuple:
        """This method computes and returns the text center position"""
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def _handle_action(self, **kwargs)-> None:
        """This method handles the action concerning state flip based on the active index"""
        if kwargs.get('start_game', False):
            self.done = True
        else:
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self._handle_action()
        elif self.start_game_button.dynamic_elevation == 0 and not self.start_game_button.check_click():
            self._handle_action(start_game=True)
        elif self.quit_game_button.dynamic_elevation == 0 and not self.quit_game_button.check_click():
            self._handle_action()

    def update(self, dt: int)-> None:
        """This method handles the update of the state"""
        pass

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the specified components on the surface"""
        surface.fill(game_constants.PURE_BLACK)
        if self.start_game_button and self.quit_game_button:
            self.start_game_button.draw(surface)
            self.quit_game_button.draw(surface)