import pygame
import os
import extra_files.game_constants as game_constants

from typing import Tuple, Optional, List, Union

from .base import BaseState
from cls.paddle import Paddle
from cls.ball import Ball
from cls.button import Button

class GamePlay(BaseState):
    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        # self.winning_score = winning_score

        self.left_score: int = 0
        self.right_score: int = 0
        self.victory_text: str = ''

        self.left_paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
                                game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
        self.ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)

    def _handle_paddle_movement(self, keys: list)-> None:
        """This method handle the paddle movement based on the keys that are being pressed and retrieved on the get_event method"""
        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height <= self.window_height:
            self.left_paddle.move(up = False)
        if keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.move(up = True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height <= self.window_height:
            self.right_paddle.move(up = False)

    def get_event(self, event: pygame.event.Event)-> None:
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.next_state: str = "GAME_PAUSE"
                self.done = True
            if event.key == pygame.K_m:
                self.next_state: str = "GAME_OVER"
                self.done = True
        
        self._handle_paddle_movement(keys)

    def update(self, dt: int)-> None:
        pass

    def _draw_score(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abstract the behaviour within it"""
        score_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), game_constants.SCORE_FONT_SIZE)

        left_score_text = score_font.render('{}'.format(self.left_score), True, game_constants.WHITE)
        right_score_text = score_font.render('{}'.format(self.right_score), True, game_constants.WHITE)

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

        self.ball.draw(surface)
        