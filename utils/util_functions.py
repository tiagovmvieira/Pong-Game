# imports
import pygame
import os
import pyfiglet

from termcolor import colored
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

def score_handling(ball: Ball, scores: List[int], paddles: Tuple[Paddle, Paddle], players_info: Tuple[int, int], window_width: int)-> list:
    goal_text = pyfiglet.figlet_format('Goal', font='isometric2')
    if ball.x > window_width:
        print(colored(goal_text, players_info[0]))
        scores[0] += 1
        ball.reset()
        paddles[0].reset
        paddles[1].reset
    elif ball.x < 0:
        print(colored(goal_text, players_info[1]))
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