import pygame
import math
import random
import extra_files.game_constants as game_constants

from cls.paddle import Paddle
from typing import Optional

class Ball:
    def __init__(self, x: float, y: float, radius: float = game_constants.BALL_RADIUS)-> None:
        """__init__ constructor"""
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.angle = self._get_random_angle(-30, 30, [0])
        self.pos = 1 if random.random() < 0.5 else -1
        self.radius = radius
        self.max_vel = game_constants.BALL_MAX_VEL
        self.x_vel = self.pos * abs(math.cos(self.angle) * self.max_vel)
        self.y_vel = math.sin(self.angle) * self.max_vel
        self.color = game_constants.BALL_COLOR

    def __repr__(self)-> str:
        """__repr__ constructor"""
        return f"Ball(x: {self.x}, y: {self.y}, radius: {self.radius}, x_vel: {self.x_vel}, y_vel: {self.y_vel}, color: {self.color})"
        
    def __str__(self)-> None:
        """__str__ constructor"""
        return self.__repr__()

    def _get_random_angle(self, min_angle: int, max_angle: int, excluded: list)-> float:
        """This method returns the random angle used on the kick off stage"""
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def _set_revertion_vel(self, x_direction: Optional[bool] = False, y_direction: Optional[bool] = False)-> None:
        """This method reverts the signal of the ball along the specified direction (x_direction | y_direction)"""
        if x_direction:
            self.x_vel *= -1
        elif y_direction:
            self.y_vel *= -1

    def _set_y_vel_after_paddle_collision(self, paddle: Paddle)-> None:
        """This method computes (based on the paddle's hitted position) and reverts the signal of the ball along the y_direction"""
        middle_y = paddle.y + paddle.height / 2
        difference_y = middle_y - self.y
        self.y_vel = -1 * difference_y / (paddle.height / 2) * self.max_vel

    def draw(self, window: pygame.Surface)-> None:
        """This method draws the ball on the pygame.surface"""
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self)-> None:
        """This method handles the movement of the ball updating it's position along the time"""
        self.x += self.x_vel
        self.y += self.y_vel

    def change_direction(self, paddle: Optional[Paddle] = None, **kwargs: Optional[bool])-> None:
        """This method handles the ball's change of direction behaviour. The Paddle object is function of the ball x_vel signal"""
        if kwargs.get('up_boundary_collision', False) or kwargs.get('down_boundary_collision', False):
            self._set_revertion_vel(y_direction=True)
        elif kwargs.get('left_paddle_collision', False):
            if self.y >= paddle.y and self.y <= paddle.y + paddle.height:
                if self.x - self.radius <= paddle.x + paddle.width: # left paddle hit
                    paddle._increase_number_of_touches()
                    self._set_revertion_vel(x_direction = True)
                    self._set_y_vel_after_paddle_collision(paddle)
        elif kwargs.get('right_paddle_collision', False):
            if self.y >= paddle.y and self.y <= paddle.y + paddle.height: 
                if self.x + self.radius >= paddle.x: # right paddle hit
                    paddle._increase_number_of_touches()
                    self._set_revertion_vel(x_direction = True)
                    self._set_y_vel_after_paddle_collision(paddle)

    def reset(self)-> None:
        """This method resets the ball object by mutating some of the instance attribute variables"""
        self.x = self.original_x
        self.y = self.original_y

        self.angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(self.angle) * self.max_vel)
        y_vel = math.sin(self.angle) * self.max_vel

        self.y_vel = y_vel
        self.x_vel *= -1

