from extra_files import game_constants
import pygame
import random
import os
import pyfiglet

from typing import Tuple, Optional, List, Union
from termcolor import colored
from cls.paddle import Paddle
from cls.ball import Ball
from cls.button import Button

class GameInformation():
    def __init__(self, left_score: int, right_score: int):
        self.left_score = left_score
        self.right_score = right_score

class Game():
    def __init__(self, window: pygame.Surface, winning_score: int, window_dims: Tuple[int, int], paddle_dims: Tuple[int, int],
                players_info: Tuple[int, int]):

        self.window = window
        self.window_width = window_dims[0]
        self.window_height = window_dims[1]

        self.left_paddle = Paddle(10, self.window_height // 2 - paddle_dims[1] // 2)
        self.right_paddle = Paddle(self.window_width - 10 - paddle_dims[0],\
                                  self.window_height // 2 - paddle_dims[1] // 2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.winning_score = winning_score
        self.left_score = 0
        self.right_score = 0
        self.victory_text = ''

        self.left_player_color = players_info[0]
        self.right_player_color = players_info[1]

    def __draw_divider(self, colors: Tuple[tuple, tuple]):
        for i in range(10, self.window_height, self.window_height // 20):
            if (i % 2) == 1: #odd i?
                continue
            pygame.draw.rect(self.window, colors[1], (self.window_width // 2 - 5, i, 10, self.window_height / 20))

    def __draw_score(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        score_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        
        left_score_text = score_font.render('{}'.format(self.left_score), 1, colors[1])
        right_score_text = score_font.render('{}'.format(self.right_score), 1, colors[1])

        self.window.blit(left_score_text, ((self.window_width // 4) - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, ((self.window_width // 4 + (self.window_width / 2) - right_score_text.get_width() // 2), 20))

    def __color_change(self, color_settings: List[Union[tuple, int]])-> list:
        for i in range(len(color_settings[0])):
            color_settings[1][i] += color_settings[2] * color_settings[0][i]
            if color_settings[1][i] >= 255:
                color_settings[1][i] = 0
            elif color_settings[1][i] <= 0:
                color_settings[1][i] = 255

        return color_settings[1]

    def __handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # collision with the field horizonal boundaries
        if (ball.y + ball.radius >= self.window_height): #down (y)
            ball.change_direction(down_boundary_collision = True)
        elif (ball.y - ball.radius <= 0): #up (y)
            ball.change_direction(up_boundary_collision = True)

        # paddle collision:
        if ball.x_vel < 0:
            #going to collide to the left paddle
            ball.change_direction(paddle = left_paddle, left_paddle_collision = True)
        else:
            # going to collide to the right paddle
            ball.change_direction(paddle = right_paddle, right_paddle_collision=True)

    def __handle_paddle_movement(self, keys: list):
        if keys[pygame.K_w] and self.left_paddle.y > 0:
            self.left_paddle.move(up = True)
        if keys[pygame.K_s] and self.left_paddle.y + self.left_paddle.height <= self.window_height:
            self.left_paddle.move(up = False)
        if keys[pygame.K_UP] and self.right_paddle.y > 0:
            self.right_paddle.move(up = True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.height <= self.window_height:
            self.right_paddle.move(up = False)

    def __draw_cover(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int], color_settings: List[Union[tuple, int]]):
        self.window.fill(colors[0])

        cover_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        welcome_message = cover_font.render('Welcome to Pong!', 1, colors[1])
        text_rect_welcome = welcome_message.get_rect()
        text_rect_welcome.center = (self.window_width // 2 - welcome_message.get_width() // 2,
                                   (self.window_height * 1 // 4 - welcome_message.get_height() // 2)
                                   )

        enter_message = cover_font.render('Press ENTER to continue', 1, color_settings[1])
        text_rect_enter = enter_message.get_rect()
        text_rect_enter.center = (self.window_width // 2 - enter_message.get_width() // 2,
                                 (self.window_height * 3 // 4 - enter_message.get_height() // 2)
                                 )

        self.window.blit(welcome_message, text_rect_welcome.center)
        self.window.blit(enter_message, text_rect_enter.center)
        color_settings[1] = self.__color_change(color_settings)
        pygame.display.update()

    def __draw_intro(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.window.fill(colors[0])
        select_mode_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        select_mode_message = select_mode_font.render('Select Mode', 1, colors[1])
        text_rect_select_mode = select_mode_message.get_rect()
        text_rect_select_mode.center = (self.window_width // 2 - select_mode_message.get_width() // 2,
                                    (self.window_height * 1 // 4 - select_mode_message.get_height() // 2)
                                    )

        single_player_button = Button(76, 230, game_constants.COVER_BUTTON_WIDTH, game_constants.COVER_BUTTON_HEIGHT, 'Single Player',\
                                    select_mode_font)

        multi_player_button = Button(416, 230, game_constants.COVER_BUTTON_WIDTH, game_constants.COVER_BUTTON_HEIGHT, 'Multi Player',\
                                    select_mode_font)
        
        single_player_button.draw(self.window)
        multi_player_button.draw(self.window)

        self.window.blit(select_mode_message, text_rect_select_mode.center)
        pygame.display.update()

    def __draw_close(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.window.fill(colors[0])

        close_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        winner_message = close_font.render('{}'.format(self.victory_text), 1, colors[1])
        text_rect_winner = winner_message.get_rect()
        text_rect_winner.center = (self.window_width // 2 - winner_message.get_width() // 2,
                                  (self.window_height * 1 // 4 - winner_message.get_height() // 2)
                                  )

        revenge_message = close_font.render('{}'.format('Do you want to play again? (Y/N)'), 1, colors[1])
        text_rect_revenge = revenge_message.get_rect()
        text_rect_revenge.center = (self.window_width // 2 - revenge_message.get_width() // 2,
                                   (self.window_height * 3 // 4 - revenge_message.get_height() // 2)
                                   )

        self.window.blit(winner_message, text_rect_winner.center)
        self.window.blit(revenge_message, text_rect_revenge.center)
        pygame.display.update()

    def __score_handling(self):
        goal_text = pyfiglet.figlet_format('Goal', font='isometric2')
        if self.ball.x > self.window_width:
            print(colored(goal_text, self.left_player_color))
            self.left_score += 1
            self.ball.reset()
            self.left_paddle.reset()
            self.right_paddle.reset()
        elif self.ball.x < 0:
            print(colored(goal_text, self.right_player_color))
            self.right_score += 1
            self.ball.reset()
            self.left_paddle.reset()
            self.right_paddle.reset()

    def winner_handling(self, victory: bool)-> tuple:
        if self.left_score == self.winning_score:
            victory = True
            self.victory_text = "Left Player Won!"
        elif self.right_score == self.winning_score:
            victory = True
            self.victory_text = "Right Player Won!"
        
        return victory

    def draw(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int], draw_score: Optional[bool] = True):
        self.window.fill(colors[0])

        if draw_score:
            self.__draw_score(colors, font_settings)

        self.__draw_divider(colors)

        for paddle in [self.left_paddle, self.right_paddle]:
            if paddle == self.left_paddle:
                paddle.draw(self.window, 'left')
            else:
                paddle.draw(self.window, 'right')

        self.ball.draw(self.window)
        pygame.display.update()

    def draw_close(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.window.fill(colors[0])

        close_font = pygame.font.Font(os.path.join(font_settings[0], os.listdir(font_settings[0])[0]), font_settings[1])
        winner_message = close_font.render('{}'.format(self.victory_text), 1, colors[1])
        text_rect_winner = winner_message.get_rect()
        text_rect_winner.center = (self.window_width // 2 - winner_message.get_width() // 2,
                                  (self.window_height * 1 // 4 - winner_message.get_height() // 2)
                                  )

        revenge_message = close_font.render('{}'.format('Do you want to play again? (Y/N)'), 1, colors[1])
        text_rect_revenge = revenge_message.get_rect()
        text_rect_revenge.center = (self.window_width // 2 - revenge_message.get_width() // 2,
                                   (self.window_height * 3 // 4 - revenge_message.get_height() // 2)
                                   )

        self.window.blit(winner_message, text_rect_winner.center)
        self.window.blit(revenge_message, text_rect_revenge.center)
        pygame.display.update()

    def inital_loop(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int], color_settings: List[Union[tuple, int]],\
                    cover: bool = False):
        self.__draw_cover(colors, font_settings, color_settings) if cover else self.__draw_intro(colors, font_settings)

    def loop(self, keys: list):
        self.__handle_paddle_movement(keys)
        self.ball.move()
        self.__handle_collision()
        self.__score_handling()

    def close_loop(self, colors: Tuple[tuple, tuple], font_settings: Tuple[str, int]):
        self.__draw_close(colors, font_settings)

    def reset_scores(self):
        self.left_score = 0
        self.right_score = 0