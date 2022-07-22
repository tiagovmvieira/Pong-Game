# imports
import pygame
import os

from typing import Tuple, List
from ball import Ball
from paddle import Paddle

def draw_intro(window: pygame.Surface, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int):
    window.fill(colors[0])

    welcome_font = pygame.font.SysFont('arial', font_size)
    # welcome_font = pygame.font.Font('assets/PixelEmulator-xq08.ttf',
    #                                font_size)
    welcome_message = welcome_font.render('Welcome to Pong!', 1, colors[1])
    text_rect_welcome = welcome_message.get_rect()
    text_rect_welcome.center = (window_dims[0] // 2 - welcome_message.get_width() // 2,
                             (window_dims[1] * 1 // 4 - welcome_message.get_height() // 2))

    enter_message = welcome_font.render('Press ENTER to continue', 1, colors[1])
    text_rect_enter = enter_message.get_rect()
    text_rect_enter.center = (window_dims[0] // 2 - enter_message.get_width() // 2,
                             (window_dims[1] * 3 // 4 - enter_message.get_height() // 2))

    window.blit(welcome_message, text_rect_welcome.center),
    window.blit(enter_message, text_rect_enter.center)

    pygame.display.update()


def draw(window: pygame.Surface, ball: Ball, paddles: Tuple[Paddle, Paddle], scores: list, colors: Tuple[tuple, tuple], window_dims: Tuple[int, int], font_size: int):
    window.fill(colors[0])

    score_font = pygame.font.SysFont('arial', font_size)

    left_score_text = score_font.render('{}'.format(scores[0]), 1, colors[1])
    right_score_text = score_font.render('{}'.format(scores[1]), 1, colors[1])

    window.blit(left_score_text, ((window_dims[0] // 4) - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, ((window_dims[0] // 4 + (window_dims[0] / 2) - right_score_text.get_width() // 2), 20))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, window_dims[1], window_dims[1] // 20):
        if (i % 2) == 1: #odd i?
            continue
        pygame.draw.rect(window, colors[1], (window_dims[0] // 2 - 5, i, 10, window_dims[1] / 20))
    
    ball.draw(window)
    pygame.display.update()


def handle_paddle_movement(keys: list, paddles: Tuple[Paddle, Paddle], window_height: int):
    if keys[pygame.K_w] and paddles[0].y > 0: #checks if the window dimensions are not exceed
        paddles[0].move(up = True)
    elif keys[pygame.K_s] and paddles[0].y + paddles[0].height <= window_height:
        paddles[0].move(up = False)
    elif keys[pygame.K_UP] and paddles[1].y > 0:
        paddles[1].move(up = True)
    elif keys[pygame.K_DOWN] and paddles[1].y + paddles[1].height <= window_height:
        paddles[1].move(up = False)


def handle_collision_paddle_y_vel(ball: Ball, paddle: Paddle)-> int:
    middle_y = paddle.y + paddle.height / 2
    difference_y = middle_y - ball.y
    ball.y_vel = -1 * difference_y / (paddle.height / 2) * ball.max_vel

    return ball.y_vel


def handle_collision(ball: Ball, paddles: Tuple[Paddle, Paddle], window_height: int):
    # collision with the field horizontal boundaries
    if (ball.y + ball.radius >= window_height): #down (y)
        ball.y_vel *= -1
    elif (ball.y - ball.radius <= 0): #up (y)
        ball.y_vel *= -1

    # paddle collision
    if ball.x_vel < 0:
        # going to collide to the left paddle
        if ball.y >= paddles[0].y and ball.y <= paddles[0].y + paddles[0].height:
            if ball.x - ball.radius <= paddles[0].x + paddles[0].width:
                ball.x_vel *= -1
                ball.y_vel = handle_collision_paddle_y_vel(ball, paddles[0])
    else:
        # going to collide to the right paddle
        if ball.y >= paddles[1].y and ball.y <= paddles[1].y + paddles[1].height:
            if ball.x + ball.radius >= paddles[1].x:
                ball.x_vel *= -1
                ball.y_vel = handle_collision_paddle_y_vel(ball, paddles[0])


def score_handling(ball: Ball, scores: list, paddles: Tuple[Paddle, Paddle], window_width: int)-> list:
    if ball.x > window_width:
        scores[0] += 1
        ball.reset()
        paddles[0].reset
        paddles[1].reset
    elif ball.x < 0:
        scores[1] += 1
        ball.reset()
        paddles[0].reset()
        paddles[1].reset()
    
    return scores


def winner_handling(scores, winning_score)-> tuple:
    if scores[0] == winning_score:
        won = True
        win_text = 'Left Player Won!'
    elif scores [1] == winning_score:
        won = True
        win_text = 'Right Player Won!'

    return won, win_text