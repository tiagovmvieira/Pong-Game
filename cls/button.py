import pygame
from pygame.locals import *
import extra_files.game_constants as game_constants

class Button:
    def __init__(self, text: str, width: int, height: int, pos: tuple, elevation: int, font: pygame.font)-> None:
        """__init__ constructor"""
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        
        self.top_rectangle = pygame.Rect((pos), (width, height))
        self.top_rectangle_color = '#475F77'

        self.text_surface = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rectangle.center)

    def draw(self, screen: pygame.surface)-> None:
        """This method draws the button on the pygame.surface"""
        pygame.draw.rect(screen, self.top_rectangle_color, self.top_rectangle, border_radius = 12)
        screen.blit(self.text_surface, self.text_rect)
        self.check_click()

    def check_click(self)-> bool:
        """This method checks if the button was clicked"""
        mouse_position: tuple = pygame.mouse.get_pos()

        if self.top_rectangle.collidepoint(mouse_position): #top rectangle colliding with the mouse position?
            self.top_rectangle_color = "#D74B4B"
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.top_rectangle_color = "#475F77"

        return self.pressed