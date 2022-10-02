import pygame
import extra_files.game_constants as game_constants

from typing import Tuple

class Paddle():
    def __init__(self, x: int, y: int, width: int = game_constants.PADDLE_WIDTH, height: int = game_constants.PADDLE_HEIGHT,
                vel: float = game_constants.PADDLE_VEL, colors: Tuple[tuple, tuple] = game_constants.PADDLE_COLOR):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.colors = colors

    def __repr__(self):
        return f"Paddle(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, vel: {self.vel}, colors: {self.colors})"

    def __str__(self):
        return self.__repr__()

    def draw(self, window: pygame.surface, paddle_position: str):
        if paddle_position == 'left':
            pygame.draw.rect(window, self.colors[0], (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(window, self.colors[1], (self.x, self.y, self.width, self.height))

    def move(self, up: bool = True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y