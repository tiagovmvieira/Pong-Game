import pygame
import math
import random
import extra_files.game_constants as game_constants

class Ball():
    def __init__(self, x: float, y: float, radius: float = game_constants.BALL_RADIUS):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.angle = self._get_random_angle(-30, 30, [0])
        self.pos = 1 if random.random() < 0.5 else -1
        self.radius = radius
        self.max_vel = game_constants.BALL_MAX_VEL
        self.x_vel = self.pos * abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
        self.color = game_constants.BALL_COLOR

    def __repr__(self):
        return 'Ball(x: {}, y: {}, radius: {}, x_vel: {}, y_vel: {}, color: {})'.format(self.x,\
            self.y, self.radius, self.x_vel, self.y_vel, self.color)

    def __str__(self):
        return self.__repr__()

    def _get_random_angle(self, min_angle: int, max_angle: int, excluded: list):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        self.angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(self.angle) * self.max_vel)
        y_vel = math.sin(self.angle) * self.max_vel

        self.y_vel = y_vel
        self.x_vel *= -1

