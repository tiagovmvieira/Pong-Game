# imports
import pygame
import os

def draw_intro(window: pygame.Surface, black_color: tuple, white_color: tuple, font_size: int, window_width: int, window_height: int):
    window.fill(black_color)

    welcome_font = pygame.font.SysFont('arial', font_size)
    # welcome_font = pygame.font.Font('assets/PixelEmulator-xq08.ttf',
    #                                font_size)
    welcome_message = welcome_font.render('Welcome to Pong!', 1, white_color)
    text_rect_welcome = welcome_message.get_rect()
    text_rect_welcome.center = (window_width // 2 - welcome_message.get_width() // 2,
                             (window_height * 1 // 4 - welcome_message.get_height() // 2))

    enter_message = welcome_font.render('Press ENTER to continue', 1, white_color)
    text_rect_enter = enter_message.get_rect()
    text_rect_enter.center = (window_width // 2 - enter_message.get_width() // 2,
                             (window_height * 3 // 4 - enter_message.get_height() // 2))

    window.blit(welcome_message, text_rect_welcome.center),
    window.blit(enter_message, text_rect_enter.center)

    pygame.display.update()






    
