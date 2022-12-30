import pygame
import os

from .base import BaseState
import extra_files.game_constants as game_constants

class Menu(BaseState):
    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()
        self.menu_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), 20)

        self.active_index: int = 0
        self.options: list = ["Start Game", "Quit Game"]
        self.next_state: str = "GAMEPLAY"

    def render_text(self, index)-> None:
        color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
        return self.menu_font.render(self.options[index], True, color)

    def get_text_position(self, text, index)-> None:
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)

    def handle_action(self)-> None:
        if self.active_index == 0:
            self.done = True
        elif self.active_index == 1:
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
            elif event.key == pygame.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
            elif event.key == pygame.K_RETURN:
                self.handle_action()

    def update(self, dt: int)-> None:
        """This method handles the update of the state"""
        pass

    def draw(self, surface: pygame.Surface)-> None:
        """This method draws the specified components on the surface"""
        surface.fill(game_constants.PURE_BLACK)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))