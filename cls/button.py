import pygame
import extra_files.game_constants as game_constants

from pygame.locals import *
from typing import Final


class Button:
    _width: Final[int] = game_constants.BUTTON_WIDTH
    _height: Final[int] = game_constants.BUTTON_HEIGHT
    _elevation: Final[int] = game_constants.BUTTON_ELEVATION
    def __init__(self, text: str, pos: tuple, font: pygame.font)-> None:
        """__init__ constructor"""

        # Core attributes
        self.pressed = False
        self.dynamic_elevation = self._elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rectangle = pygame.Rect((pos), (self._width, self._height))
        self.top_rectangle_color = '#475F77'

        # bottom rectangle
        self.bottom_rectangle = pygame.Rect((pos), (self._width, self._elevation))
        self.bottom_rectangle_color = "#354B5E"

        # text
        self.text_surface = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rectangle.center)

    def draw(self, screen: pygame.surface)-> None:
        """This method draws the button on the pygame.surface"""
        # elevation logic
        self.top_rectangle.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rectangle.center

        self.bottom_rectangle.midtop = self.top_rectangle.midtop
        self.bottom_rectangle.height = self.top_rectangle.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_rectangle_color, self.bottom_rectangle, border_radius = 12)
        pygame.draw.rect(screen, self.top_rectangle_color, self.top_rectangle, border_radius = 12)
        screen.blit(self.text_surface, self.text_rect)
        self.check_click()

    def check_click(self)-> bool:
        """This method checks if the button was clicked"""
        mouse_position: tuple = pygame.mouse.get_pos()

        if self.top_rectangle.collidepoint(mouse_position): #top rectangle colliding with the mouse position?
            self.top_rectangle_color = "#D74B4B"
            if pygame.mouse.get_pressed()[0]: #pressing mouse left button?
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self._elevation
                if self.pressed == True:
                    self.pressed = False
                    pygame.time.wait(130)
                return self.pressed
        else:
            self.dynamic_elevation = self._elevation
            self.top_rectangle_color = "#475F77"

        return self.pressed