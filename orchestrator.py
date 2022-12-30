"""
pong game
author: tiago vieira, tiagomvmvieira@hotmail.com
"""

import sys
import os
import pygame
import extra_files.game_constants as game_constants

from states.splash import Splash
from states.menu import Menu
from states.gameplay import GamePlay
from states.game_pause import GamePause
from states.game_over import GameOver

from cls.game import Game


class Orchestrator:
    def __init__(self)-> None:
        pygame.init()
        game_screen = pygame.display.set_mode((game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Pong Game")

        states = {
            "SPLASH": Splash(),
            "MENU": Menu(),
            "GAMEPLAY": GamePlay(),
            "GAME_PAUSE": GamePause(),
            "GAME_OVER": GameOver()
        }

        game = Game(game_screen, states, "SPLASH")
        game.run()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    o = Orchestrator()