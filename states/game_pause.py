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

        self.pause_menu_options = {
            0: "A",
            1: "B",
            2: "C",
            3: "D"
        }

        self.rect_box = pygame.Rect(0, 0, 500, 75)
        self.rect_box.center = (self.window_width // 2, self.window_height // 2 + 150)

        self.pause_message = self.game_pause_font.render('Game Paused', True, game_constants.BLACK)

        self.backspace_message = self.game_pause_font.render('Press BACKSPACE to resume', True, game_constants.WHITE)
        self.text_rect_backspace = self.pause_message.get_rect()
        self.text_rect_backspace.center = (self.window_width // 2 - self.backspace_message.get_width() // 2,
                                        (self.window_height * 3 // 4 - self.backspace_message.get_height() // 2)
                                        )

        self.next_state: Final[str] = "GAMEPLAY"

    def update(self, dt: int)-> None:
        pass

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.persist.clear()
                self.done = True

    def _draw_elements_from_gameplay_state(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abtract the behaviour within it"""
        # paddles
        left_paddle = self.persist.get("left_paddle", None)
        right_paddle = self.persist.get("right_paddle", None)

        for paddle in [left_paddle, right_paddle]:
            paddle.draw(surface, paddle_position = 'left' if paddle == left_paddle else 'right')

        # ball
        ball = self.persist.get("ball", None)
        ball.draw(surface)

        # divider
        for i in range(10, self.window_height, self.window_height // 20):
            if (i % 2) == 1: #odd i?
                continue
            pygame.draw.rect(surface, game_constants.WHITE, (self.window_width // 2 - 5, i, 10, self.window_height / 20))

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)

        self._draw_elements_from_gameplay_state(surface)

        # pause box
        self.rect_box_obj = pygame.draw.rect(surface, 'white', self.rect_box, border_radius = 10)
        self.text_rect_pause = self.pause_message.get_rect(center=(self.rect_box_obj.center[0], self.rect_box_obj.center[1]- 20))
        
        surface.blit(self.pause_message, self.text_rect_pause)