"""
pong game
author: tiago vieira, tiagovmvieira@hotmail.com
"""

# imports
import pygame
import game_constants

from utils import *
from ball import Ball
from paddle import Paddle

def main():
    pygame.init()

    window = pygame.display.set_mode((game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT))

    intro = True
    clock = pygame.time.Clock()

    while intro:
        clock.tick(game_constants.FPS * 4)
        draw_intro(window, (game_constants.BLACK, game_constants.WHITE),
        (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), game_constants.WELCOME_FONT_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    intro = False
                    break

    run = True

    left_paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    right_paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
        game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)

    left_score = 0
    right_score = 0
    while run:
        clock.tick(game_constants.FPS)

        draw(window, ball, (left_paddle, right_paddle), (left_score, right_score), 
            (game_constants.BLACK, game_constants.WHITE), (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), game_constants.SCORE_FONT_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, (left_paddle, right_paddle), game_constants.WINDOW_HEIGHT)

        ball.move()
        handle_collision(ball, (left_paddle, right_paddle), game_constants.WINDOW_HEIGHT)


if __name__ == '__main__':
    main()