# imports
import pygame
import os

from typing import Tuple
from ball import Ball
from paddle import Paddle

def draw_intro(window: pygame.Surface, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int):
    window.fill(colors[0])

    welcome_font = pygame.font.SysFont('arial', font_size)
    # welcome_font = pygame.font.Font('assets/PixelEmulator-xq08.ttf',
    #                                font_size)
    welcome_message = welcome_font.render('Welcome to Pong!', 1, colors[1])
    text_rect_welcome = welcome_message.get_rect()
    text_rect_welcome.center = (window_dims[0] // 2 - welcome_message.get_width() // 2,
                             (window_dims[1] * 1 // 4 - welcome_message.get_height() // 2))

    enter_message = welcome_font.render('Press ENTER to continue', 1, colors[1])
    text_rect_enter = enter_message.get_rect()
    text_rect_enter.center = (window_dims[0] // 2 - enter_message.get_width() // 2,
                             (window_dims[1] * 3 // 4 - enter_message.get_height() // 2))

    window.blit(welcome_message, text_rect_welcome.center),
    window.blit(enter_message, text_rect_enter.center)

    pygame.display.update()


def draw(window: pygame.Surface, ball: Ball, paddles: Tuple[Paddle, Paddle], scores: Tuple[int, int], colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int):
    window.fill(Tuple[0])

    score_font = pygame.font.SysFont('arial', font_size)

    left_score_text = score_font.render('{}'.format(scores[0]), 1, colors[1])
    right_score_text = score_font.render('{}'.format(scores[1]), 1, colors[1])

    window.blit(left_score_text, ((window_dims[0] // 4) - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, ((window_dims[0] // 4 + (window_dims[0] / 2) - right_score_text.get_width() // 2), 20))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, window_dims[1], window_dims[1] // 20):
        if (i % 2) == 1: #odd i?
            continue
        pygame.draw.rect(window, colors[1], (window_dims[0] // 2 - 5, i, 10, window_dims[1] / 20))
    
    ball.draw(window)
    pygame.display.update()
