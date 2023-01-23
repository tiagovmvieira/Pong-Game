import pygame
import extra_files.game_constants as game_constants

from cls.paddle import Paddle
from cls.ball import Ball
from cls.button import Button
from cls.launcher import Launcher

from states.base import BaseState
from states.menu import Menu
from states.game_over import GameOver

from typing import Final, List


class GameInformation:
    _scores: List[int] = [0, 0]


class GameElements:
    _paddles: List[Paddle] = [
        Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2),
        Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
                                game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    ]
    _ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)


class MenuElements:
    _state_font = Menu.get_state_font()
    _buttons: List[Button] = [
        Button('Start Game', (250, 250), _state_font),
        Button('Quit Game', (250, 350), _state_font)
    ]


class GameOverElements:
    _state_font = GameOver.get_state_font()
    _buttons: List[Button] = [
        Button("Play Again", (250, 250), _state_font),
        Button("Quit Game", (250, 350), _state_font)
    ]
    _launchers: List[Launcher] = [
        Launcher(game_constants.WINDOW_WIDTH / 5, game_constants.WINDOW_HEIGHT - game_constants.LAUNCHER_HEIGHT, 3000),
        Launcher(game_constants.WINDOW_WIDTH * 4 / 5, game_constants.WINDOW_HEIGHT - game_constants.LAUNCHER_HEIGHT, 2000)
    ]


class GameStatesHandler:
    def __init__(self, screen: pygame.Surface, states: dict, start_state: str)-> None:
        """__init__ constructor"""
        self.screen = screen
        self.states = states
        self.state_name = start_state
        self.previous_state = None

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps: Final[int] = game_constants.FPS
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

    def _bootstrap_state(self, **kwargs)-> None:
        """This method includes the state bootstrap logic according to the fed kwargs"""
        if kwargs.get("gameplay", False):
            self.state.set_state_elements(GameElements._paddles, GameElements._ball)
            self.state.set_initial_positions()
            self.state.set_game_initial_score(GameInformation._scores)
        elif kwargs.get("menu", False):
            self.state.set_state_elements(MenuElements._buttons)
        elif kwargs.get("game_over", False):
            self.state.set_state_elements(GameOverElements._buttons, GameOverElements._launchers)
            for launcher in self.state.launchers:
                launcher.reset_start_time()

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
                self._bootstrap_state(gameplay=True)
        elif self.state_name == "MENU":
            self._bootstrap_state(menu=True)
        elif self.state_name == "GAME_OVER":
            self._bootstrap_state(game_over=True)

    def update(self, dt: int)-> None:
        """This function orchestrates the flip_state method and handles the update logic on each state"""
        if self.state.quit:
            # meter sys.quit aqui ver Clear Codes
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self)-> None:
        """This function handles the drawing logic on each state"""
        self.state.draw(self.screen)

    def run(self)-> None:
        """This function is the game main loop"""
        while not self.done:
            dt = self.clock.tick(self.fps * 2 if self.state_name == "SPLASH" else self.fps)
            self.event_loop()

            if self.state_name == "GAMEPLAY":
                self.state.handle_paddle_movement()
                self.state.ball.move()
                self.state.handle_collision()
                self.state.score_handling()
                self.state.winner_handling()
            elif self.state_name == "GAME_OVER":
                for launcher in self.state.launchers:
                    launcher.loop(self.screen, game_constants.WINDOW_WIDTH, game_constants.WINDOW_HEIGHT)
            
            self.update(dt)
            self.draw()
            pygame.display.update()