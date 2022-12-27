import pygame
import os
import extra_files.game_constants as game_constants

from .base import BaseState
from typing import Final


class GamePause(BaseState):
    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.game_pause_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.pause_message = self.game_pause_font.render('Game Paused', True, game_constants.WHITE)
        self.text_rect_pause = self.pause_message.get_rect()
        self.text_rect_pause.center = (self.window_width // 2 - self.pause_message.get_width() // 2,
                                    (self.window_height * 1 // 4 - self.pause_message.get_height() // 2)                                    
                                    )

        self.backspace_message = self.game_pause_font.render('Press BACKSPACE to resume', True, game_constants.WHITE)
        self.text_rect_backspace = self.pause_message.get_rect()
        self.text_rect_backspace.center = (self.window_width // 2 - self.backspace_message.get_width() // 2,
                                        (self.window_height * 3 // 4 - self.backspace_message.get_height() // 2)
                                        )

        self.next_state: Final[str] = "GAMEPLAY"

    def update(self, dt: int):
        pass

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.done = True

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        surface.blit(self.pause_message, self.text_rect_pause.center)
        surface.blit(self.backspace_message, self.text_rect_backspace.center)








