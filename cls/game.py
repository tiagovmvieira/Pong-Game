import pygame
import extra_files.game_constants as game_constants

from cls.paddle import Paddle
from cls.ball import Ball
from cls.button import Button
from typing import Final

from states.base import BaseState
from states.menu import Menu

class GameInformation:
    _left_player_score: Final[int] = 0
    _right_player_score: Final[int] = 0


class GameElements:
    _left_paddle: Paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    _right_paddle: Paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
                                game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    _ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)


class MenuElements:
    _menu_font = Menu.get_menu_font()
    _start_game_button = Button('Start Game', game_constants.COVER_BUTTON_WIDTH, game_constants.COVER_BUTTON_HEIGHT, (250, 250), 6,
                            _menu_font)
    _quit_game_button = Button('Quit Game', game_constants.COVER_BUTTON_WIDTH, game_constants.COVER_BUTTON_HEIGHT, (250, 350), 6,
                            _menu_font)

class GameStatesHandler:
    def __init__(self, screen: pygame.Surface, states: dict, start_state: str)-> None:
        """__init__ constructor"""
        self.screen = screen
        self.states = states
        self.state_name = start_state
        self.previous_state = None

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = game_constants.FPS
        self.state: BaseState = self.states.get(self.state_name, None)

    def event_loop(self)-> None:
        """This function handles the game event loop"""
        for event in pygame.event.get():
            self.state.get_event(event)

    def _set_previous_state(self, previous_state):
        """This method stores the previous state of the game into an atribute variable"""
        self.previous_state = previous_state

    def _set_previous_state_resume(self, previous_state_resume):
        """This method stores the previous state resume attribute variable of the game into an attribute variable"""
        self.previous_state_resume = previous_state_resume

    def _bootstrap_gameplay_state(self)-> None:
        """This method includes the gameplay state bootstrap logic"""
        self.state.set_game_elements(GameElements._left_paddle, GameElements._right_paddle, GameElements._ball)
        self.state.set_initial_positions()
        self.state.set_game_initial_score(GameInformation._left_player_score, GameInformation._right_player_score)

    def _bootstrap_menu_state(self)-> None:
        """This method includes the menu state bootstrap logic"""
        self.state.set_menu_elements(MenuElements._start_game_button, MenuElements._quit_game_button)

    def flip_state(self)-> None:
        """This function flips the state assumed on the game"""
        self._set_previous_state(self.state_name)
        self._set_previous_state_resume(self.state.resume)

        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states.get(self.state_name, None)
        self.state.startup(persistent)

        if self.state_name == "GAMEPLAY":
            if self.previous_state in ["MENU", "GAME_PAUSE"] and not self.previous_state_resume:
                pygame.time.wait(300) if self.previous_state == "GAME_PAUSE" else None
                self._bootstrap_gameplay_state()
        elif self.state_name == "MENU":
            self._bootstrap_menu_state()

    def update(self, dt: int)-> None:
        """This function updates.."""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self)-> None:
        """This function draws.."""
        self.state.draw(self.screen)

    def run(self)-> None:
        """This function runs the game"""
        while not self.done:
            dt = self.clock.tick(self.fps * 2 if self.state_name == "SPLASH" else self.fps)
            self.event_loop()

            if self.state_name == "GAMEPLAY":
                self.state.handle_paddle_movement()
                self.state.ball.move()
                self.state.handle_collision()
                self.state.score_handling()
                self.state.winner_handling()

            self.update(dt)
            self.draw()
            pygame.display.update()