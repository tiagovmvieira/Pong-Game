import pygame
import os
import extra_files.game_constants as game_constants

from .base import BaseState
from typing import Final


class GameOver(BaseState):
    _time_active_threshold: Final[int] = 10000

    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.close_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.winner_message = self.close_font.render('{}'.format(self.persist.get("winner_message")), True, game_constants.WHITE)


        self.revenge_message = self.close_font.render('{}'.format('Do you want to play again? (Y/N)'), True, game_constants.WHITE)
        self.text_rect_revenge = self.revenge_message.get_rect()
        self.text_rect_revenge.center = (self.window_width // 2 - self.revenge_message.get_width() // 2,
                                        (self.window_height * 3 // 4 - self.revenge_message.get_height() // 2)
                                        )

        self._time_active: Final[int] = 0

    def _reset_time_active(self)-> None:
        self._time_active = 0

    def _generate_time_active_message(self)-> None:
        """This method generates the time active message block message to be draw"""
        self.time_active_message = self.close_font.render('{}'.format(10 - (self._time_active // 1000)), True, game_constants.WHITE)
        self.text_rect_active = self.time_active_message.get_rect()
        self.text_rect_active.center = (self.window_width // 2 - self.time_active_message.get_width() // 2,
                                    (self.window_height * 6 // 10 - self.time_active_message.get_height() // 2)
                                    )

    def _update_winner_message(self)-> None:
        self.winner_message = self.close_font.render('{}'.format(self.persist.get("winner_message")), True, game_constants.WHITE)
        self.text_rect_winner = self.winner_message.get_rect()
        self.text_rect_winner.center = (self.window_width // 2 - self.winner_message.get_width() // 2,
                                    (self.window_height * 1 // 4 - self.winner_message.get_height() // 2)
                                    )

    def update(self, dt: int)-> None:
        self._time_active += dt #dt in miliseconds
        self._update_winner_message()
        self._generate_time_active_message()
        if self._time_active >= self._time_active_threshold:
            self.persist.clear()
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.next_state: str = "GAMEPLAY"
                self._reset_time_active()
                self.persist.clear()
                self.done = True
            elif event.key == pygame.K_n:
                self.quit = True

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        surface.blit(self.winner_message, self.text_rect_winner.center)
        surface.blit(self.revenge_message, self.text_rect_revenge.center)
        surface.blit(self.time_active_message, self.text_rect_active.center)