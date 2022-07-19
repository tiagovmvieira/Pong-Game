import game_constants

class Paddle:
    def __init__(self, x: int, y: int, width: int = game_constants.PADDLE_WIDTH, height: int = game_constants.PADDLE_HEIGHT,
                vel: float = game_constants.PADDLE_VEL, color: tuple = game_constants.PADDLE_COLOR):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color

    def move(self, up: bool = True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y