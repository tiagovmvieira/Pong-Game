import pygame
import extra_files.game_constants as game_constants

class Paddle():
    def __init__(self, x: int, y: int, width: int = game_constants.PADDLE_WIDTH, height: int = game_constants.PADDLE_HEIGHT,
                vel: float = game_constants.PADDLE_VEL, color: tuple = game_constants.PADDLE_COLOR):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color

    def __repr__(self):
        return 'Paddle(x: {}, y: {}, width: {}, height: {}, vel: {}, color: {})'.format(self.x, self.y,\
            self.width, self.height, self.vel, self.color)

    def __str__(self):
        return self.__repr__()

    def draw(self, window: pygame.surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up: bool = True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y