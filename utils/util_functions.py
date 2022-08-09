# imports
import pygame
import os

from typing import Tuple, List
from cls.ball import Ball
from cls.paddle import Paddle

def color_change(color_settings: list)-> list:
    for i in range(len(color_settings[0])):
        color_settings[1][i] += color_settings[2] * color_settings[0][i]
        if color_settings[1][i] >= 255:
            color_settings[1][i] = 0
        elif color_settings[1][i] <= 0:
            color_settings[1][i] = 255

    return color_settings[1]

def handle_collision_paddle_y_vel(ball: Ball, paddle: Paddle)-> int:
    middle_y = paddle.y + paddle.height / 2
    difference_y = middle_y - ball.y
    ball.y_vel = -1 * difference_y / (paddle.height / 2) * ball.max_vel

    return ball.y_vel

def score_handling(ball: Ball, scores: List[int], paddles: Tuple[Paddle, Paddle], window_width: int)-> list:
    if ball.x > window_width:
        scores[0] += 1
        ball.reset()
        paddles[0].reset
        paddles[1].reset
    elif ball.x < 0:
        scores[1] += 1
        ball.reset()
        paddles[0].reset()
        paddles[1].reset()
    
    return scores

def winner_handling(scores: list, victory: bool, victory_text: str, winning_score: int)-> tuple:
    if scores[0] == winning_score:
        victory = True
        victory_text = 'Left Player Won!'
    elif scores [1] == winning_score:
        victory = True
        victory_text = 'Right Player Won!'

    return victory, victory_text