import pygame
import os
import extra_files.game_constants as game_constants

from .base import BaseState
from cls.button import Button
from typing import Final


class GameOver(BaseState):
    pygame.init()
    _time_active_threshold: Final[int] = game_constants.GAME_OVER_ACTIVE_THRESHOLD
    play_again_button: None = None
    quit_game_button: None = None
    state_font: pygame.font = pygame.font.Font(os.path.join(BaseState.assets_dir, os.listdir(BaseState.assets_dir)[0]), 20)

    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.close_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.winner_message = self.close_font.render('{}'.format(self.persist.get("winner_message")), True, game_constants.WHITE)
        self._time_active: Final[int] = 0

    @classmethod
    def get_state_font(cls)-> pygame.font:
        return cls.state_font

    @classmethod
    def set_state_elements(cls, play_again_button: Button, quit_game_button: Button)-> None:
        cls.play_again_button = play_again_button
        cls.quit_game_button = quit_game_button

    def _reset_time_active(self)-> None:
        self._time_active = 0

    def _generate_time_active_message(self)-> None:
        """This method generates the time active message block message to be draw"""
        self.time_active_message = self.close_font.render('{}'.format((self._time_active_threshold - self._time_active) * 1 // 1000), True,\
                                                        game_constants.WHITE)
        self.text_rect_active = self.time_active_message.get_rect()
        self.text_rect_active.center = (self.window_width // 2 - self.time_active_message.get_width() // 2,
                                    (self.window_height * 4 // 10 - self.time_active_message.get_height() // 2)
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
            self._handle_action()

    def _handle_action(self, **kwargs)-> None:
        """This method handles the action to proceed in based on the fed kwargs from the get_event method"""
        if kwargs.get("play_again", False):
            self.next_state: str = "GAMEPLAY"
            self._reset_time_active()
            self.persist.clear()
            self.done = True
        else:
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self._handle_action()
        elif self.play_again_button.dynamic_elevation == 0 and not self.play_again_button.check_click():
            self._handle_action(play_again=True)
        elif self.quit_game_button.dynamic_elevation == 0 and not self.quit_game_button.check_click():
            self._handle_action()

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        surface.blit(self.winner_message, self.text_rect_winner.center)
        surface.blit(self.time_active_message, self.text_rect_active.center)

        if self.play_again_button and self.quit_game_button:
            self.play_again_button.draw(surface)
            self.quit_game_button.draw(surface)