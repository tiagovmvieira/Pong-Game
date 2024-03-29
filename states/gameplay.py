import pygame
import os
import pyfiglet

import extra_files.game_constants as game_constants

from termcolor import colored
from typing import Union, Final, List

from .base import BaseState
from cls.paddle import Paddle
from cls.ball import Ball

class GamePlay(BaseState):
    left_player_score: Union[None, int] = None
    right_player_score: Union[None, int] = None
    left_paddle: Union[None, Paddle] = None
    right_paddle: Union[None, Paddle] = None
    ball: Union[None, Ball] = None

    def __init__(self)-> None:
        """__init__ constructor"""
        super().__init__()

        self._winning_score: int = game_constants.WINNING_SCORE
        self.winner_message: str = ''

        self._left_player_color = game_constants.LEFT_PLAYER_COLOR
        self._right_player_color = game_constants.RIGHT_PLAYER_COLOR

    @classmethod
    def set_state_elements(cls, paddles: List[Paddle], ball: Ball)-> None:
        """This class allocates on the left_paddle, right_paddle and ball cls variables the corresponding GameElements objects"""
        cls.left_paddle = paddles[0]
        cls.right_paddle = paddles[1]
        cls.ball = ball

    @classmethod
    def set_game_initial_score(cls, scores: List[int])-> None:
        """This class allocates on the left_player_score and right_player_score cls variables the corresponding GameInformation variables"""
        cls.left_player_score = scores[0]
        cls.right_player_score = scores[1]

    @classmethod
    def _set_player_score(cls, **kwargs)-> None:
        """This method sets the player(s) score based on the **kwargs that are being passed"""
        if kwargs.get('reset_players_score', False):
            cls.left_player_score, cls.right_player_score = 0, 0
        else:
            if kwargs.get('left_player'):
                cls.left_player_score += 1
            else:
                cls.right_player_score += 1

    @classmethod
    def set_initial_positions(cls)-> None:
        """This method sets the initial positions of the game elements (left_paddle, right_paddle, and ball)"""
        cls.left_paddle.reset()
        cls.right_paddle.reset()
        cls.ball.reset()

    def handle_paddle_movement(self)-> None:
        """This method handles the paddle movement based on the keys that are being pressed on the keyboard"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height <= self.window_height:
            self.left_paddle.move(up = False)
        if keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.move(up = True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height <= self.window_height:
            self.right_paddle.move(up = False)

    def handle_collision(self)-> None:
        """This method handles ball collisions with field horizontal boundaries and paddles"""
        # collision with the field horizontal boundaries
        if self.ball.y + self.ball._radius >= self.window_height: #down (y)
            self.ball.change_direction(down_boundary_collision=True)
        elif (self.ball.y - self.ball._radius <= 0): #up (y)
            self.ball.change_direction(up_boundary_collision=True)

        # paddle collision:
        if self.ball.x_vel < 0:
            # going to colllide to the left paddle
            self.ball.change_direction(paddle = self.left_paddle, left_paddle_collision = True)
        else:
            # going to collide to the right paddle
            self.ball.change_direction(paddle = self.right_paddle, right_paddle_collision = True)

    def score_handling(self)-> None:
        """This method handles the result score of the game, and the corresponding commands"""
        goal_text = pyfiglet.figlet_format('Goal', font='isometric2')

        if self.ball.x > self.window_width:
            print(colored(goal_text, self._left_player_color))
            self._set_player_score(left_player=True)
        elif self.ball.x < 0:
            print(colored(goal_text, self._right_player_color))
            self._set_player_score()

        if self.ball.x > self.window_width or self.ball.x < 0:
            self.ball.reset()
            self.left_paddle.reset()
            self.right_paddle.reset()

    def winner_handling(self)-> None:
        """This method handles the winner event proceedings (winner message re-declaration, players' score reset, and next state migration"""
        if self.left_player_score == self._winning_score or self.right_player_score == self._winning_score:
            self.winner_message = "Left Player Won!" if self.left_player_score == self._winning_score else "Right Player Won!"
            self.persist["winner_message"] = self.winner_message
            self._set_player_score(reset_players_score=True)
            self.next_state: str = "GAME_OVER"
            self.done = True

    def _handle_action(self, **kwargs)-> None:
        """This method handles the action to proceed in based on the fed kwargs from the get_event method"""
        if kwargs.get("game_pause", False):
            self.next_state: str = "GAME_PAUSE"
            self.persist.update(
                    {
                        "left_paddle": self.left_paddle,
                        "right_paddle": self.right_paddle,
                        "ball": self.ball,
                        "left_player_score": self.left_player_score,
                        "right_player_score": self.right_player_score
                    }
                )
            self.done = True
        else:
            self.quit = True

    def get_event(self, event: pygame.event.Event)-> None:
        if event.type == pygame.QUIT:
            self._handle_action()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._handle_action(game_pause=True)

    def update(self, dt: int)-> None:
        pass

    def _draw_score(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abstract the behaviour within it"""
        self.score_font = pygame.font.Font(os.path.join(self.assets_dir, os.listdir(self.assets_dir)[0]), game_constants.SCORE_FONT_SIZE)

        left_score_text = self.score_font.render('{}'.format(self.left_player_score), True, game_constants.WHITE)
        right_score_text = self.score_font.render('{}'.format(self.right_player_score), True, game_constants.WHITE)

        surface.blit(left_score_text,
                    ((self.window_width / 2) - (left_score_text.get_width() / 2) - (self.ball._radius) - 2 * 15,
                    (self.window_height / 2) - (left_score_text.get_height() / 2))
                    )
        surface.blit(right_score_text,
                    ((self.window_width / 2) + (right_score_text.get_width() / 2) + (self.ball._radius) + 15,
                    (self.window_height / 2) - (right_score_text.get_height() / 2))
                    )

    def _draw_divider(self, surface: pygame.Surface)-> None:
        """This method acts as an util to the main draw method, in order to abstract the behaviour within it"""
        pygame.draw.aaline(surface, game_constants.WHITE, (self.window_width / 2, 0), (self.window_width / 2, self.window_height), blend=1)

    def draw(self, surface: pygame.Surface)-> None:
        surface.fill(game_constants.PURE_BLACK)
        self._draw_score(surface)
        self._draw_divider(surface)

        if self.left_paddle and self.right_paddle and self.ball:
            for paddle in [self.left_paddle, self.right_paddle]:
                paddle.draw(surface, paddle_position = 'left' if paddle == self.left_paddle else 'right')
            
            self.ball.draw(surface)

        self.left_score_text = self.score_font.render('{}'.format(self.left_player_score), True, game_constants.WHITE)
        self.right_score_text = self.score_font.render('{}'.format(self.right_player_score), True, game_constants.WHITE)