"""
game_engine
"""

import pygame
from utils import *

def intro_session(clock, fps: int, window: pygame.Surface, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int):
    clock.tick(fps * 4)
    draw_intro(window, colors, window_dims, font_size)

def game_session(clock, fps: int, window: pygame.Surface, ball : Ball, paddles: Tuple[Paddle, Paddle], scores: list,
                colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int, keys: list):
    
    clock.tick(fps)
    draw(window, ball, paddles, scores, colors, window_dims, font_size)
    handle_paddle_movement(keys, paddles, window_dims[1])

    ball.move()
    handle_collision(ball, paddles, window_dims[1])








