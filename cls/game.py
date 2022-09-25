import pygame
import random
import os

from typing import Tuple, Optional, List
from cls.paddle import Paddle
from cls.ball import Ball
from utils.util_functions import handle_collision_paddle_y_vel, score_handling, winner_handling

class GameInformation():
    def __init__(self, left_score: int, right_score: int):
        self.left_score = left_score
        self.right_score = right_score

class Game():
    def __init__(self, window: pygame.Surface, window_dims: Tuple[int, int], paddle_dims: Tuple[int, int]):
        self.window = window
        self.window_width = window_dims[0]
        self.window_height = window_dims[1]

        self.left_paddle = Paddle(10, self.window_height // 2 - paddle_dims[1] // 2)
        self.right_paddle = Paddle(self.window_width - 10 - paddle_dims[0],\
                                  self.window_height // 2 - paddle_dims[1] // 2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.scores = [self.left_score, self.right_score]
        self.victory_text = ''

    def _draw_divider(self, colors: Tuple[tuple, tuple]):
        for i in range(10, self.window_height, self.window_height // 20):
            if (i % 2) == 1: #odd i?
                continue
            pygame.draw.rect(self.window, colors[1], (self.window_width // 2 - 5, i, 10, self.window_height / 20))

    def _draw_score(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        score_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        
        left_score_text = score_font.render('{}'.format(self.scores[0]), 1, colors[1])
        right_score_text = score_font.render('{}'.format(self.scores[1]), 1, colors[1])

        self.window.blit(left_score_text, ((self.window_width // 4) - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, ((self.window_width // 4 + (self.window_width / 2) - right_score_text.get_width() // 2), 20))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # collision with the field horizonal boundaries
        if (ball.y + ball.radius >= self.window_height): #down (y)
            ball.y_vel *= -1
        elif (ball.y - ball.radius <= 0): #up (y)
            ball.y_vel *= -1
    
        # paddle collision:
        if ball.x_vel < 0:
            #going to collide to the left paddle
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1
                    ball.y_vel = handle_collision_paddle_y_vel(ball, left_paddle)
        else:
            # going to collide to the right paddle
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    ball.x_vel *= -1
                    ball.y_vel = handle_collision_paddle_y_vel(ball, right_paddle)

    def _handle_paddle_movement(self, keys: list):
        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        elif keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height <= self.window_height:
            self.left_paddle.move(up = False)
        elif keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.move(up = True)
        elif keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height <= self.window_height:
            self.right_paddle.move(up = False)

    def draw(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int], draw_score: Optional[bool] = True):
        self.window.fill(colors[0])

        if draw_score:
            self._draw_score(colors, font_settings)

        self._draw_divider(colors)

        for paddle in [self.left_paddle, self.right_paddle]:
            if paddle == self.left_paddle:
                paddle.draw(self.window, 'left')
            else:
                paddle.draw(self.window, 'right')

        self.ball.draw(self.window)
        pygame.display.update()
        
    def draw_intro(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.window.fill(colors[0])

        welcome_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        welcome_message = welcome_font.render('Welcome to Pong!', 1, colors[1])
        text_rect_welcome = welcome_message.get_rect()
        text_rect_welcome.center = (self.window_width // 2 - welcome_message.get_width() // 2,
                                   (self.window_height * 1 // 4 - welcome_message.get_height() // 2)
                                   )

        enter_message = welcome_font.render('Press ENTER to continue', 1, colors[1])
        text_rect_enter = enter_message.get_rect()
        text_rect_enter.center = (self.window_width // 2 - enter_message.get_width() // 2,
                                 (self.window_height * 3 // 4 - enter_message.get_height() // 2)
                                 )

        self.window.blit(welcome_message, text_rect_welcome.center)
        self.window.blit(enter_message, text_rect_enter.center)
        pygame.display.update()

    def draw_close(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.window.fill(colors[0])

        close_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        winner_message = close_font.render('{}'.format(self.victory_text), 1, colors[1])
        text_rect_winner = winner_message.get_rect()
        text_rect_winner.center = (self.window_width // 2 - winner_message.get_width() // 2,
                                  (self.window_height * 1 // 4 - winner_message.get_height() // 2)
                                  )

        revenge_message = close_font.render('{}'.format('Do you want to play again? (Y/N)'), 1, colors[1])
        text_rect_revenge = revenge_message.get_rect()
        text_rect_revenge.center = (self.window_width // 2 - revenge_message.get_width() // 2,
                                   (self.window_height * 3 // 4 - revenge_message.get_height() // 2)
                                   )

        self.window.blit(winner_message, text_rect_winner.center)
        self.window.blit(revenge_message, text_rect_revenge.center)
        pygame.display.update()

    def intro_loop(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.draw_intro(colors, font_settings)

    def loop(self, keys: list):
        self._handle_paddle_movement(keys)
        self.ball.move()
        self._handle_collision()

    def close_loop(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.draw_close(colors, font_settings)
