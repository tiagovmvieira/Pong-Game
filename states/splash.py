import pygame
import os
import extra_files.game_constants as game_constants

from .base import BaseState
from typing import List, Union


class Splash(BaseState):
    _defined_color = game_constants.DEFINED_COLOR

    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.splash_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.welcome_message = self.splash_font.render('Welcome to Pong!', True, game_constants.WHITE)
        self.text_rect_welcome = self.welcome_message.get_rect()
        self.text_rect_welcome.center = (self.window_width // 2 - self.welcome_message.get_width() // 2,
                                        (self.window_height * 1 // 4 - self.welcome_message.get_height() // 2)                                    
                                        )

        self.enter_message = self.splash_font.render('Press ENTER to continue', True, self._defined_color)
        self.text_rect_enter = self.enter_message.get_rect()
        self.text_rect_enter.center = (self.window_width // 2 - self.enter_message.get_width() // 2,
                                    (self.window_height * 3 // 4 - self.enter_message.get_height() // 2)
                                    )

        self.next_state: str = "MENU"
        self.time_active: int = 0

    @classmethod
    def _set_defined_color(cls, defined_color_to_define: list)-> None:
        """This function sets the attribute variable defined color to the one resulting from the color change method"""
        cls._defined_color = defined_color_to_define

    def _color_change(self, color_settings: List[Union[tuple, int]])-> list:
        for i in range(len(color_settings[0])):
            color_settings[1][i] += color_settings[2] * color_settings[0][i]
            if color_settings[1][i] >= 255:
                color_settings[1][i] = 0
            elif color_settings[1][i] <= 0:
                color_settings[1][i] = 255

        return color_settings[1]

    def update(self, dt)-> None:
        self.time_active += dt
        if self.time_active >= 5000:
            self.done = True

    def draw(self, surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        surface.blit(self.welcome_message, self.text_rect_welcome.center)
        surface.blit(self.enter_message, self.text_rect_enter.center)

        self._set_defined_color(self._color_change(
            [
                game_constants.COLOR_DIRECTION,
                game_constants.DEFINED_COLOR,
                game_constants.COLOR_VEL
            ]
        ))
        self.enter_message = self.splash_font.render('Press ENTER to continue', True, self._defined_color)