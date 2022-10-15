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

    cover_event = True
    intro_event = False
    game_event = True
    clock = pygame.time.Clock()

    game = Game(window, (game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT), 
           (game_constants.PADDLE_WIDTH, game_constants.PADDLE_HEIGHT))

    while cover_event or intro_event:
        clock.tick(game_constants.FPS * 2)
        game.inital_loop((game_constants.BLACK, game_constants.WHITE),
                        (font_path, game_constants.WELCOME_FONT_SIZE),
                        [game_constants.COLOR_DIRECTION, game_constants.DEFINED_COLOR, game_constants.COLOR_VEL], 
                        cover = True if cover_event else False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cover_event = False
                intro_event = False
                game_event = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    cover_event = False
                    intro_event = True
                    break
    
    play_event = True
    victory_event = False

    while game_event:
        while play_event:
            clock.tick(game_constants.FPS)
            keys = pygame.key.get_pressed()

            game.loop(keys)
            game.draw((game_constants.BLACK, game_constants.WHITE), (font_path, game_constants.SCORE_FONT_SIZE))

            scores = score_handling(game.ball, game.scores, (game.left_paddle, game.right_paddle),
            (game_constants.LEFT_PLAYER_COLOR, game_constants.RIGHT_PLAYER_COLOR), game_constants.WINDOW_WIDTH)
            victory_event, game.victory_text = winner_handling(scores, victory_event, game.victory_text, game_constants.WINNING_SCORE)
            if victory_event:
                play_event = False
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play_event = False
                    break

        while victory_event:
            clock.tick(game_constants.FPS * 2)
            game.close_loop((game_constants.BLACK, game_constants.WHITE),
                            (font_path, game_constants.WELCOME_FONT_SIZE))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    victory_event = False
                    game_event = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        victory_event = False
                        play_event = True 
                        break
                    elif event.key == pygame.K_n:
                        victory_event = False
                        game_event = False
                        break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_event = False
                break

if __name__ == '__main__':
    cwd = os.getcwd()
    font_path = os.path.join(cwd, 'assets')
    main()