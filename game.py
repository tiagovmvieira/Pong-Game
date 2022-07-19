"""
pong game
author: tiago vieira, tiagovmvieira@hotmail.com
"""

# imports
import pygame
import game_constants

from utils import *

def main():
    pygame.init()

    window = pygame.display.set_mode((game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT))

    intro = True
    clock = pygame.time.Clock()

    while intro:
        clock.tick(game_constants.FPS * 4)
        draw_intro(window, game_constants.BLACK, game_constants.WHITE, game_constants.WELCOME_FONT_SIZE,
        game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    intro = False
                    break

    run = True

if __name__ == '__main__':
    main()