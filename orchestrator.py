"""
pong game
author: tiago vieira, tiagomvmvieira@hotmail.com
"""

#imports
import pygame
import os

import extra_files.game_constants as game_constants

from utils.util_functions import *
from game_engine import *
from cls.ball import Ball
from cls.paddle import Paddle


def main():
    pygame.init()
    window = pygame.display.set_mode((game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT))
    pygame.display.set_caption("Pong Game")

    game = True
    intro = True
    clock = pygame.time.Clock()
    cwd = os.getcwd()
    font_path = os.path.join(cwd, 'assets')

    while intro:
        intro_session(clock, game_constants.FPS, window, (game_constants.BLACK, game_constants.WHITE),
        (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), (font_path, game_constants.WELCOME_FONT_SIZE),
        [game_constants.COLOR_DIRECTION, game_constants.DEFINED_COLOR, game_constants.COLOR_VEL]
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                game = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    intro = False
                    break

    left_paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    right_paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
        game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)

    
    play = True
    victory = False

    while game:
        left_score = 0
        right_score = 0
        scores = [left_score, right_score]

        while play:
            victory_text = ''
            keys = pygame.key.get_pressed()
            game_session(clock, game_constants.FPS, window, ball, (left_paddle, right_paddle), scores,
                        (game_constants.BLACK, game_constants.WHITE), (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT),
                        (font_path, game_constants.SCORE_FONT_SIZE), keys
                        )

            scores = score_handling(ball, scores, (left_paddle, right_paddle), game_constants.WINDOW_WIDTH)

            victory, victory_text = winner_handling(scores, victory, victory_text, game_constants.WINNING_SCORE)  
            if victory:
                play = False
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    break
        
        while victory:
            closing_session(window, victory_text, (game_constants.BLACK, game_constants.WHITE),
                           (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), (font_path, game_constants.WELCOME_FONT_SIZE),
                           [game_constants.COLOR_DIRECTION, game_constants.DEFINED_COLOR, game_constants.COLOR_VEL]
                           )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    victory = False
                    game = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        victory = False
                        play = True 
                        break
                    elif event.key == pygame.K_n:
                        victory = False
                        game = False
                        break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break


if __name__ == '__main__':
    main()