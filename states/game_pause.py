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

        self.active_index: int = 0
        self.pause_menu_options: list = ["Resume", "Quit", "Restart"]

        self.rect_box = pygame.Rect(0, 0, 500, 75)
        self.rect_box.center = (self.window_width // 2, self.window_height // 2 + 150)

        self.pause_message = self.game_pause_font.render('Game Paused', True, game_constants.BLACK)

        self.backspace_message = self.game_pause_font.render('Press BACKSPACE to resume', True, game_constants.WHITE)
        self.text_rect_backspace = self.pause_message.get_rect()
        self.text_rect_backspace.center = (self.window_width // 2 - self.backspace_message.get_width() // 2,
                                        (self.window_height * 3 // 4 - self.backspace_message.get_height() // 2)
                                        )

    def update(self, dt: int)-> None:
        pass

    def _handle_action(self):
        """This methosd handles the action concerning state flip based on the active index"""
        if self.active_index == 0:
            self.persist.clear()
            self.next_state: str = "GAMEPLAY"
            self.resume = True
            self.done = True
        elif self.active_index == 1:
            self.quit = True
        elif self.active_index == 2:
            self.persist.clear()
            self.next_state: str = "GAMEPLAY"
            self.done = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if self.active_index in [0, 1]:
                    self.active_index += 1
                else:
                    self.active_index = 0
            elif event.key == pygame.K_LEFT:
                if self.active_index in [1, 2]:
                    self.active_index -= 1
                else:
                    self.active_index = 2
            elif event.key == pygame.K_RETURN:
                self._handle_action()            

    def _render_text(self, index: int)-> pygame.Surface:
        """This method renders the text grabbed through the index on the options attribute and returns the Pygame Surface"""
        color = game_constants.BLUE if index == self.active_index else game_constants.BLACK
        return self.game_pause_font.render(self.pause_menu_options[index], True, color)

    def _get_text_position(self, text, index)-> tuple:
        """This method computes and returns the text center position"""
        if index == 0:
            center = (self.rect_box_obj.center[0] - 100 - (text.get_width() / 2), self.rect_box_obj.center[1])
        elif index == 1:
            center = (self.rect_box_obj.center[0], self.rect_box_obj.center[1])
        else:
            center = (self.rect_box_obj.center[0] + (text.get_width() / 2) + 100, self.rect_box_obj.center[1])

        return text.get_rect(center=center)

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

        # score
        left_player_score = self.persist.get("left_player_score", None)
        right_player_score = self.persist.get("right_player_score", None)
    
        score_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), game_constants.SCORE_FONT_SIZE)

        left_score_text = score_font.render('{}'.format(left_player_score), True, game_constants.WHITE)
        right_score_text = score_font.render('{}'.format(right_player_score), True, game_constants.WHITE)
    
        surface.blit(left_score_text, ((self.window_width // 4) - left_score_text.get_width() // 2, 20))
        surface.blit(right_score_text, ((self.window_width // 4 + (self.window_width / 2) - right_score_text.get_width() // 2), 20))

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)

        self._draw_elements_from_gameplay_state(surface)

        # pause box
        self.rect_box_obj = pygame.draw.rect(surface, 'white', self.rect_box, border_radius = 10)
        self.text_rect_pause = self.pause_message.get_rect(center=(self.rect_box_obj.center[0], self.rect_box_obj.center[1]- 20))
        
        surface.blit(self.pause_message, self.text_rect_pause)

        for index, option in enumerate(self.pause_menu_options):
            text_render = self._render_text(index)
            surface.blit(text_render, self._get_text_position(text_render, index))