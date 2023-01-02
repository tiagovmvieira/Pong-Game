import pygame
import extra_files.game_constants as game_constants

from cls.paddle import Paddle
from cls.ball import Ball
from typing import Final

from states.base import BaseState

class GameInformation:
    _left_player_score: Final[int] = 0
    _right_player_score: Final[int] = 0


class GameElements:
    _left_paddle: Paddle = Paddle(10, game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    _right_paddle: Paddle = Paddle(game_constants.WINDOW_WIDTH - 10 - game_constants.PADDLE_WIDTH,\
                                game_constants.WINDOW_HEIGHT // 2 - game_constants.PADDLE_HEIGHT // 2)
    _ball = Ball(game_constants.WINDOW_WIDTH // 2, game_constants.WINDOW_HEIGHT // 2)


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
        self.state = self.states.get(self.state_name, None)

    def event_loop(self)-> None:
        """This function handles the game event loop"""
        for event in pygame.event.get():
            self.state.get_event(event)

    def _set_previous_state(self, previous_state):
        """This method stores the previous state of the game into an atribute variable"""
        self.previous_state = previous_state

    def flip_state(self)-> None:
        """This function flips the state assumed on the game"""
        self._set_previous_state(self.state_name)

        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states.get(self.state_name, None)
        self.state.startup(persistent)

        if self.state_name == "GAMEPLAY":
            if self.previous_state == "MENU":
                self.state.set_game_elements(GameElements._left_paddle, GameElements._right_paddle, GameElements._ball)
                self.state.set_game_initial_score(GameInformation._left_player_score, GameInformation._right_player_score)

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