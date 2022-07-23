import pygame
import extra_files.game_constants as game_constants

class Ball:
    def __init__(self, x: float, y: float, radius: float = game_constants.BALL_RADIUS):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.max_vel = game_constants.BALL_MAX_VEL
        self.x_vel = game_constants.BALL_MAX_VEL
        self.y_vel = 0
        self.color = game_constants.BALL_COLOR

    def __repr__(self):
        return 'Ball(x: {}, y: {}, radius: {}, x_vel: {}, y_vel: {}, color: {})'.format(self.x,\
            self.y, self.radius, self.x_vel, self.y_vel, self.color)

    def __str__(self):
        return self.__repr__()

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

