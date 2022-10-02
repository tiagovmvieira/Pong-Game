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
from cls.game import Game

def main():
    pygame.init()
    window = pygame.display.set_mode((game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT))
    pygame.display.set_caption("Pong Game")

    cover = True
    intro = False
    game = True
    clock = pygame.time.Clock()

    game = Game(window, (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), 
           (game_constants.PADDLE_WIDTH, game_constants.PADDLE_HEIGHT))

    while cover or intro:
        clock.tick(game_constants.FPS * 2)
        game.inital_loop((game_constants.BLACK, game_constants.WHITE),
                        (font_path, game_constants.WELCOME_FONT_SIZE),
                        [game_constants.COLOR_DIRECTION, game_constants.DEFINED_COLOR, game_constants.COLOR_VEL], 
                        cover = True if cover else False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cover = False
                intro = False
                game = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    cover = False
                    intro = True
                    break
    
    play = True
    victory = False

    while game:
        while play:
            clock.tick(game_constants.FPS)
            keys = pygame.key.get_pressed()

            game.loop(keys)
            game.draw((game_constants.BLACK, game_constants.WHITE), (font_path, game_constants.SCORE_FONT_SIZE))

            scores = score_handling(game.ball, game.scores, (game.left_paddle, game.right_paddle),
            (game_constants.LEFT_PLAYER_COLOR, game_constants.RIGHT_PLAYER_COLOR), game_constants.WINDOW_WIDTH)
            victory, game.victory_text = winner_handling(scores, victory, game.victory_text, game_constants.WINNING_SCORE)
            if victory:
                play = False
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    break

        while victory:
            clock.tick(game_constants.FPS * 2)
            game.close_loop((game_constants.BLACK, game_constants.WHITE),
                            (font_path, game_constants.WELCOME_FONT_SIZE))

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
    cwd = os.getcwd()
    font_path = os.path.join(cwd, 'assets')
    main()