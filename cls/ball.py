import pygame
import math
import random
import extra_files.game_constants as game_constants

from cls.paddle import Paddle
from typing import Optional

class Ball():
    def __init__(self, x: float, y: float, radius: float = game_constants.BALL_RADIUS):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.angle = self.__get_random_angle(-30, 30, [0])
        self.pos = 1 if random.random() < 0.5 else -1
        self.radius = radius
        self.max_vel = game_constants.BALL_MAX_VEL
        self.x_vel = self.pos * abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
        self.color = game_constants.BALL_COLOR

    def __repr__(self):
        return f"Ball(x: {self.x}, y: {self.y}, radius: {self.radius}, x_vel: {self.x_vel}, y_vel: {self.y_vel}, color: {self.color})"
        
    def __str__(self):
        return self.__repr__()

    def __get_random_angle(self, min_angle: int, max_angle: int, excluded: list):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def __set_revertion_vel(self, x_direction: Optional[bool] = False, y_direction: Optional[bool] = False):
        if x_direction:
            self.x_vel *= -1
        elif y_direction:
            self.y_vel *= -1 

    def __set_y_vel_after_paddle_collision(self, paddle: Paddle):
        middle_y = paddle.y + paddle.height / 2
        difference_y = middle_y - self.y
        self.y_vel = -1 * difference_y / (paddle.height / 2) * self.max_vel

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def change_direction(self, paddle: Optional[Paddle] = None, up_boundary_collision: Optional[bool] = False,
                        down_boundary_collision: Optional[bool] = False, left_paddle_collision: Optional[bool] = False,
                        right_paddle_collision: Optional[bool] = False):

        if up_boundary_collision or down_boundary_collision:
            self.__set_revertion_vel(y_direction= True)
        elif left_paddle_collision:
            if self.y >= paddle.y and self.y <= paddle.y + paddle.height:
                if self.x - self.radius <= paddle.x + paddle.width:
                    self.__set_revertion_vel(x_direction = True)
                    self.__set_y_vel_after_paddle_collision(paddle)
        elif right_paddle_collision:
            if self.y >= paddle.y and self.y <= paddle.y + paddle.height:
                if self.x + self.radius >= paddle.x:
                    self.__set_revertion_vel(x_direction = True)
                    self.__set_y_vel_after_paddle_collision(paddle)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        self.angle = self.__get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(self.angle) * self.max_vel)
        y_vel = math.sin(self.angle) * self.max_vel

        self.y_vel = y_vel
        self.x_vel *= -1

