import pygame
import extra_files.game_constants as game_constants

from typing import Tuple

class Paddle:
    def __init__(self, x: int, y: int, width: int = game_constants.PADDLE_WIDTH, height: int = game_constants.PADDLE_HEIGHT,
                vel: float = game_constants.PADDLE_VEL, colors: Tuple[tuple, tuple] = game_constants.PADDLE_COLOR):
        """__init__ constructor"""
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.colors = colors
        self.touches: int = 0

    def __repr__(self)-> None:
        """__repr__ constructor"""
        return f"Paddle(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, vel: {self.vel}, colors: {self.colors})"

    def __str__(self)-> None:
        """__str__ constructor"""
        return self.__repr__()

    def _increase_number_of_touches(self)-> None:
        """This method increases the number of touches instance attribute variable"""
        self.touches += 1

    def draw(self, window: pygame.surface, paddle_position: str)-> None:
        """This method draws the paddle on the pygame.surface"""
        if paddle_position == 'left':
            pygame.draw.rect(window, self.colors[0], (self.x, self.y, self.width, self.height), border_radius = 12)
        else:
            pygame.draw.rect(window, self.colors[1], (self.x, self.y, self.width, self.height), border_radius = 12)

    def move(self, up: bool = True)-> None:
        """This method handles the movement of the paddle updating it's position along the time"""
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

    def reset(self)-> None:
        """This method resets the paddle object by redefining some of the instance attribute variables"""
        self.x = self.original_x
        self.y = self.original_y
        self.touches = 0