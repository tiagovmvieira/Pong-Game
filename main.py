"""
pong
author: tiago vieira , tiagovmvieira@hotmail.com
"""

#imports
import pygame
pygame.init()


WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong Game")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

WELCOME_FONT = pygame.font.Font("PixelEmulator-xq08.ttf", 20)
SCORE_FONT = pygame.font.Font("PixelEmulator-xq08.ttf", 50)
WINNIN_SCORE = 10

COLOR_SPD = 1
COL_DIR = [-1, -1, -1]
DEF_COLOR = [255, 255, 255]

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, WINDOW):
        pygame.draw.rect(WINDOW, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up = True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def col_change(DEF_COLOR, COL_DIR):
    for i in range (len(COL_DIR)):
        DEF_COLOR[i] += COLOR_SPD * COL_DIR[i]
        if DEF_COLOR[i] >= 255:
            DEF_COLOR[i] = 0
        elif DEF_COLOR[i] <= 0:
            DEF_COLOR[i] = 255

def draw_intro(WINDOW):
    WINDOW.fill(BLACK)

    welcome_text = WELCOME_FONT.render('Welcome to Pong!', 1, WHITE)
    text_rect_welcome = welcome_text.get_rect()
    text_rect_welcome.center = (WIDTH // 2 - welcome_text.get_width() // 2, (HEIGHT * 1 // 4 - welcome_text.get_height() // 2))

    enter_text = WELCOME_FONT.render('Press ENTER to continue', 1, DEF_COLOR)
    text_rect_enter = welcome_text.get_rect()
    text_rect_enter.center = (WIDTH // 2 - enter_text.get_width() // 2, (HEIGHT * 3 // 4 - enter_text.get_height() // 2))

    WINDOW.blit(welcome_text, text_rect_welcome.center)
    WINDOW.blit(enter_text, text_rect_enter.center)

    col_change(DEF_COLOR, COL_DIR)
    pygame.display.update()

def draw(WINDOW, paddles, ball, left_score, right_score):
    WINDOW.fill(BLACK)

    left_score_text = SCORE_FONT.render(f'{left_score}', 1, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, WHITE)
    WINDOW.blit(left_score_text, ((WIDTH // 4) - left_score_text.get_width() // 2, 20))
    WINDOW.blit(right_score_text, ((WIDTH // 4 + (WIDTH / 2) - right_score_text.get_width() // 2), 20))

    for paddle in paddles:
        paddle.draw(WINDOW)

    for i in range(10, HEIGHT, HEIGHT//20):
        if (i % 2) == 1: #odd i?
            continue
        pygame.draw.rect(WINDOW, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT//20))

    ball.draw(WINDOW)
    pygame.display.update() #manually update the display

def handle_collision_paddle_y_vel(ball, paddle):
    middle_y = paddle.y + paddle.height / 2
    difference_y = middle_y - ball.y
    ball.y_vel = -1 * difference_y / (paddle.height / 2) * ball.MAX_VEL

    return ball.y_vel

def handle_collision(ball, left_paddle, right_paddle):
    #collision with the field horizontal boundaries
    if (ball.y + ball.radius >= HEIGHT): #down (y)
        ball.y_vel *= -1
    elif (ball.y - ball.radius <= 0): #up (y)
        ball.y_vel *= -1

    #paddle collision
    if (ball.x_vel < 0):
        #going to collide to the left paddle
        if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height):
            if (ball.x - ball.radius <= left_paddle.x + left_paddle.width):
                ball.x_vel *= -1

                ball.y_vel = handle_collision_paddle_y_vel(ball, left_paddle)
    else:
        #going to collide to the rigth paddle
        if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height):
            if (ball.x + ball.radius >= right_paddle.x):
                ball.x_vel *= -1

                ball.y_vel = handle_collision_paddle_y_vel(ball, right_paddle)

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if (keys[pygame.K_w] and left_paddle.y > 0): #checks if the window dimensions are not exceed
        left_paddle.move(up = True)
    if (keys[pygame.K_s] and left_paddle.y + left_paddle.height <= HEIGHT): #checks if the window dimensions are not exceed
        left_paddle.move(up = False)

    if (keys[pygame.K_UP] and right_paddle.y > 0): #checks if the window dimensions are not exceed
        right_paddle.move(up = True)    
    if (keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height <= HEIGHT): #checks if the window dimensions are not exceed
        right_paddle.move(up = False)

def main():
    intro = True
    clock = pygame.time.Clock()

    while intro:
        clock.tick(FPS * 4)
        draw_intro(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    intro = False
                    break

    run = True

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0
    while run: #main event loop
        clock.tick(FPS)

        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed() #returns a list containing all the different keys that have been pressed
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if (ball.x > WIDTH):
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif (ball.x < 0):
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if (left_score >= WINNIN_SCORE):
            won = True
            win_text = "Left Player Won!"
        elif (right_score >= WINNIN_SCORE):
            won = True
            win_text = "Right Player Won!"
        
        if (won):
            text = SCORE_FONT.render(f'{win_text}', 1, WHITE)
            WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__' :
    main()