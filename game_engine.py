"""
game_engine
"""

import pygame
from utils.util_functions import *

def intro_session(clock, fps: int, window: pygame.Surface, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int],
                  font_settings: Tuple[str, int], color_settings: list):

    clock.tick(fps * 2)
    draw_intro(window, colors, window_dims, font_settings, color_settings)

def game_session(clock, fps: int, window: pygame.Surface, ball : Ball, paddles: Tuple[Paddle, Paddle], scores: list,
                colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_settings: Tuple[str, int], keys: list):
    clock.tick(fps)
    draw(window, ball, paddles, scores, colors, window_dims, font_settings)
    handle_paddle_movement(keys, paddles, window_dims[1])

    ball.move()
    handle_collision(ball, paddles, window_dims[1])

def closing_session(window: pygame.Surface, victory_text: str, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int],
                   font_settings: Tuple[str, int], color_settings: list):
    draw_close(window, victory_text, colors, window_dims, font_settings, color_settings)