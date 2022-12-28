import pygame
import os
import pyfiglet

import extra_files.game_constants as game_constants

from termcolor import colored
from typing import Final

from .base import BaseState
from cls.paddle import Paddle
from cls.ball import Ball

class GamePlay(BaseState):
    _left_player_score : int = 0
    _right_player_score : int = 0 

    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()

        self.winning_score = game_constants.WINNING_SCORE
        self.victory_text: str = ''

        self.left_paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
                                game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
        self.ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)

        self.left_player_color = game_constants.LEFT_PLAYER_COLOR
        self.right_player_color = game_constants.RIGHT_PLAYER_COLOR

    @classmethod
    def _set_player_score(cls, left_player: bool = False)-> None:
        if left_player:
            cls._left_player_score += 1
        else:
            cls._right_player_score += 1

    def _handle_paddle_movement(self)-> None:
        """This method handle the paddle movement based on the keys that are being pressed on the keyboard"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height <= self.window_height:
            self.left_paddle.move(up = False)
        if keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.move(up = True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height <= self.window_height:
            self.right_paddle.move(up = False)

    def _handle_collision(self)-> None:
        """This method handles ball collisions with field horizontal boundaries and paddles"""
        # collision with the field horizontal boundaries
        if self.ball.y + self.ball.radius >= self.window_height: #down (y)
            self.ball.change_direction(down_boundary_collision = True)
        elif (self.ball.y - self.ball.radius <= 0): #up (y)
            self.ball.change_direction(up_boundary_collision = True)

        # paddle collision:
        if self.ball.x_vel < 0:
            # going to colllide to the left paddle
            self.ball.change_direction(paddle = self.left_paddle, left_paddle_collision = True)
        else:
            # going to collide to the right paddle
            self.ball.change_direction(paddle = self.right_paddle, right_paddle_collision = True)

    def _score_handling(self):
        """This method handles the result score of the game, and the corresponding commands"""
        goal_text = pyfiglet.figlet_format('Goal', font='isometric2')

        if self.ball.x > self.window_width or self.ball.x < 0:
            self.ball.reset()
            self.left_paddle.reset()
            self.right_paddle.reset()

        if self.ball.x > self.window_width:
            print(colored(goal_text, self.left_player_color))
            self.left_score += 1
            self._set_player_score(left_player=True)
        elif self.ball.x < 0:
            print(colored(goal_text, self.right_player_color))
            self.right_score += 1

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.next_state: str = "GAME_PAUSE"
                self.done = True
            if event.key == pygame.K_m:
                self.next_state: str = "GAME_OVER"
                self.done = True

    def update(self, dt: int)-> None:
        pass

    def _draw_score(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abstract the behaviour within it"""
        self.score_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), game_constants.SCORE_FONT_SIZE)

        left_score_text = self.score_font.render('{}'.format(self._left_player_score), True, game_constants.WHITE)
        right_score_text = self.score_font.render('{}'.format(self._right_player_score), True, game_constants.WHITE)

        surface.blit(left_score_text, ((self.window_width // 4) - left_score_text.get_width() // 2, 20))
        surface.blit(right_score_text, ((self.window_width // 4 + (self.window_width / 2) - right_score_text.get_width() // 2), 20))

    def _draw_divider(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abstract the behaviour within it"""
        for i in range(10, self.window_height, self.window_height // 20):
            if (i % 2) == 1: #odd i?
                continue
            pygame.draw.rect(surface, game_constants.WHITE, (self.window_width // 2 - 5, i, 10, self.window_height / 20))

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        self._draw_score(surface)
        self._draw_divider(surface)

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(surface, paddle_position = 'left' if paddle == self.left_paddle else 'right')

        self.left_score_text = self.score_font.render('{}'.format(self._left_player_score), True, game_constants.WHITE)
        self.right_score_text = self.score_font.render('{}'.format(self._right_player_score), True, game_constants.WHITE)

        self.ball.draw(surface)
        