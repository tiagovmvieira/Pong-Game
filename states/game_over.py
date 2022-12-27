import pygame
import os
import extra_files.game_constants as game_constants

from .base import BaseState


class GameOver(BaseState):
    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.close_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.winner_message = self.close_font.render('{}'.format('Winner'), True, game_constants.WHITE)
        self.text_rect_winner = self.winner_message.get_rect()
        self.text_rect_winner.center = (self.window_width // 2 - self.winner_message.get_width() // 2,
                                    (self.window_height * 1 // 4 - self.winner_message.get_height() // 2)
                                    )

        self.revenge_message = self.close_font.render('{}'.format('Do you want to play again? (Y/N)'), True, game_constants.WHITE)
        self.text_rect_revenge = self.revenge_message.get_rect()
        self.text_rect_revenge.center = (self.window_width // 2 - self.revenge_message.get_width() // 2,
                                        (self.window_height * 3 // 4 - self.revenge_message.get_height() // 2)
                                        )
        
        self.time_active: int = 0

    def update(self, dt: int):
        self.time_active += dt
        if self.time_active >= 10000:
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        """This method handles how to react to specific events"""
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.next_state: str = "GAMEPLAY"
                self.done = True
            elif event.key == pygame.K_n:
                self.quit = True

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the specified components on the surface"""
        surface.fill(game_constants.PURE_BLACK)
        surface.blit(self.winner_message, self.text_rect_winner.center)
        surface.blit(self.revenge_message, self.text_rect_revenge.center)